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
import type { ITag, IResourceItem } from '@/types/resource-types';
import type { TagEvent } from '@/types/event-types';
import { state, tag } from '@store';
import pFetch from '@/utils/fetch';
import Tag from '@components/Tag/Tag.vue';

// props
const props = defineProps<{
    id: number
}>()

// state
const stateStore = state.useStateStore()
const tagStore = tag.useTagStore()

tagStore.$onAction(
    ({
        name: name,
        after: after,
    }) => {
        after((result) => {
            switch (name) {
                case "onUpdate":
                    loadResourceItemAsync()
                    break;
                case "onRemove":
                    loadResourceItemAsync()
                    break;
                case "onDelete":
                    loadResourceItemAsync()
                    break;
                case "onChoose":
                    const e = result as TagEvent
                    if (e.filterId === props.id) {
                        handleAddTagAsync(result as TagEvent)
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
async function handleCurrentChangeAsync(_cur: number) {
    if (pdfDoc !== null) {
        await nextTick(() => {
            renderPageAsync(pdfDoc!, currentPage.value)
        })
    }
}

async function handleScaleAsync(_val: Arrayable<number>) {
    await nextTick(() => {
        renderPageAsync(pdfDoc!, currentPage.value)
    })
}

async function handleScaleFitAsync() {
    pdfScale.value = 1
    await nextTick(() => {
        renderPageAsync(pdfDoc!, currentPage.value)
    })
}

async function handleCloseAsync(tagId: number) {
    await pFetch(`/tag/remove_tag?tag_id=${tagId}&resource_item_id=${props.id}`, {
        method: 'PUT',
        successCallback: async () => {
            dynamicTags.value.splice(dynamicTags.value.findIndex((t) => t.id === tagId), 1)
            tagStore.onRemove(tagId, props.id)
        }
    })
}

async function handleInputConfirmAsync() {
    if (inputValue.value) {
        const tagCreateData = {
            name: inputValue.value,
            color: colorValue.value,
            resource_item_id: props.id
        }
        await pFetch(`/tag/create_tag`, {
            method: 'POST',
            body: JSON.stringify(tagCreateData),
            successCallback: async (response) => {
                const data = await response.json()
                dynamicTags.value.push(data as ITag)
                tagStore.onCreate()
            }
        })
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

async function handleAddTagAsync(tag: TagEvent) {
    await pFetch(`/tag/add_tag?tag_id=${tag.tag.id}&resource_item_id=${props.id}`, {
        method: 'PUT',
        successCallback: async (response) => {
            const data = await response.json() as IResourceItem
            dynamicTags.value = data.tags
            tagStore.onAdd()
            handleInputCancel()
        }
    })
}

// load function
async function loadFileAsync(url: string) {
    pdfjs.GlobalWorkerOptions.workerSrc = pdfWorker
    const loadingTask = pdfjs.getDocument({
        httpHeaders: {
            "Authorization": `Bearer ${localStorage.getItem('token')}`
        },
        url: url,
        cMapUrl: 'https://cdn.jsdelivr.net/npm/pdfjs-dist@2.5.207/cmaps/',
        cMapPacked: true
    })
    try {
        pdfDoc = await loadingTask.promise
        totalPages.value = pdfDoc.numPages
        if (pdfDoc !== null) {
            await nextTick(() => {
                renderPageAsync(pdfDoc!, 1)
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

async function loadResourceItemAsync() {
    await pFetch(`/resource/get_resource_item?resource_item_id=${props.id}`, {
        successCallback: async (response) => {
            const data = await response.json() as IResourceItem
            dynamicTags.value = data.tags
            pdf = `${stateStore.backendHost}/${data.url}`
        }
    })
}

// display function
function showInput() {
    inputVisible.value = true
    nextTick(() => {
        InputRef.value!
        ColorRef.value!.show()
    })
}

async function renderPageAsync(pdfDoc: pdfjs.PDFDocumentProxy, num: number) {
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

async function exportPdfAsync(pdfUrl: string) {
    const response = await fetch(pdfUrl, {
        method: 'GET',
        mode: 'cors',
    });
    const data = await response.blob();
    const blob = new Blob([data], { type: 'application/pdf' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', pdfUrl.split('/').pop()!);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function exportPdf() {
    if (pdf) {
        exportPdfAsync(pdf)
    }
}

// hook
onMounted(async () => {
    await loadResourceItemAsync()
    loadFileAsync(pdf!)
})

onActivated(async () => {
    await loadResourceItemAsync()
})
</script>

<template>
    <div class="pdf-container" style="height: 100%;">
        <div class="pdf-up">
            <el-scrollbar>
                <div style="display: flex; margin-bottom: 18px; max-width: 50vw;">
                    <tag v-for="tag in dynamicTags" :key="tag.id" :color="tag.color" closable :disable="false"
                        @close="handleCloseAsync(tag.id)">
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
                <el-button size="small" type="primary" @click="handleInputConfirmAsync" class="button">
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
            <font-awesome-icon :icon="['fas', 'crop-simple']" class="icon" @click="handleScaleFitAsync" />
            <font-awesome-icon :icon="['fas', 'file-export']" class="icon" @mousedown="exportPdf()" />
            <el-slider v-model="pdfScale" :min="100" :max="500" size="small" style="width: 72px; margin-left: 24px;"
                @change="handleScaleAsync" />
        </div>
        <el-scrollbar>
            <canvas ref="canvasItem" />
        </el-scrollbar>
        <el-pagination v-model:current-page="currentPage" :page-size="10" :background="true" small
            layout="prev, pager, next, jumper" :page-count="totalPages" @current-change="handleCurrentChangeAsync">
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

.pdf-container .pdf-middle .icon {
    margin: 0 10px;
    font-size: 20px;
    color: #aaaaaa;
    cursor: pointer;
}

.pdf-container .pdf-middle .icon:hover {
    color: #4D78cc;
}

.pdf-container canvas {
    width: 100%;
    height: 100%;
}
</style>@/types/tag-types