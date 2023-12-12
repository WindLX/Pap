<script setup lang="ts">
import katex from "katex";
import { JsGenerator } from "md_wasm";
import { Ref, nextTick, onMounted, ref, inject } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { ElImage, ElSkeleton } from "element-plus";
import type { Block, Paragraph, Title, ListItem, TodoItem, Footer, Image } from "@/md/mdexpr";
import { BlockTag } from "@/md/mdexpr";
import { ResourceApi } from "@/api/resource";
import { useMarkdownStore } from "@/store/markdown";
import MdParagraph from './MdParagraph.vue';

const props = defineProps<{
    id: number,
    lineNum: number,
    isHighlight?: boolean,
}>();

const emits = defineEmits<{
    (e: 'upLine', value: number): void;
    (e: 'downLine', value: number): void;
}>()

defineExpose({
    update: async () => {
        await updateLineAsync()
    },
    focus: (pos: number) => {
        isEdit.value = true;
        handleFocus(pos)
    },
    focusEnd: () => {
        isEdit.value = true;
        handleFocusEnd()
    },
    focusStart: () => {
        isEdit.value = true;
        handleFocusStart()
    }
})

// data
const markdownStore = useMarkdownStore()
const splitData = ref('')
const block = ref<Block>()
const raw: Ref<HTMLSpanElement | null> = ref(null);
const math: Ref<HTMLDivElement | null> = ref(null);
let isEdit = ref(false);
let src = ref<string>('');
const lock = inject<Ref<boolean>>('lockState')
const generator = JsGenerator.new()

async function serializeAsync(rawData: string): Promise<Block> {
    var p = new Promise<Block>((resolve) => {
        try {
            const result = generator.serialize(rawData);
            resolve(result);
        } catch (_e) {
            resolve({
                tag: BlockTag.Error,
                content: rawData
            });
        }
    })
    return p
}

async function handleInputAsync() {
    if (raw.value) {
        const data = raw.value.innerText
        markdownStore.updateLine(props.id, props.lineNum, data);
        await updateLineAsync()
    }
}

function handleEdit() {
    if (!lock?.value) {
        isEdit.value = true;
        handleFocusEnd();
    }
}

function handleTouchEdit(event: TouchEvent) {
    if (!lock?.value && event.touches.length == 2) {
        isEdit.value = true;
        handleFocusEnd();
    }
}

async function handleBehaviorAsync(e: KeyboardEvent) {
    const selection = window.getSelection();
    const focusOffset = selection?.focusOffset;
    switch (e.key) {
        case 'Enter':
            e.preventDefault();
            if ((block.value?.tag === BlockTag.CodeBlock
                || block.value?.tag === BlockTag.MathBlock)
                && focusOffset !== raw.value?.innerText.length && selection && raw.value) {
                const oldRange = selection.getRangeAt(0);
                const end = oldRange.endOffset
                raw.value.innerText =
                    raw.value.innerText.slice(0, end)
                    + '\n'
                    + raw.value.innerText.slice(end);
                markdownStore.updateLine(props.id, props.lineNum, raw.value.innerText);
                await updateLineAsync()
                const rangePos = end + 1
                handleFocus(rangePos)
            } else {
                const remainData = splitData.value.slice(0, focusOffset)
                const sliceData = splitData.value.slice(focusOffset)
                markdownStore.updateLine(props.id, props.lineNum, remainData);
                markdownStore.appendLine(props.id, props.lineNum, sliceData);
                await updateLineAsync()
            }
            break;
        case 'Tab':
            e.preventDefault();
            if (raw.value && selection) {
                const oldRange = selection.getRangeAt(0);
                const end = oldRange.endOffset
                raw.value.innerText =
                    raw.value.innerText.slice(0, end)
                    + '\t'
                    + raw.value.innerText.slice(end);
                markdownStore.updateLine(props.id, props.lineNum, raw.value.innerText);
                await updateLineAsync()
                const rangePos = end + 1
                handleFocus(rangePos)
            }
            break;
        case 'Backspace':
            if (raw.value) {
                let s = false;
                if (selection) {
                    const a = selection.anchorOffset;
                    const f = selection.focusOffset;
                    s = Math.abs(a - f) == raw.value?.innerText.length && a !== f;
                }
                if (raw.value?.innerText.length === 1 && s) {
                    const newValue = "";
                    raw.value.innerText = newValue;
                    markdownStore.updateLine(props.id, props.lineNum, newValue);
                    await updateLineAsync()
                    e.preventDefault();
                } else if (raw.value?.innerText.length === 0) {
                    e.preventDefault();
                    markdownStore.deleteLine(props.id, props.lineNum);
                    await updateLineAsync()
                } else if (selection) {
                    if (selection.anchorOffset == 0) {
                        e.preventDefault();
                        const data = raw.value.innerText!
                        markdownStore.combineLine(props.id, props.lineNum, data);
                        await updateLineAsync()
                    }
                }
                if (block.value?.tag === BlockTag.CodeBlock
                    || block.value?.tag === BlockTag.MathBlock && selection) {
                    const oldRange = selection!.getRangeAt(0);
                    handleFocus(oldRange.startOffset)
                }
            }
            break;
        case 'ArrowUp':
            if ((block.value?.tag === BlockTag.CodeBlock
                || block.value?.tag === BlockTag.MathBlock)
                && selection?.anchorOffset != 0) {
                break;
            } else if (e.shiftKey) {
                if (raw.value && raw.value.firstChild && selection) {
                    const oldRange = selection.getRangeAt(0);
                    const range = document.createRange();
                    const rangePos = oldRange.startOffset;
                    range.setStartAfter(raw.value.firstChild)
                    range.setEnd(raw.value.firstChild, rangePos)
                    selection?.removeAllRanges();
                    selection?.addRange(range);
                }
            } else {
                e.preventDefault()
                emits('upLine', props.lineNum);
            }
            break;
        case 'ArrowDown':
            if ((block.value?.tag === BlockTag.CodeBlock
                || block.value?.tag === BlockTag.MathBlock)
                && selection?.focusOffset != (raw.value?.innerText.length!)) {
                break;
            } else if (e.shiftKey) {
                if (raw.value && raw.value.firstChild && selection) {
                    const oldRange = selection.getRangeAt(0);
                    const range = document.createRange();
                    const rangePos = oldRange.startOffset;
                    range.setStart(raw.value.firstChild, rangePos)
                    range.setEndAfter(raw.value.firstChild)
                    selection?.removeAllRanges();
                    selection?.addRange(range);
                }
            } else {
                e.preventDefault()
                emits('downLine', props.lineNum);
            }
            break;
    }
}

