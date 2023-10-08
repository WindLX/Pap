<script setup lang="ts">
import * as pdfjs from 'pdfjs-dist'
import { nextTick, ref, Ref, onMounted } from 'vue'
import { ElScrollbar, ElPagination, ElSlider, ElButton } from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { Arrayable } from 'element-plus/es/utils/typescript.mjs';

// props
const props = defineProps<{
    id: string
    pdf: string
}>()

// data
const totalPages = ref(1)
let currentPage = ref(1)
let pdfDoc: pdfjs.PDFDocumentProxy | null = null
let pdfScale = ref(1)
const canvasItem: Ref<HTMLCanvasElement | null> = ref(null)

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

// load function
async function loadFile(url: string) {
    pdfjs.GlobalWorkerOptions.workerSrc = 'static/pdf.worker.min.js'
    const loadingTask = pdfjs.getDocument(url)
    try {
        pdfDoc = await loadingTask.promise
        totalPages.value = pdfDoc.numPages
        if (pdfDoc !== null) {
            await nextTick(() => {
                renderPage(pdfDoc!, 1)
            })
        }
    } catch (error) {
        console.log(error)
    }
}

async function renderPage(pdfDoc: pdfjs.PDFDocumentProxy, num: number) {
    const canvas: HTMLCanvasElement = canvasItem.value!
    try {
        const page = await pdfDoc.getPage(num)
        // page.cleanup()
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
        console.log(error)
    }
}

// hook
onMounted(() => {
    loadFile(props.pdf)
    canvasItem.value?.focus()
})
</script>

<template>
    <div class="pdf-container" style="height: 100%;">
        <div class="pdf-up">
            <el-button class="button" size="small" @click="handleScaleFit">
                <font-awesome-icon :icon="['fas', 'crop-simple']" class="icon" />
            </el-button>
            <el-slider v-model="pdfScale" :min="100" :max="500" size="small" style="width: 72px;margin-left: 12px;"
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
    /* align-items: center; */
    width: 100%;
}

.pdf-container canvas {
    width: 100%;
    height: 100%;
}
</style>