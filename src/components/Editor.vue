<script setup lang="ts">
// import * as md_wasm from "md_wasm";
import { nextTick, ref } from "vue";
import MdBlock from "./MdBlock.vue";
import { ElScrollbar } from "element-plus";

// const generator = md_wasm.JsGenerator.new(1000);
// element
const container = ref<HTMLDivElement | null>(null);
const blocks = ref<Array<InstanceType<typeof MdBlock>>>([]);

// data
let rawDataSet = ref<Array<string>>([""])

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
</script>

<template>
    <div class="editor" ref="container">
        <el-scrollbar>
            <MdBlock v-for="(rawData, index) in rawDataSet" :key="index" :raw-data="rawData" :line-num="index" ref="blocks"
                @update:raw-data="(newValue) => rawDataSet[index] = newValue" @append-line="appendLine"
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
    height: inherit;
    border: 1px solid #ccc;
    position: relative;
}
</style>