async function handlePasteAsync(event: ClipboardEvent) {
    event.preventDefault();
    if (event.clipboardData?.types.includes('text/plain')) {
        const selection = window.getSelection();
        const focusOffset = selection?.focusOffset;
        const remainData = splitData.value.slice(0, focusOffset)
        const sliceData = splitData.value.slice(focusOffset)
        const parseData = event.clipboardData.getData('text/plain')
        const r = markdownStore.paste(props.id, props.lineNum, parseData, remainData, sliceData)
        if (r) {
            splitData.value = markdownStore.getSplitData(props.id, props.lineNum)!
            await loadAsync(splitData.value)
        }
    }
}

function handleFocus(pos: number) {
    const range = document.createRange();
    const selection = window.getSelection();
    window.setTimeout(() => {
        raw.value?.focus()
        if (raw.value?.firstChild) {
            var rangePos
            if (raw.value.innerText.length > pos)
                rangePos = pos
            else
                rangePos = raw.value.innerText.length
            range.setEnd(raw.value.firstChild, rangePos)
            range.collapse();
            selection?.removeAllRanges();
            selection?.addRange(range);
        } else {
            range.setEnd(raw.value!.parentNode!.childNodes[1], 0)
            range.collapse();
            selection?.removeAllRanges();
            selection?.addRange(range);
        }
    }, 0)
}

function handleFocusEnd() {
    const range = document.createRange();
    const selection = window.getSelection();
    window.setTimeout(() => {
        raw.value?.focus()
        if (raw.value?.firstChild) {
            const rangePos = raw.value?.innerText.length!;
            range.setEnd(raw.value.firstChild, rangePos)
            range.collapse();
            selection?.removeAllRanges();
            selection?.addRange(range);
        } else {
            range.setEnd(raw.value!.parentNode!.childNodes[1], 0)
            range.collapse();
            selection?.removeAllRanges();
            selection?.addRange(range);
        }
    }, 0)
}

function handleFocusStart() {
    const range = document.createRange();
    const selection = window.getSelection();
    window.setTimeout(() => {
        raw.value?.focus()
        if (raw.value?.firstChild) {
            range.setEnd(raw.value.firstChild, 0)
            range.collapse();
            selection?.removeAllRanges();
            selection?.addRange(range);
        } else {
            range.setEnd(raw.value!.parentNode!.childNodes[1], 0)
            range.collapse();
            selection?.removeAllRanges();
            selection?.addRange(range);
        }
    }, 0)
}

function calcuateClass(block: Block): string {
    switch (block.tag) {
        case BlockTag.Title:
            return (block.content as Title).level.toString()
        default:
            return block.tag.toString()
    }
}

function calcuateInline(tag: BlockTag): boolean {
    const target = [BlockTag.CodeBlock, BlockTag.MathBlock, BlockTag.Line, BlockTag.Image];
    return !target.includes(tag)
}

