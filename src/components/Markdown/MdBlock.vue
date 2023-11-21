<script setup lang="ts">
import { JsGenerator } from "md_wasm";
import { Ref, nextTick, onMounted, ref, watch, inject } from 'vue';
import katex from "katex";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { ElImage, ElSkeleton } from "element-plus";
import MdParagraph from './MdParagraph.vue';
import type { Block, Paragraph, Title, ListItem, TodoItem, Footer, Image } from "../../types/mdexpr-types";
import { BlockTag } from "../../types/mdexpr-types";

const props = defineProps<{
    lineNum: number,
    rawData: string,
}>();

const emits = defineEmits<{
    (e: 'update:rawData', value: string): void,
    (e: 'appendLine', value: number, data: string): void;
    (e: 'deleteLine', value: number): void;
    (e: 'combineLine', value: number, data: string): void;
    (e: 'edit'): void;
    (e: 'upLine', value: number): void;
    (e: 'downLine', value: number): void;
}>()

defineExpose({
    focus: () => {
        isEdit.value = true;
        handleFocus()
    }
})

// data
const generator = JsGenerator.new();

const raw: Ref<HTMLSpanElement | null> = ref(null);
const math: Ref<HTMLDivElement | null> = ref(null);
let isEdit = ref(false);
let block: Ref<Block | null> = ref(null)
const lock = inject<Ref<boolean>>('lockState')

async function serializeAsync(rawData: string): Promise<Block> {
    try {
        const result = generator.serialize(rawData);
        return Promise.resolve(result);
    } catch (_e) {
        // console.log(_e)
        return Promise.resolve({
            tag: BlockTag.Error,
            content: rawData
        });
    }
}

function handleInput() {
    if (raw.value) {
        emits('update:rawData', raw.value.innerText);
    }
}

function handleEdit() {
    if (!lock?.value) {
        isEdit.value = true;
        handleFocus();
    }
}

function behaviorHandler(e: KeyboardEvent) {
    const selection = window.getSelection();
    const focusOffset = selection?.focusOffset;
    switch (e.key) {
        case 'Enter':
            e.preventDefault();
            if ((block.value?.tag === BlockTag.CodeBlock
                || block.value?.tag === BlockTag.MathBlock)
                && focusOffset !== raw.value?.innerText.length) {
                selection?.getRangeAt(0).insertNode(document.createTextNode('\n'));
                emits('update:rawData', raw.value?.innerText!);
                let pos = selection?.getRangeAt(0).startOffset;
                nextTick(async () => {
                    const range = document.createRange();
                    if (raw.value?.firstChild && pos) {
                        range.setStart(raw.value.firstChild, 0)
                        range.setEnd(raw.value.firstChild, pos + 1)
                        range.collapse(false);
                        selection?.removeAllRanges();
                        selection?.addRange(range);
                    }
                })
            } else {
                const remainData = props.rawData.slice(0, focusOffset)
                const sliceData = props.rawData.slice(focusOffset)
                emits('update:rawData', remainData);
                emits('appendLine', props.lineNum, sliceData);
            }
            break;
        case 'Tab':
            e.preventDefault();
            if (raw.value && selection) {
                const oldRange = selection.getRangeAt(0);
                oldRange.insertNode(document.createTextNode('\t'));
                emits('update:rawData', raw.value.innerText);
                const pos = oldRange.startOffset + 1;
                raw.value?.focus();
                const range = document.createRange();
                if (raw.value?.firstChild) {
                    range.setEnd(raw.value.firstChild, pos)
                    range.collapse();
                    selection?.removeAllRanges();
                    selection?.addRange(range);
                }
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
                if (raw.value?.innerText.length === 1 || s) {
                    const newValue = "";
                    raw.value.innerText = newValue;
                    emits('update:rawData', newValue);
                    e.preventDefault();
                } else if (raw.value?.innerText.length === 0) {
                    e.preventDefault();
                    emits('deleteLine', props.lineNum);
                } else if (selection) {
                    if (selection.anchorOffset == 0) {
                        e.preventDefault();
                        emits('combineLine', props.lineNum, raw.value?.innerText);
                    }
                }
            }
            break;
        case 'ArrowUp':
            if (block.value?.tag === BlockTag.CodeBlock && selection?.anchorOffset != 0) {
                break;
            } else {
                e.preventDefault()
                emits('upLine', props.lineNum);
            }
            break;
        case 'ArrowDown':
            if (block.value?.tag === BlockTag.CodeBlock && selection?.focusOffset != (raw.value?.innerText.length!)) {
                break;
            } else {
                e.preventDefault()
                emits('downLine', props.lineNum);
            }
            break;
    }
}

