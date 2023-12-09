<script setup lang="ts">
import { Link } from '@/md/mdexpr';
import { watch, ref, onMounted, onActivated } from 'vue';
import { ElEmpty } from 'element-plus';
import PDFViewer from '../MdExtend/PDFViewer.vue';

const props = defineProps<{
    link: Link
}>()

const url = ref('')
const config = ref<string | null>(null)

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
        <PDFViewer v-if="isPDF(url)" :name="props.link.content" :url="url.slice(6)" :config="config" />
        <el-empty v-else description="无法加载的文件类型" />
    </div>
</template>

<style scoped></style>