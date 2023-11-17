<script setup lang="ts">
import { ref, watch } from 'vue';
import katex from "katex";
import type { FooterIndex, Link, Paragraph, Text } from '../types/mdexpr-types';
import { SentenceTag, Sentence } from '../types/mdexpr-types';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { ElPopover, ElButton, ElNotification } from 'element-plus';

const props = defineProps<{
    paragraph: Paragraph
}>();

const math = ref<Array<HTMLSpanElement>>();

function jump(id: string) {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" })
}

function newJump(href: string | undefined) {
    if (href) {
        window.open(href, "_blank");
    } else {
        ElNotification({
            title: '跳转失败',
            message: '不存在的链接',
            type: 'error',
            duration: 2000
        })
    }
}

watch(props, async () => {
    props.paragraph.map((sentence: Sentence, index: number, _) => {
        if (sentence.tag === SentenceTag.Math && math.value && math.value[index]) {
            katex.render((sentence.content as string).replace(/[\t\r\f\n]*/g, ""), math.value[index].children[0] as HTMLDivElement, {
                throwOnError: false, output: "html", errorColor: "#cc4d4d"
            })
        }
    })
})
</script>

<template>
    <span v-for="(sentence, index) in (props.paragraph)" :key="index" class="sentence" ref="math">
        <span v-if="sentence.tag === SentenceTag.Text" class="text" :class="{
            'bold': (sentence.content as Text).is_bold,
            'italic': (sentence.content as Text).is_italic,
            'strike': (sentence.content as Text).is_strike
        }">
            {{ (sentence.content as Text).content }}
        </span>
        <span v-else-if="sentence.tag === SentenceTag.Link" class="link">
            <el-popover placement="top-start" trigger="hover" :title="(sentence.content as Link).href">
                <div style="text-align: center; margin: 0">
                    <el-button size="small" type="primary" @click="newJump((sentence.content as Link).href)">Go!</el-button>
                </div>
                <template #reference>
                    <span>
                        <span>
                            {{ (sentence.content as Link).content }}
                        </span>
                        <font-awesome-icon class="super" :icon="['fas', 'link']" />
                    </span>
                </template>
            </el-popover>
        </span>
        <span v-else-if="sentence.tag === SentenceTag.Code" class="code">
            {{ sentence.content as string }}
        </span>
        <div v-else-if="sentence.tag === SentenceTag.Math" class="math">
        </div>
        <span v-else-if="sentence.tag === SentenceTag.Emoji" class="emoji"></span>
        <span v-else-if="sentence.tag === SentenceTag.FooterIndex" class="footer-index">
            <el-popover placement="top-start" trigger="hover" :title="(sentence.content as FooterIndex)">
                <div style="text-align: center; margin: 0">
                    <el-button size="small" type="primary" @click="jump((sentence.content as FooterIndex))">Go!</el-button>
                </div>
                <template #reference>
                    <span>
                        <span>
                            {{ (sentence.content as FooterIndex) }}
                        </span>
                        <font-awesome-icon class="super" :icon="['fas', 'bookmark']" />
                    </span>
                </template>
            </el-popover>
        </span>
    </span>
</template>

<style scoped>
.sentence {
    display: inline-block;
}


.sentence .super {
    font-size: 12px;
    vertical-align: super;
}

.sentence .bold {
    font-weight: bold;
}

.sentence .italic {
    font-style: italic;
}

.sentence .strike {
    text-decoration: line-through;
}

.sentence .code {
    margin: 0 2px;
    background-color: #ebebeb;
    border-radius: 5px;
    padding: 0 5px;
    color: #6D7D8D;
    font-family: 'Source Code Pro', 'Courier New', Courier, monospace;
}

.sentence .link {
    color: #4D78CC;
}

.sentence .footer-index {
    color: #24af34;
}
</style>