function handleFocus() {
    const range = document.createRange();
    const selection = window.getSelection();
    window.setTimeout(() => {
        raw.value?.focus();
        if (raw.value?.firstChild) {
            range.setEnd(raw.value.firstChild, raw.value.innerText.length)
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
    const target = [BlockTag.CodeBlock, BlockTag.MathBlock, BlockTag.Line];
    return !target.includes(tag)
}

function calcuateMargin(level: number): string {
    const margin = level * 18;
    return `margin-left: ${margin}px;`
}

function calcuateRows(): number {
    const l = Math.min(props.rawData.length / 100, 10)
    return Math.max(l, 4)
}

watch(props, async (newValue) => {
    block.value = await serializeAsync(newValue.rawData);
    if (block.value.tag === BlockTag.MathBlock && math.value) {
        katex.render((block.value.content as string).replace(/[\t\r\f\n]*/g, ""), math.value, {
            throwOnError: false, output: "html", errorColor: "#cc4d4d", displayMode: true
        })
    }
})

onMounted(async () => {
    block.value = await serializeAsync(props.rawData)
})
</script>

<template>
    <div v-if="block" class="md-block" @mousedown="handleEdit()">
        <span v-show="isEdit" class="line-num" :class="{ 'focus-num': isEdit }">
            {{ props.lineNum }}
        </span>
        <span v-show="isEdit" class="edit" ref="raw" @focusout="isEdit = false" @keydown="behaviorHandler"
            @input="handleInput()" :class="[calcuateClass(block), isEdit ? 'focus-line' : '']" contenteditable="true">
            {{ props.rawData }}
        </span>
        <span v-show="!isEdit" class="render" :class="{ 'inline': calcuateInline(block.tag) }">
            <span v-if="block.tag === BlockTag.Title" class="title" :class="(block.content as Title).level">
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
                    <font-awesome-icon v-if="!(block.content as ListItem).index" style="margin-right: 4px;"
                        :icon="['fas', 'circle-chevron-right']" />
                    <span v-else>
                        {{ (block.content as ListItem).index }}
                    </span>
                </span>
                <MdParagraph :paragraph="(block.content as ListItem).content"></MdParagraph>
            </span>
            <div v-else-if="block.tag === BlockTag.Image" class="image">
                <el-image :src="(block.content as Image).src" :alt="(block.content as Image).title" fit="contain" />
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
    font-family: 'Source Code Pro', 'Courier New', Courier, monospace;
    margin-top: 22px;
    margin-bottom: 15px;
    display: inline-block;
}

.md-block .edit.MathBlock {
    white-space: pre-wrap;
    font-family: 'Source Code Pro', 'Courier New', Courier, monospace;
    margin-top: 22px;
    margin-bottom: 15px;
    display: inline-block;
}

.md-block .H1 {
    font-size: 32px;
}

.md-block .H2 {
    font-size: 28px;
}

.md-block .H3 {
    font-size: 26px;
}

.md-block .H4 {
    font-size: 24px;
}

.md-block .H5 {
    font-size: 22px;
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
    font-family: 'Source Code Pro', 'Courier New', Courier, monospace;
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