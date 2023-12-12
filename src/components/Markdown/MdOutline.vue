<script setup lang="ts">
import { onActivated, onMounted, ref } from 'vue';
import { JsStatusGenerator } from 'md_wasm'
import { RawTitle, TitleLevel } from '@/md/mdexpr';
import { useMarkdownStore } from '@/store/markdown';
import type { TreeCreateNode } from '../Utils/Tree.vue';
import Tree from '../Utils/Tree.vue';

const props = defineProps<{
    name: string,
    id: number
}>()

const markdownStore = useMarkdownStore()

const generator = JsStatusGenerator.new()
const titles = ref<Array<TreeCreateNode>>([])

function jump(id: number) {
    document.getElementById(`md-title-${id}`)?.scrollIntoView({ behavior: "smooth" })
}

function levelToNumber(level: TitleLevel): number {
    switch (level) {
        case TitleLevel.H1: return 1;
        case TitleLevel.H2: return 2;
        case TitleLevel.H3: return 3;
        case TitleLevel.H4: return 4;
        case TitleLevel.H5: return 5;
        case TitleLevel.H6: return 6;
        default: return 0;
    }
}

async function loadTitleAsync() {
    const d = markdownStore.getRawData(props.id)
    if (d) {
        let t = await Promise.resolve<Array<RawTitle>>(generator.get_js_titles(d))
        titles.value = t.map((t) => {
            return {
                id: t.line,
                level: levelToNumber(t.level),
                data: t.content
            }
        })
    }
}

onMounted(async () => {
    await loadTitleAsync()
})

onActivated(async () => {
    await loadTitleAsync()
})
</script>

<template>
    <div class="md-outline">
        <span class="root-name">
            {{ props.name }}
        </span>
        <Tree v-if="titles.length > 0" :raw-data="titles" @node-click="jump" />
    </div>
</template>

<style scoped>
.md-outline {
    position: absolute;
    right: 0;
    z-index: 40;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    padding: 10px 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: calc(100vh - 140px);
    width: 300px;
    user-select: none;
    overflow-y: auto;
}

.md-outline .root-name {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 12px;
}
</style>