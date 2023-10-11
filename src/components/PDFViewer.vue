<script setup lang="ts">
import * as pdfjs from 'pdfjs-dist'
import pdfWorker from "pdfjs-dist/build/pdf.worker";
import { nextTick, ref, Ref, onMounted, onActivated } from 'vue'
import {
    ElScrollbar, ElPagination, ElSlider,
    ElButtonGroup, ElButton, ElInput,
    ElColorPicker, ElNotification
} from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { Arrayable } from 'element-plus/es/utils/typescript.mjs';
import { ITag, IResourceItem } from 'resource-types';
import { TagEvent } from 'event-types';
import Tag from './Tag.vue';
import { useStateStore } from '../store/state';
import { useTagStore } from '../store/tag';

// props
const props = defineProps<{
    id: number
}>()

// state
const stateStore = useStateStore()
const tagStore = useTagStore()

tagStore.$onAction(
    ({
        name: name,
        after: after,
    }) => {
        after((result) => {
            switch (name) {
                case "onUpdate":
                    loadResourceItem()
                    break;
                case "onRemove":
                    loadResourceItem()
                    break;
                case "onDelete":
                    loadResourceItem()
                    break;
                case "onChoose":
                    const e = result as TagEvent
                    if (e.filterId === props.id) {
                        handleAddTag(result as TagEvent)
                    }
                    break;
                default:
                    break;
            }
        })
    }
)

// const
const predefineColors = [
    '#ff4500',
    '#ff8c00',
    '#ffd700',
    '#90ee90',
    '#00ced1',
    '#409EFF',
    '#c71585'
]

// style data
const inputVisible = ref(false)
const totalPages = ref(1)
let currentPage = ref(1)

// componment ref
const InputRef = ref<InstanceType<typeof ElInput>>()
const ColorRef = ref<InstanceType<typeof ElColorPicker>>()

// data
let pdf: string | null = null
let pdfDoc: pdfjs.PDFDocumentProxy | null = null
let pdfScale = ref(1)
const canvasItem: Ref<HTMLCanvasElement | null> = ref(null)
const inputValue = ref('')
const colorValue = ref('#409EFF')
let dynamicTags: Ref<Array<ITag>> = ref([])

// callback function
async function handleCurrentChange(_cur: number) {
    if (pdfDoc !== null) {
        await nextTick(() => {
            renderPage(pdfDoc!, currentPage.value)
        })
    }
}

async function handleScale(_val: Arrayable<number>) {
    await nextTick(() => {
        renderPage(pdfDoc!, currentPage.value)
    })
}

async function handleScaleFit() {
    pdfScale.value = 1
    await nextTick(() => {
        renderPage(pdfDoc!, currentPage.value)
    })
}

async function handleClose(tagId: number) {
    const response = await fetch(`${stateStore.backendHost}/tag/remove_tag?tag_id=${tagId}&resource_item_id=${props.id}`, {
        method: 'PUT',
        mode: 'cors',
    })
    if (response.status == 202) {
        dynamicTags.value.splice(dynamicTags.value.findIndex((t) => t.id === tagId), 1)
        tagStore.onRemove(tagId, props.id)
    } else {
        ElNotification({
            title: '移除失败',
            message: response.statusText,
            type: 'error',
            duration: 2000
        })
    }
}

async function handleInputConfirm() {
    if (inputValue.value) {
        const tagCreateData = {
            name: inputValue.value,
            color: colorValue.value,
            resource_item_id: props.id
        }
        const response = await fetch(`${stateStore.backendHost}/tag/create_tag`, {
            method: 'POST',
            mode: 'cors',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify(tagCreateData)
        })
        if (response.status != 201) {
            ElNotification({
                title: '创建失败',
                message: response.statusText,
                type: 'error',
                duration: 2000
            })
        } else {
            const data = await response.json()
            dynamicTags.value.push(data as ITag)
            tagStore.onCreate()
        }
    }
    inputVisible.value = false
    inputValue.value = ''
}

function handleInputCancel() {
    inputVisible.value = false
    inputValue.value = ''
}

function handleShowTag() {
    tagStore.show = true
    tagStore.editable = false
    tagStore.filterId = props.id
}

async function handleAddTag(tag: TagEvent) {
    const response = await fetch(`${stateStore.backendHost}/tag/add_tag?tag_id=${tag.tag.id}&resource_item_id=${props.id}`, {
        method: 'PUT',
        mode: 'cors'
    })
    if (response.status != 202) {
        ElNotification({
            title: '添加失败',
            message: response.statusText,
            type: 'error',
            duration: 2000
        })
    } else {
        const data = await response.json() as IResourceItem
        dynamicTags.value = data.tags
        tagStore.onAdd()
        handleInputCancel()
    }
}

