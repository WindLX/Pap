<script setup lang="ts">
import { computed, nextTick, onMounted, ref, provide } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ElScrollbar, ElNotification, ElLoading, ElSkeleton } from "element-plus";
import { INote } from "@/types/note-types";
import pFetch from '@/utils/fetch';
import Editor from './Editor.vue';

// props
const props = defineProps<{
    isNote: boolean
    id: number
}>();

const emits = defineEmits<{
    (e: 'lock', value: boolean): void,
    (e: 'save', value: boolean): void,
}>();

// data
const routerString = computed(() => {
    return props.isNote ? 'note' : 'content'
})
let mdData = ref<string | null>(null);
let name = "";
const editor = ref<InstanceType<typeof Editor> | null>(null);
let lockState = ref<boolean>(false);

// inject
provide('lockState', lockState);

// load
async function loadContentAsync() {
    await pFetch(`/${routerString.value}/get_${routerString.value}?${routerString.value}_id=${props.id}`, {
        successCallback: async (response) => {
            const data = await response.json() as INote
            name = data.name
            await pFetch(`/${data.url}`, {
                successCallback: async (response) => {
                    mdData.value = await response.text()
                }
            })
        }
    })
}

// save
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

async function saveContentAsync(newData: string) {
    const loadingInstance = ElLoading.service({ target: "#md-loader", fullscreen: true })
    mdData.value = newData
    const blob = await createBlobAsync(newData)
    const formData = await createFormDataAsync(blob)
    loadingInstance.close()
    try {
        await pFetch(`/${routerString.value}/save_${routerString.value}?${routerString.value}_id=${props.id}`, {
            method: 'POST',
            body: formData,
            isForm: true,
            successMsg: '文件保存成功',
            successCallback: async () => {
                emits('save', true)
            }
        })
    } catch (error) {
        ElNotification({
            title: '保存失败',
            message: 'blob创建失败',
            type: 'error',
            duration: 2000
        })
    }
}

async function downloadMdDataAsync(newData: string) {
    const blob = await createBlobAsync(newData);
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${name}.md`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function updateMdData(newData: string) {
    saveContentAsync(newData)
}

function downloadMdData() {
    if (editor.value) {
        editor.value.saveData()
        nextTick(() => {
            if (mdData.value) {
                downloadMdDataAsync(mdData.value)
            }
        })
    }
}

function exportPdf() {
    nextTick(() => {
        if (editor.value) {
            if (mdData.value) {
                let oldHTML = window.document.body.innerHTML;
                var printHTML = document.getElementById("md-print")?.innerHTML;
                if (printHTML) {
                    window.document.body.innerHTML = printHTML;
                    window.print();
                    location.reload();
                    window.document.body.innerHTML = oldHTML;
                }
            }
        }
    })
}

onMounted(async () => {
    await loadContentAsync()
    window.onbeforeprint = () => {
        editor.value?.saveData()
    }
})
</script>

<template>
    <div class="markdown" v-if="mdData !== null">
        <div class="markdown-tool">
            <font-awesome-icon :icon="['fas', lockState ? 'lock' : 'lock-open']" class="icon"
                :class="lockState ? 'lock' : ''" style="font-size: 24px;"
                @mousedown="lockState = !lockState; emits('lock', lockState)" />
            <font-awesome-icon :icon="['fas', 'floppy-disk']" class="icon" style="font-size: 24px;"
                @mousedown="editor?.saveData()" />
            <font-awesome-icon :icon="['fas', 'file-export']" class="icon" @mousedown="downloadMdData()" />
            <font-awesome-icon :icon="['fas', 'file-pdf']" class="icon" @mousedown="exportPdf()" />
        </div>
        <el-scrollbar id="md-loader">
            <Editor :md-data="mdData" :lock="lockState" @update:md-data="updateMdData" @on-edit="emits('save', false)"
                ref="editor" />
        </el-scrollbar>
    </div>
    <el-skeleton v-else :rows="10" class="md-block-skeleton" animated />
</template>

<style scoped>
.markdown-tool {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
    margin-bottom: 10px;
    padding: 5px 0;
    border: 1px solid #ccc;
    border-radius: 5px;
    width: fit-content;
}

.markdown-tool .icon {
    margin: 0 10px;
    font-size: 20px;
    color: #aaaaaa;
    cursor: pointer;
}

.markdown-tool .icon.lock {
    color: #4D78cc;
}

.markdown-tool .icon:hover {
    color: #4D78cc;
}

.md-block-skeleton {
    max-width: 95%;
    outline: none;
    position: relative;
    margin: 20px auto;
    cursor: wait;
}
</style>@/types/tag-types