<script setup lang="ts">
import { nextTick, onMounted, ref } from "vue";
import { ElScrollbar } from "element-plus";
import { useMarkdownStore } from "@/store/markdown";
import MdBlock from "./MdBlock.vue";

const props = defineProps<{
    id: number
}>();

const emits = defineEmits<{
    (e: 'onEdit'): void,
    (e: 'keyboard', key: string): void
}>();

defineExpose({
    grep: (regexPattern: string) => {
        if (regexPattern != '') {
            try {
                const rawDataSet = markdownStore.getSplitDataSet(props.id);
                if (rawDataSet) {
                    const regex = new RegExp(regexPattern, 'g');
                    const matchingIndexes: number[] = [];
                    rawDataSet.forEach((str, index) => {
                        const match = str.match(regex);
                        if (match && match.length > 0) {
                            matchingIndexes.push(index);
                        }
                    });
                    grepIndex.value = matchingIndexes
                }
            } catch (e) {
            }
        } else {
            grepIndex.value = []
            highlightIndex.value = null
        }
    },
    focusLast: () => {
        if (grepIndex.value.length > 0) {
            if (highlightIndex.value === null) {
                highlightIndex.value = 0
            } else if (highlightIndex.value > 0) {
                highlightIndex.value -= 1
            }
            document.getElementById(`md-block-${grepIndex.value[highlightIndex.value]}`)?.scrollIntoView({ behavior: "smooth" })
        }
    },
    focusNext: () => {
        if (grepIndex.value.length > 0) {
            if (highlightIndex.value === null) {
                highlightIndex.value = 0
            } else if (highlightIndex.value < grepIndex.value.length) {
                highlightIndex.value += 1
            }
            document.getElementById(`md-block-${grepIndex.value[highlightIndex.value]}`)?.scrollIntoView({ behavior: "smooth" })
        }
    },
    grepClear: () => {
        grepIndex.value = []
        highlightIndex.value = null
    }
})


const markdownStore = useMarkdownStore()

markdownStore.$onAction(({
    name,
    args,
    after
}) => {
    after((result) => {
        switch (name) {
            case 'updateLine':
                emits('onEdit')
                break;
            case 'appendLine':
                updateLines()
                emits('onEdit')
                nextTick(() => {
                    blocks.value[args[1] + 1].focusStart()
                })
                break;
            case 'deleteLine':
                updateLines()
                emits('onEdit')
                nextTick(() => {
                    if (args[1] !== 0) {
                        blocks.value[args[1] - 1].focusEnd()
                    }
                })
                break;
            case 'combineLine':
                updateLines()
                emits('onEdit')
                blocks.value[args[1] - 1].update()
                nextTick(() => {
                    if (result) {
                        blocks.value[args[1] - 1].focus(result as number)
                    }
                })
                break;
            case 'paste':
                updateLines()
                emits('onEdit')
                nextTick(() => {
                    if (result) {
                        blocks.value[(result as number[])[0]].focus((result as number[])[1])
                    }
                })
                break;
            default:
                break;
        }
    })
})

// element
const container = ref<HTMLDivElement | null>(null);
const blocks = ref<Array<InstanceType<typeof MdBlock>>>([]);

// data
let lines = ref<Array<string>>([])
let grepIndex = ref<Array<number>>([])
let highlightIndex = ref<number | null>(null)

function handleKeyDown(event: KeyboardEvent) {
    if (event.ctrlKey) {
        if (['1', '2', 's', '4', '5', '6', '7'].includes(event.key))
            event.preventDefault()
        emits('keyboard', event.key)
    }
}

function upLine(lineNum: number) {
    if (lineNum > 0) {
        blocks.value[lineNum - 1].focusEnd()
    }
}

function downLine(lineNum: number) {
    if (lineNum < blocks.value.length - 1) {
        blocks.value[lineNum + 1].focusEnd()
    }
}

function updateLines() {
    if (markdownStore.exist(props.id)) {
        lines.value = markdownStore.getSplitDataSet(props.id)!
    }
}

onMounted(() => {
    updateLines()
})
</script>

<template>
    <div class="editor">
        <el-scrollbar>
            <div class="editor-content" ref="container" @keydown="handleKeyDown" id="md-print">
                <MdBlock v-for="(_d, index) in lines" :key="index" :id="props.id" :line-num="index"
                    :is-highlight="grepIndex.includes(index)" ref="blocks" @up-line="upLine" @down-line="downLine">
                </MdBlock>
                <div class="blank" />
            </div>
        </el-scrollbar>
    </div>
</template>

<style scoped>
.editor {
    max-width: 100%;
    display: flex;
    flex-direction: column;
    position: relative;
    padding: 10px 0;
}

.editor-content {
    height: calc(100vh - 140px);
}

.editor .editor-content .blank {
    max-width: 90%;
    outline: none;
    position: relative;
    margin: 5px;
    margin-left: 12px;
    margin-right: 12px;
    height: calc(100vh - 500px);
}
</style>