// load function
async function loadFile(url: string) {
    pdfjs.GlobalWorkerOptions.workerSrc = pdfWorker
    const loadingTask = pdfjs.getDocument({
        url: url,
        cMapUrl: 'https://cdn.jsdelivr.net/npm/pdfjs-dist@2.5.207/cmaps/',
        cMapPacked: true
    })
    try {
        pdfDoc = await loadingTask.promise
        totalPages.value = pdfDoc.numPages
        if (pdfDoc !== null) {
            await nextTick(() => {
                renderPage(pdfDoc!, 1)
            })
        }
    } catch (error) {
        ElNotification({
            title: '加载失败',
            message: error as string,
            type: 'error',
            duration: 2000
        })
    }
}

async function loadResourceItem() {
    const response = await fetch(`${stateStore.backendHost}/resource/get_resource_item?resource_item_id=${props.id}`, {
        method: 'GET',
        mode: 'cors',
    })
    if (response.status != 200) {
        ElNotification({
            title: '查找失败',
            message: response.statusText,
            type: 'error',
            duration: 2000
        })
    } else {
        const data = await response.json() as IResourceItem
        dynamicTags.value = data.tags
        pdf = `${stateStore.backendHost}/${data.url}`
    }
}

// display function
function showInput() {
    inputVisible.value = true
    nextTick(() => {
        InputRef.value!
        ColorRef.value!.show()
    })
}

async function renderPage(pdfDoc: pdfjs.PDFDocumentProxy, num: number) {
    const canvas: HTMLCanvasElement = canvasItem.value!
    try {
        const page = await pdfDoc.getPage(num)
        page.cleanup()
        if (canvas) {
            const ctx = canvas.getContext('2d') as CanvasRenderingContext2D
            const scale = pdfScale.value / 100
            const viewport = page.getViewport({ scale: scale })
            canvas.height = Math.floor(viewport.height);
            canvas.width = Math.floor(viewport.width);
            const renderContext = {
                canvasContext: ctx,
                viewport: viewport
            }
            page.render(renderContext)
        }
    } catch (error) {
        ElNotification({
            title: '渲染失败',
            message: error as string,
            type: 'error',
            duration: 2000
        })
    }
}

// hook
onMounted(async () => {
    await loadResourceItem()
    loadFile(pdf!)
    canvasItem.value?.focus()
})

onActivated(async () => {
    await loadResourceItem()
})
</script>

<template>
    <div class="pdf-container" style="height: 100%;">
        <div class="pdf-up">
            <el-scrollbar>
                <div style="display: flex; margin-bottom: 18px; max-width: 50vw;">
                    <tag v-for="tag in dynamicTags" :key="tag.id" :color="tag.color" closable :disable="false"
                        @close="handleClose(tag.id)">
                        {{ tag.name }}
                    </tag>
                </div>
            </el-scrollbar>
            <el-input v-if="inputVisible" ref="InputRef" v-model="inputValue" class="item" size="small"
                style="width: 48px;">
            </el-input>
            <el-color-picker v-if="inputVisible" size="small" ref="ColorRef" v-model="colorValue"
                :predefine="predefineColors" />
            <el-button-group v-if="inputVisible" class="item" id="group">
                <el-button size="small" type="primary" @click="handleShowTag" class="button">
                    <font-awesome-icon :icon="['fas', 'tag']" class="icon" />
                </el-button>
                <el-button size="small" type="primary" @click="handleInputConfirm" class="button">
                    <font-awesome-icon :icon="['fas', 'check']" class="icon" />
                </el-button>
                <el-button size="small" type="primary" @click="handleInputCancel" class="button">
                    <font-awesome-icon :icon="['fas', 'xmark']" class="icon" />
                </el-button>
            </el-button-group>
            <el-button v-else class="item" size="small" @click="showInput">
                + 新标签
            </el-button>
        </div>
        <div class="pdf-middle">
            <el-button class="button" size="small" @click="handleScaleFit">
                <font-awesome-icon :icon="['fas', 'crop-simple']" class="icon" />
            </el-button>
            <el-slider v-model="pdfScale" :min="100" :max="500" size="small" style="width: 72px; margin-left: 24px;"
                @change="handleScale" />
        </div>
        <el-scrollbar>
            <canvas ref="canvasItem" />
        </el-scrollbar>
        <el-pagination v-model:current-page="currentPage" :page-size="10" :background="true" small
            layout="prev, pager, next, jumper" :page-count="totalPages" @current-change="handleCurrentChange">
        </el-pagination>
    </div>
</template>

<style scoped>
.pdf-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.pdf-container .pdf-up {
    display: flex;
}

.pdf-container .pdf-up .item {
    margin: 0 3px;
    height: 24px;
    min-width: 32px;
    width: fit-content;
}

.tag {
    border-width: 0;
}

.pdf-container .pdf-up #group {
    width: 84px;
}

.pdf-container .pdf-up .button {
    height: 24px;
    width: 28px;
}

.pdf-container .pdf-middle {
    display: flex;
    width: 100%;
}

.pdf-container canvas {
    width: 100%;
    height: 100%;
}
</style>