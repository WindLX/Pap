<script setup lang="ts">
import { Link } from '@/md/mdexpr';
import { watch, ref, onMounted, onActivated, computed } from 'vue';
import PDFViewer from '../MdExtend/PDFViewer.vue';
import VideoViewer from '../MdExtend/VideoViewer.vue';
import AudioViewer from '../MdExtend/AudioViewer.vue';

const props = defineProps<{
    link: Link
}>()

const url = ref('')
const config = ref<string | null>(null)

const currentComponent = computed(() => {
    if (isPDF(url.value)) {
        return PDFViewer
    } else if (isVideo(url.value)) {
        return VideoViewer
    } else if (isAudio(url.value)) {
        return AudioViewer
    }
});

function extractGroups(url: string): [string, string | null] {
    const reg = /(.*) (\{.*\})/gm;
    const match = reg.exec(url);

    if (match) {
        const group1 = match[1].trim();
        const group2 = match[2].trim();
        return [group1, group2];
    } else {
        return [url, null];
    }
}

function generateURL() {
    const u = extractGroups(props.link.href!)
    url.value = u[0]
    config.value = u[1]
}

function isPDF(url: string): boolean {
    return (url.endsWith('.pdf') || url.endsWith('.PDF'))
}

function isVideo(url: string): boolean {
    return (url.endsWith('.mp4') || url.endsWith('.webm') || url.endsWith('.flv') || url.endsWith('.mkv'))
}

function isAudio(url: string): boolean {
    return (url.endsWith('.mp3') || url.endsWith('.wav'))
}

watch(props, () => {
    generateURL()
})

onMounted(() => {
    generateURL()
})

onActivated(() => {
    generateURL()
})
</script>

<template>
    <div class="link-extend">
        <component :is="currentComponent" :name="props.link.content" :url="url.slice(6)" :config="config" />
    </div>
</template>

<style scoped></style>