import { defineStore } from 'pinia'
import { JsGenerator } from "md_wasm";
import { NoteApi } from '@/api/note';
import { ResourceApi } from '@/api/resource';
import { NoteSchema } from '@/schemas/note';

async function createBlobAsync(newData: string): Promise<Blob> {
    return new Promise((resolve) => {
        const encoder = new TextEncoder();
        const dataArrayBuffer = encoder.encode(newData);

        const blobOptions = { type: "text/plain;charset=utf-8" };
        const blob = new Blob([dataArrayBuffer], blobOptions);

        resolve(blob);
    });
}

async function createFormDataAsync(blob: Blob): Promise<FormData> {
    return new Promise((resolve) => {
        const formData = new FormData();
        formData.append("file", blob);
        resolve(formData);
    });
}

async function saveContentAsync(id: number, newData: string) {
    const blob = await createBlobAsync(newData)
    const formData = await createFormDataAsync(blob)
    await NoteApi.saveNote(id, formData)
}

export const useMarkdownStore = defineStore('markdowns', {
    state: () => {
        return {
            markdownSplitedDataMap: new Map<number, string[]>(),
            generator: JsGenerator.new(),
        }
    },
    getters: {
        exist(state) {
            return (id: number) => state.markdownSplitedDataMap.has(id)
        },
        existLine(state) {
            return (id: number, lineNum: number) => {
                if (state.markdownSplitedDataMap.has(id)) {
                    return state.markdownSplitedDataMap.get(id)!.length > lineNum
                } else {
                    return false
                }
            }
        },
        getRawData(state) {
            return (id: number) => {
                if (state.markdownSplitedDataMap.has(id)) {
                    return state.markdownSplitedDataMap.get(id)!.join("\n")
                }
            }
        },
        getSplitDataSet(state) {
            return (id: number) => {
                return state.markdownSplitedDataMap.get(id)
            }
        },
        getSplitDataSetLength(state) {
            return (id: number) => {
                if (state.markdownSplitedDataMap.has(id)) {
                    return state.markdownSplitedDataMap.get(id)!.length
                }
                return 0
            }
        },
        getSplitData(state) {
            return (id: number, lineNum: number) => {
                const s = state.markdownSplitedDataMap.get(id)
                if (s) {
                    return s[lineNum]
                }
            }
        },
    },
    actions: {
        async insertNewDataAsync(id: number): Promise<NoteSchema> {
            const data = await NoteApi.getNote(id);
            const rawData = await ResourceApi.getResource(data.url);
            const splitData = this.generator.split(rawData)
            this.markdownSplitedDataMap.set(id, splitData)
            return data
        },
        async saveDataAsync(id: number) {
            const splitDataSet = this.getSplitDataSet(id)
            if (splitDataSet) {
                const rawData = splitDataSet.join('\n')
                if (rawData) {
                    await saveContentAsync(id, rawData)
                }
            }
        },
        updateLine(id: number, lineNum: number, data: string) {
            const rawDataSet = this.getSplitDataSet(id)
            if (rawDataSet) {
                rawDataSet[lineNum] = data
            }
        },
        appendLine(id: number, lineNum: number, data: string) {
            const rawDataSet = this.getSplitDataSet(id)
            if (rawDataSet) {
                if (lineNum + 1 < rawDataSet.length) {
                    rawDataSet.splice(lineNum + 1, 0, data);
                } else {
                    rawDataSet.push(data);
                }
            }
        },
        deleteLine(id: number, lineNum: number) {
            const rawDataSet = this.getSplitDataSet(id)
            if (rawDataSet) {
                if (rawDataSet.length !== 1) {
                    rawDataSet.splice(lineNum, 1)
                }
            }
        },
        combineLine(id: number, lineNum: number, data: string) {
            const rawDataSet = this.getSplitDataSet(id)
            if (rawDataSet) {
                if (lineNum !== 0) {
                    const lineLength = rawDataSet[lineNum - 1].length
                    rawDataSet[lineNum - 1] = rawDataSet[lineNum - 1] + data
                    rawDataSet.splice(lineNum, 1)
                    return lineLength
                }
            }
        },
        paste(id: number, lineNum: number, data: string, remainData: string, spliceData: string) {
            const rawDataSet = this.getSplitDataSet(id)
            if (rawDataSet) {
                let d = remainData + data + spliceData
                const newData = this.generator.split(d)
                if (newData.length > 0) {
                    rawDataSet.splice(lineNum, 1, ...newData)
                    return [lineNum + newData.length - 1, newData[newData.length - 1].length - spliceData.length]
                }
            }
        }
    }
})