function calcuateMargin(level: number): string {
    const margin = level * 18;
    return `margin-left: ${margin}px;`
}

function calcuateRows(): number {
    const l = Math.min(splitData.value.length / 100, 10)
    return Math.max(l, 4)
}

async function getImage(url: string | undefined): Promise<string> {
    if (url) {
        if (url.startsWith("res://")) {
            const newUrl = await ResourceApi.getBlobUrl(url.slice(6))
            return newUrl
        } else {
            return url
        }
    } else {
        return ''
    }
}

async function loadAsync(rawData: string) {
    const data = await serializeAsync(rawData)
    block.value = data
    nextTick(async () => {
        if (data.tag === BlockTag.MathBlock && math.value) {
            katex.render((data.content as string).replace(/[\t\r\f\n]*/g, ""), math.value, {
                throwOnError: false, output: "html", errorColor: "#cc4d4d", displayMode: true
            })
        } else if (data.tag === BlockTag.Image) {
            src.value = await getImage((data.content as Image).src)
        }
    })
}

async function updateLineAsync() {
    const data = markdownStore.getSplitData(props.id, props.lineNum)
    if (data != undefined) {
        splitData.value = data
        await loadAsync(splitData.value)
    }
}

onMounted(async () => {
    if (markdownStore.existLine(props.id, props.lineNum)) {
        await updateLineAsync()
    }
})
</script>

<template>
    <div v-if="block" class="md-block" :class="{ 'highlight': props.isHighlight }" @dblclick="handleEdit()"
        @touchstart="handleTouchEdit" :id="`md-block-${props.lineNum}`">
        <span v-show="isEdit || props.isHighlight" class="line-num" :class="{ 'focus-num': isEdit }">
            {{ props.lineNum }}
        </span>
        <span v-show="isEdit" class="edit" ref="raw" @focusout="isEdit = false" @keydown="handleBehaviorAsync"
            @paste="handlePasteAsync" @input="handleInputAsync()"
            :class="[calcuateClass(block), isEdit ? 'focus-line' : '']" contenteditable="true">
            {{ splitData }}
        </span>
        <span v-show="!isEdit" class="render" :class="{ 'inline': calcuateInline(block.tag) }">
            <span v-if="block.tag === BlockTag.Title" class="title" :class="(block.content as Title).level"
                :id="`md-title-${$props.lineNum}`">
                <span class="title-tip">{{ (block.content as Title).level }}</span>
                <MdParagraph :paragraph="(block.content as Title).content"></MdParagraph>
            </span>
            <span v-else-if="block.tag === BlockTag.Paragraph" class="paragraph">
                <MdParagraph :paragraph="(block.content as Paragraph)"></MdParagraph>
            </span>
            <span v-else-if="block.tag === BlockTag.Quote" class="quote">
                <span class="quote-tip">
                    <font-awesome-icon :icon="['fas', 'quote-left']" />
                </span>
                <MdParagraph :paragraph="(block.content as Paragraph)"></MdParagraph>
            </span>
            <span v-else-if="block.tag === BlockTag.ListItem" class="list-item">
                <span class="list-tip" :style="calcuateMargin((block.content as ListItem).level)">
                    <font-awesome-icon v-if="!(block.content as ListItem).index && (block.content as ListItem).index !== 0"
                        style="margin-right: 4px;" :icon="['fas', 'chevron-right']" />
                    <span v-else>
                        {{ (block.content as ListItem).index }}
                    </span>
                </span>
                <MdParagraph :paragraph="(block.content as ListItem).content"></MdParagraph>
            </span>
            <div v-else-if="block.tag === BlockTag.Image" class="image">
                <el-image :src="src" :alt="(block.content as Image).title" fit="contain" />
                <div class="image-title">{{ (block.content as Image).title }}</div>
            </div>
            <span v-else-if="block.tag === BlockTag.TodoItem" class="todo-item">
                <span class="todo-tip">
                    <font-awesome-icon
                        :icon="['fas', (block.content as TodoItem).is_finished ? 'square-check' : 'square']" />
                </span>
                <MdParagraph :paragraph="(block.content as TodoItem).content"></MdParagraph>
            </span>
            <span v-else-if="block.tag === BlockTag.Footer" class="footer" :id="(block.content as Footer).index">
                <span class="footer-tip">
                    <font-awesome-icon :icon="['fas', 'bookmark']" />
                    <span>
                        {{ (block.content as Footer).index }}
                    </span>
                </span>
                <MdParagraph :paragraph="(block.content as Footer).content"></MdParagraph>
            </span>
            <div v-else-if="block.tag === BlockTag.Line" class="line" />
            <div v-else-if="block.tag === BlockTag.CodeBlock" class="multi-block code-block">
                <span class="code-tip">
                    <font-awesome-icon :icon="['fas', 'code']" />
                    {{ (block.content as [string, string])[0] }}
                </span>
                <div class="code">
                    {{ (block.content as [string, string])[1] }}
                </div>
            </div>
            <div v-else-if="block.tag === BlockTag.MathBlock" class="multi-block">
                <span class="math-tip">
                    <font-awesome-icon :icon="['fas', 'infinity']" />
                </span>
                <div class="math" ref="math" />
            </div>
            <span v-else-if="block.tag === BlockTag.Error" class="error">
                <span class="error-tip">
                    err
                </span>
                <span>
                    {{ block.content as string }}
                </span>
            </span>
        </span>
    </div>
    <el-skeleton v-else :rows="calcuateRows()" class="md-block-skeleton" animated />
