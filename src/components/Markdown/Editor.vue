<script setup lang="ts">
import { JsGenerator } from "md_wasm";
import { nextTick, onMounted, ref } from "vue";
import { ElScrollbar } from "element-plus";
import MdBlock from "./MdBlock.vue";

const props = defineProps<{
    mdData: string,
}>();

const emits = defineEmits<{
    (e: 'update:mdData', value: string): void,
    (e: 'onEdit'): void,
    (e: 'keyboard', key: string): void
}>();

defineExpose({
    saveData: () => {
        const newData = saveData()
        emits('update:mdData', newData)
    },
    grep: (regexPattern: string) => {
        if (regexPattern != '') {
            try {
                const regex = new RegExp(regexPattern, 'g');
                const matchingIndexes: number[] = [];
                rawDataSet.value.forEach((str, index) => {
                    const match = str.match(regex);
                    if (match && match.length > 0) {
                        matchingIndexes.push(index);
                    }
                });
                grepIndex.value = matchingIndexes
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

const generator = JsGenerator.new();

// element
const container = ref<HTMLDivElement | null>(null);
const blocks = ref<Array<InstanceType<typeof MdBlock>>>([]);

// data
let rawDataSet = ref<Array<string>>([""])
let grepIndex = ref<Array<number>>([])
let highlightIndex = ref<number | null>(null)

function handleKeyDown(event: KeyboardEvent) {
    if (event.ctrlKey) {
        event.preventDefault();
        switch (event.key) {
            case '3':
                const newData = saveData();
                emits('update:mdData', newData);
                break;
            default:
                emits('keyboard', event.key)
                break;
        }
    }
}

function saveData(): string {
    return rawDataSet.value.join('\n')
}

// edit    
function appendLine(lineNum: number, data: string) {
    if (lineNum + 1 < rawDataSet.value.length) {
        rawDataSet.value.splice(lineNum + 1, 0, data);
    } else {
        rawDataSet.value.push(data);
    }
    nextTick(() => {
        blocks.value[lineNum + 1].focusStart()
    })
}

function deleteLine(lineNum: number) {
    if (rawDataSet.value.length !== 1) {
        rawDataSet.value = rawDataSet.value.filter((_, index) => index !== lineNum)
        nextTick(() => {
            if (lineNum !== 0) {
                blocks.value[lineNum - 1].focusEnd()
            }
        })
    }
}

function combineLine(lineNum: number, data: string) {
    if (lineNum !== 0) {
        const lineLength = rawDataSet.value[lineNum - 1].length
        rawDataSet.value[lineNum - 1] = rawDataSet.value[lineNum - 1] + data
        rawDataSet.value = rawDataSet.value.filter((_, index) => index !== lineNum)
        nextTick(() => {
            blocks.value[lineNum - 1].focus(lineLength)
        })
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

function updateRawData(lineNum: number, data: string) {
    rawDataSet.value[lineNum] = data
    emits("onEdit")
}

onMounted(async () => {
    rawDataSet.value = await Promise.resolve(generator.split(props.mdData))
    if (rawDataSet.value.length === 0) {
        rawDataSet.value = [''];
    }
})
</script>

<template>
    <div class="editor">
        <el-scrollbar>
            <div class="editor-content" ref="container" @keydown="handleKeyDown" id="md-print">
                <MdBlock v-for="(rawData, index) in rawDataSet" :key="index" :raw-data="rawData" :line-num="index"
                    :is-highlight="grepIndex.includes(index)" ref="blocks"
                    @update:raw-data="(newValue: string) => updateRawData(index, newValue)" @append-line="appendLine"
                    @delete-line="deleteLine" @combine-line="combineLine" @up-line="upLine" @down-line="downLine">
                </MdBlock>
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
</style>