<script setup lang="ts">
import * as pdfjs from 'pdfjs-dist'
import pdfWorker from "pdfjs-dist/build/pdf.worker";
import { nextTick, ref, watch, onMounted, onActivated } from 'vue'
import {
    ElScrollbar, ElPagination,
    ElSlider, ElNotification, ElEmpty
} from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { Arrayable } from 'element-plus/es/utils/typescript.mjs';
import { ResourceApi } from '@/api/resource';
import { downloadUrlAsync } from '@/utils';

// props
const props = defineProps<{
    name: string,
    url: string,
    config: string | null
}>()

interface Config {
    pages: number[]
    scale: number
    rotation: number
}

let url = ref<string | null>(null)
let config = ref<Config | null>(null)

const totalPages = ref(1)
let currentPage = ref(1)
let pdfDoc: pdfjs.PDFDocumentProxy | null = null
let pdfScale = ref(500)
let pdfRotation = ref(0)
const canvasItem = ref<HTMLCanvasElement | null>(null)

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
    pdfScale.value = 500
    await nextTick(() => {
        renderPageAsync(pdfDoc!, currentPage.value)
    })
}

async function handleRotationAsync() {
    if (pdfRotation.value < 270) {
        pdfRotation.value += 90
    } else {
        pdfRotation.value = 0
    }
    await nextTick(() => {
        renderPageAsync(pdfDoc!, currentPage.value)
    })
}

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
        if (config.value) {
            totalPages.value = Math.min(pdfDoc.numPages, config.value.pages.length)
        } else {
            totalPages.value = pdfDoc.numPages
        }
        if (pdfDoc !== null) {
            await nextTick(() => {
                renderPageAsync(pdfDoc!, 1)
            })
        }
    } catch (error) {
    }
}

async function renderPageAsync(pdfDoc: pdfjs.PDFDocumentProxy, num: number) {
    const canvas: HTMLCanvasElement = canvasItem.value!
    try {
        var pageNum
        if (config.value) {
            pageNum = config.value.pages[num - 1]
        } else {
            pageNum = num
        }
        const page = await pdfDoc.getPage(pageNum)
        page.cleanup()
        if (canvas) {
            const ctx = canvas.getContext('2d') as CanvasRenderingContext2D
            const scale = pdfScale.value / 100
            const viewport = page.getViewport({ scale: scale, rotation: pdfRotation.value })
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
            title: '渲染PDF文件失败',
            message: error as string,
            type: 'error',
            duration: 2000
        })
    }
}

async function exportPdfAsync() {
    if (url.value) {
        await downloadUrlAsync(props.name, url.value)
    }
}

async function loadUrlAsync(newUrl: string) {
    if (newUrl.startsWith('./')) {
        url.value = await ResourceApi.getBlobUrl(newUrl)
    } else {
        url.value = newUrl
    }
    loadFileAsync(url.value)
}

function loadConfig(newConfig: string | null) {
    if (newConfig) {
        const configJson = JSON.parse(newConfig) as Config
        config.value = configJson
        pdfRotation.value = config.value.rotation
        pdfScale.value = config.value.scale * 100
    }
}

watch(props, async () => {
    await loadUrlAsync(props.url)
    loadConfig(props.config)
})

onMounted(async () => {
    await loadUrlAsync(props.url)
    loadConfig(props.config)
})

onActivated(async () => {
    await loadUrlAsync(props.url)
    loadConfig(props.config)
})
</script>

<template>
    <div class="pdf-container" v-if="url">
        <div class="pdf-middle">
            <font-awesome-icon :icon="['fas', 'crop-simple']" class="icon" @click="handleScaleFitAsync" />
            <font-awesome-icon :icon="['fas', 'file-export']" class="icon" @click="exportPdfAsync()" />
            <font-awesome-icon :icon="['fas', 'rotate-right']" class="icon" @click="handleRotationAsync()" />
            <el-slider v-model="pdfScale" :min="100" :max="500" size="small" class="slider" @change="handleScaleAsync" />
        </div>
        <el-pagination v-model:current-page="currentPage" :page-size="10" :background="true" small hide-on-single-page
            layout="prev, pager, next, jumper" :page-count="totalPages" @current-change="handleCurrentChangeAsync">
        </el-pagination>
        <el-scrollbar>
            <canvas ref="canvasItem" />
        </el-scrollbar>
    </div>
    <el-empty v-else description="加载失败" />
</template>

<style scoped>
.pdf-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.pdf-container .pdf-middle {
    display: flex;
    width: 100%;
    justify-content: center;
    margin-bottom: 10px;
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

.pdf-container .pdf-middle .slider {
    width: 72px;
    margin-left: 24px;
}

.pdf-container canvas {
    width: 100%;
    height: 100%;
}
</style>