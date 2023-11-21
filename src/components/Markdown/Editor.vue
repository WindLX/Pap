<script setup lang="ts">
import { JsGenerator } from "md_wasm";
import { nextTick, onMounted, ref } from "vue";
import MdBlock from "./MdBlock.vue";
import { ElScrollbar } from "element-plus";

const props = defineProps<{
    mdData: string,
}>();

const emits = defineEmits<{
    (e: 'update:mdData', value: string): void,
    (e: 'onEdit'): void,
}>();

defineExpose({
    saveData: () => {
        const newData = saveData()
        emits('update:mdData', newData)
    },
})

const generator = JsGenerator.new();

// element
const container = ref<HTMLDivElement | null>(null);
const blocks = ref<Array<InstanceType<typeof MdBlock>>>([]);

// data
let rawDataSet = ref<Array<string>>([""])

function handleKeyDown(event: KeyboardEvent) {
    if (event.ctrlKey && event.key === 's') {
        event.preventDefault();
        const newData = saveData();
        emits('update:mdData', newData);
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
        blocks.value[lineNum + 1].focus()
    })
}

function deleteLine(lineNum: number) {
    if (rawDataSet.value.length !== 1) {
        rawDataSet.value = rawDataSet.value.filter((_, index) => index !== lineNum)
        nextTick(() => {
            if (lineNum !== 0) {
                blocks.value[lineNum - 1].focus()
            }
        })
    }
}

function combineLine(lineNum: number, data: string) {
    if (lineNum !== 0) {
        rawDataSet.value[lineNum - 1] = rawDataSet.value[lineNum - 1] + data
        rawDataSet.value = rawDataSet.value.filter((_, index) => index !== lineNum)
        nextTick(() => {
            blocks.value[lineNum - 1].focus()
        })
    }

}

function upLine(lineNum: number) {
    if (lineNum > 0) {
        blocks.value[lineNum - 1].focus()
    }
}

function downLine(lineNum: number) {
    if (lineNum < blocks.value.length - 1) {
        blocks.value[lineNum + 1].focus()
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
    <div class="editor" ref="container" @keydown="handleKeyDown" id="md-print">
        <el-scrollbar>
            <MdBlock v-for="(rawData, index) in rawDataSet" :key="index" :raw-data="rawData" :line-num="index" ref="blocks"
                @update:raw-data="(newValue: string) => updateRawData(index, newValue)" @append-line="appendLine"
                @delete-line="deleteLine" @combine-line="combineLine" @up-line="upLine" @down-line="downLine">
            </MdBlock>
        </el-scrollbar>
    </div>
</template>

<style scoped>
.editor {
    max-width: 100%;
    grid-area: content;
    display: flex;
    flex-direction: column;
    border: 1px solid #ccc;
    position: relative;
    border-radius: 10px;
    padding: 10px 0;
}
</style>