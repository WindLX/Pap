<script setup lang="ts">
import { nextTick, onMounted, ref, provide } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ElLoading, ElSkeleton } from "element-plus";
import { NoteApi } from '@/api/note';
import { ResourceApi } from '@/api/resource';
import Editor from './Editor.vue';
import MdOutline from './MdOutline.vue';
import TagList from '../Tag/TagList.vue';

// props
const props = defineProps<{
    id: number
}>();

const emits = defineEmits<{
    (e: 'lock', value: boolean): void,
    (e: 'save', value: boolean): void,
}>();

// data
let mdData = ref<string | null>(null);
let name = ref<string>("");
const editor = ref<InstanceType<typeof Editor> | null>(null);
let lockState = ref<boolean>(false);
let isTagListShow = ref<boolean>(false);
let isRightbarShow = ref<boolean>(false);
let updateStatus = ref<number>(new Date().getTime())

// inject
// provide('updateStatus', updateStatus)
provide('lockState', lockState);

// load
async function loadContentAsync() {
    const data = await NoteApi.getNote(props.id);
    name.value = data.name
    mdData.value = await ResourceApi.getResource(data.url);
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
    await NoteApi.saveNote(props.id, formData)
    emits('save', true)
    updateStatus.value = new Date().getTime()
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

function handleShowTagList() {
    isTagListShow.value = !isTagListShow.value
    isRightbarShow.value = false
}

function handleShowOutline() {
    isRightbarShow.value = !isRightbarShow.value
    isTagListShow.value = false
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
            <font-awesome-icon :icon="['fas', 'tags']" class="icon" :class="isTagListShow ? 'active' : ''"
                @mousedown="handleShowTagList()" />
            <font-awesome-icon :icon="['fas', lockState ? 'lock' : 'lock-open']" class="icon"
                :class="lockState ? 'active' : ''" @mousedown="lockState = !lockState; emits('lock', lockState)" />
            <font-awesome-icon :icon="['fas', 'floppy-disk']" class="icon" style="font-size: 22px;"
                @mousedown="editor?.saveData()" />
            <font-awesome-icon :icon="['fas', 'file-export']" class="icon" @mousedown="downloadMdData()" />
            <font-awesome-icon :icon="['fas', 'file-pdf']" class="icon" @mousedown="exportPdf()" />
            <font-awesome-icon :icon="['fas', 'hashtag']" class="icon" :class="isRightbarShow ? 'active' : ''"
                @mousedown="handleShowOutline()" style="font-size: 22px;" />
        </div>
        <Transition name="drag">
            <TagList :id="props.id" v-show="isTagListShow" />
        </Transition>
        <Transition name="push">
            <MdOutline :md-data="mdData" :name="name" v-show="isRightbarShow" :key="updateStatus" />
        </Transition>
        <Editor :md-data="mdData" :lock="lockState" @update:md-data="updateMdData" @on-edit="emits('save', false)"
            ref="editor" />
    </div>
    <el-skeleton v-else :rows="10" class="md-block-skeleton" animated />
</template>

<style scoped>
.drag-enter-active {
    animation: drag-in 0.3s;
}

.drag-leave-active {
    animation: drag-in 0.3s reverse;
}

@keyframes drag-in {
    0% {
        transform: translateY(-50%);
        opacity: 0;
    }

    100% {
        opacity: 1;
    }
}

.push-enter-active {
    animation: push-in 0.3s;
}

.push-leave-active {
    animation: push-in 0.3s reverse;
}

@keyframes push-in {
    0% {
        transform: translateX(50%);
        opacity: 0;
    }

    100% {
        opacity: 1;
    }
}

.markdown {
    position: relative;
}

.markdown .markdown-tool {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
    padding: 5px 0;
    width: fit-content;
    margin-bottom: 5px;
}

.markdown .icon {
    margin: 0 10px;
    font-size: 20px;
    color: #aaaaaa;
    cursor: pointer;
}

.markdown .icon.active {
    color: var(--el-color-primary);
}

.markdown .icon:hover {
    color: var(--el-color-primary);
}

.markdown .md-block-skeleton {
    max-width: 95%;
    outline: none;
    position: relative;
    margin: 20px auto;
    cursor: wait;
}
</style>