</template>

<style scoped>
.md-block {
    max-width: 90%;
    outline: none;
    position: relative;
    font-size: 18px;
    margin: 5px;
    margin-left: 12px;
    margin-right: 12px;
    word-break: break-all;
}

.md-block.highlight .edit {
    border: 2px solid #409eff;
}

.md-block.highlight .line-num {
    color: #409eff;
}

.md-block-skeleton {
    max-width: 95%;
    outline: none;
    position: relative;
    margin: 20px auto;
    cursor: wait;
}

.line-num {
    user-select: none;
    font-size: 13px;
    font-weight: 1000;
    color: #aaaaaa;
    position: absolute;
    font-family: Arial, Helvetica, sans-serif;
}

.line-num.focus-num {
    color: #4D78CC;
}

.md-block .edit.focus-line {
    background-color: #f7f7f7;
}

.md-block .edit {
    outline: none;
    display: inline-block;
    white-space: pre-wrap;
    margin-left: 5%;
    width: 100%;
    caret-color: #4D78CC;
}

.md-block .edit::selection {
    background-color: #e7e7e7;
    color: #4D78CC;
}

.md-block .edit.Line {
    font-size: 19px;
}

.md-block .edit.CodeBlock {
    white-space: pre-wrap;
    font-family: var(--code-font);
    margin-top: 22px;
    margin-bottom: 15px;
}

.md-block .edit.MathBlock {
    white-space: pre-wrap;
    font-family: var(--code-font);
    margin-top: 22px;
    margin-bottom: 15px;
}

.md-block .title {
    font-weight: bold;
}

.md-block .H1 {
    font-size: 40px;
}

.md-block .H2 {
    font-size: 36px;
}

.md-block .H3 {
    font-size: 32px;
}

.md-block .H4 {
    font-size: 28px;
}

.md-block .H5 {
    font-size: 24px;
}

.md-block .H6 {
    font-size: 20px;
}

.md-block .render {
    user-select: none;
    margin-left: 5%;
}

.md-block .render.inline {
    display: inline-block;
}

.md-block .render .title-tip {
    vertical-align: text-top;
    font-size: 13px;
    font-weight: 1000;
    color: #4D78CC;
    font-family: Arial, Helvetica, sans-serif;
}

.md-block .render .error-tip {
    vertical-align: text-top;
    font-size: 13px;
    font-weight: 1000;
    color: rgb(204, 77, 77);
    font-family: Arial, Helvetica, sans-serif;
}

.md-block .render .list-tip {
    color: #4D78CC;
}

.md-block .render .list-tip span {
    margin-right: 8px;
    font-weight: 1000;
    font-family: Arial, Helvetica, sans-serif;
}

.md-block .render .quote {
    color: #777;
}

.md-block .render .quote-tip {
    margin-right: 4px;
}

.md-block .render .todo-tip {
    color: #cc864d;
}

.md-block .render .footer-tip {
    color: #24af34;
}

.md-block .render .footer-tip span {
    margin-left: 6px;
    margin-right: 6px;
}

.md-block .render .paragraph {
    margin-left: 2em;
}

.md-block .render .line {
    height: 2px;
    width: 90%;
    background-color: #d0d0d0;
    margin: 0 auto;
}

.md-block .render .image {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.md-block .render .image-title {
    font-size: 16px;
    font-weight: 500;
    color: #525d6e;
}

.md-block .render .multi-block {
    white-space: pre-wrap;
    width: 100%;
    margin-left: 5%;
    background-color: #f5f5f5;
    border-radius: 5px;
    padding-bottom: 10px;
    padding-top: 3px;
}

.md-block .render .math {
    margin-left: 18px;
    margin-right: 18px;
    margin-top: 0px;
}

.md-block .render .math-tip {
    margin-left: 10px;
    color: #4D78CC;
    font-size: 18px;
}

.md-block .render .code-block {
    font-family: var(--code-font);
}

.md-block .render .code-block .code {
    margin: 12px 18px;
}

.md-block .render .code-tip {
    margin-left: 10px;
    color: #4D78CC;
    font-size: 18px;
    text-transform: capitalize;
}
</style>