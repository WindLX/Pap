<script setup lang="ts">
import { nextTick, onMounted, ref, provide, reactive } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ElLoading, ElSkeleton } from "element-plus";
import { ResourceApi } from '@/api/resource';
import { downloadUrlAsync } from '@/utils';
import { useMarkdownStore } from '@/store/markdown';
import Editor from './Editor.vue';
import MdOutline from './MdOutline.vue';
import TagList from '../Tag/TagList.vue';
import Grep from './Grep.vue';

// props
const props = defineProps<{
    id: number
}>();

const emits = defineEmits<{
    (e: 'lock', value: boolean): void,
    (e: 'save', value: boolean): void,
}>();

const markdownStore = useMarkdownStore();

// data
let name = ref<string>("");
let url = ref<string>("");
const editor = ref<InstanceType<typeof Editor> | null>(null);
let lockState = ref<boolean>(false);
let isToolbarShow = reactive([false, false, false, false])
let updateStatus = ref<number>(new Date().getTime())

// inject
provide('lockState', lockState);

// load
async function loadContentAsync() {
    const note = await markdownStore.insertNewDataAsync(props.id)
    name.value = note.name
    url.value = note.url
}

// save
async function saveContentAsync() {
    const loadingInstance = ElLoading.service({ target: "#md-loader", fullscreen: true })
    await markdownStore.saveDataAsync(props.id)
    loadingInstance.close()
    emits('save', true)
    updateStatus.value = new Date().getTime()
}

async function downloadMdDataAsync() {
    await markdownStore.saveDataAsync(props.id)
    const newUrl = await ResourceApi.getBlobUrl(url.value);
    await downloadUrlAsync(`${name.value}.md`, newUrl)
}

function exportPdf() {
    nextTick(() => {
        let oldHTML = window.document.body.innerHTML;
        var printHTML = document.getElementById("md-print")?.innerHTML;
        if (printHTML) {
            window.document.body.innerHTML = printHTML;
            window.print();
            location.reload();
            window.document.body.innerHTML = oldHTML;
        }
    })
}

function handleShowToolbar(index: number) {
    const s = isToolbarShow[index]
    isToolbarShow.fill(false)
    isToolbarShow[index] = !s
}

function handleLock() {
    lockState.value = !lockState.value;
    emits('lock', lockState.value)
}

async function handleKeyDown(key: string) {
    switch (key) {
        case '1':
            handleShowToolbar(0)
            break;
        case '2':
            handleLock()
            break;
        case 's':
            await saveContentAsync();
            break;
        case '4':
            await downloadMdDataAsync()
            break;
        case '5':
            exportPdf()
            break;
        case '6':
            handleShowToolbar(1)
            break;
        case '7':
            handleShowToolbar(2)
            break;
        default:
            break;
    }
}

function handleGrep(regex: string) {
    editor.value?.grep(regex)
}

function handleFocusLast() {
    editor.value?.focusLast()
}

function handleFocusNext() {
    editor.value?.focusNext()
}

function handleGrepClear() {
    editor.value?.grepClear()
}

onMounted(async () => {
    await loadContentAsync()
    window.onbeforeprint = async () => {
        await markdownStore.saveDataAsync(props.id)
    }
})
</script>

<template>
    <div class="markdown" v-if="markdownStore.exist(props.id)">
        <div class="markdown-tool">
            <font-awesome-icon :icon="['fas', 'tags']" class="icon" :class="isToolbarShow[0] ? 'active' : ''"
                @mousedown="handleShowToolbar(0)" />
            <font-awesome-icon :icon="['fas', lockState ? 'lock' : 'lock-open']" class="icon"
                :class="lockState ? 'active' : ''" @mousedown="handleLock()" />
            <font-awesome-icon :icon="['fas', 'floppy-disk']" class="icon" style="font-size: 22px;"
                @mousedown="saveContentAsync()" />
            <font-awesome-icon :icon="['fas', 'file-export']" class="icon" @mousedown="downloadMdDataAsync()" />
            <font-awesome-icon :icon="['fas', 'file-pdf']" class="icon" @mousedown="exportPdf()" />
            <font-awesome-icon :icon="['fas', 'hashtag']" class="icon" :class="isToolbarShow[1] ? 'active' : ''"
                @mousedown="handleShowToolbar(1)" style="font-size: 22px;" />
            <font-awesome-icon :icon="['fas', 'magnifying-glass']" class="icon" :class="isToolbarShow[2] ? 'active' : ''"
                @mousedown="handleShowToolbar(2)" />
        </div>
        <Transition name="drag">
            <TagList :id="props.id" v-show="isToolbarShow[0]" />
        </Transition>
        <Transition name="push">
            <MdOutline :id="props.id" :name="name" v-show="isToolbarShow[1]" :key="updateStatus" />
        </Transition>
        <Transition name="drag">
            <Grep v-show="isToolbarShow[2]" @grep="handleGrep" @focus-last="handleFocusLast" @focus-next="handleFocusNext"
                @clear="handleGrepClear" />
        </Transition>
        <Editor :id="props.id" @on-edit="emits('save', false)" @keyboard="handleKeyDown" ref="editor" />
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