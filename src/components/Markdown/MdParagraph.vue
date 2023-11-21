<script setup lang="ts">
import { ref, watch } from 'vue';
import katex from "katex";
import type { FooterIndex, Link, Paragraph, Text } from '../../types/mdexpr-types';
import { SentenceTag, Sentence } from '../../types/mdexpr-types';
import type { Emoji } from '../../types/emoji-types';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { ElPopover, ElButton, ElNotification, ElScrollbar } from 'element-plus';
import { state } from "@store";

const props = defineProps<{
    paragraph: Paragraph
}>();

const stateStore = state.useStateStore()

const span = ref<Array<HTMLSpanElement>>()

let emoji_fail = false;
let emojis = ref<Array<Emoji>>([])

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

async function getEmojiAsync(emoji: string): Promise<Array<Emoji>> {
    const response = await fetch(`${stateStore.backendHost}/emoji/get_emoji?emoji=${emoji}`, { method: 'GET', mode: 'cors' });
    if (response.status == 200) {
        const emoji = await response.json() as Array<Emoji>;
        return emoji.map(e => {
            const unicodeArray = e.unicode.split(' ');
            const htmlEntities = unicodeArray.map(code => '&#x' + code.slice(2) + ';');
            return { unicode: htmlEntities.join(''), name: e.name }
        });
    } else {
        if (!emoji_fail && response.status == 406) {
            emoji_fail = true;
            ElNotification({
                title: '渲染失败',
                message: 'emoji数据库加载失败',
                type: 'error',
                duration: 2000
            })
            return [{ unicode: "&#x2757;", name: "failtoload" }]
        } else {
            return [{ unicode: "&#x2753;", name: "failtoload" }]
        }
    }
}

watch(props, async () => {
    props.paragraph.map(async (sentence: Sentence, index: number, _) => {
        if (span.value && span.value[index]) {
            if (sentence.tag === SentenceTag.Math) {
                await Promise.resolve(katex.render((sentence.content as string).replace(/[\t\r\f\n]*/g, ""), span.value[index].children[0] as HTMLDivElement, {
                    throwOnError: false, output: "html", errorColor: "#cc4d4d"
                }))
            } else if (sentence.tag === SentenceTag.Emoji) {
                const emoji = await getEmojiAsync(sentence.content as string)
                span.value[index].getElementsByClassName("emoji")[0].innerHTML = emoji[0].unicode
                if (emoji[0].name !== "failtoload") {
                    emojis.value = emoji
                } else {
                    emojis.value = []
                }
            }
        }
    })
})
</script>

<template>
    <span v-for="(sentence, index) in (props.paragraph)" :key="index" class="sentence" ref="span">
        <span v-if="sentence.tag === SentenceTag.Text" class="text" :class="{
            'bold': (sentence.content as Text).is_bold,
            'italic': (sentence.content as Text).is_italic,
            'strike': (sentence.content as Text).is_strike
        }">
            {{ (sentence.content as Text).content }}
        </span>
        <span v-else-if="sentence.tag === SentenceTag.Link" class="link">
            <el-popover placement="bottom" trigger="hover" :title="(sentence.content as Link).href">
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
        <div v-else-if="sentence.tag === SentenceTag.Math" class="math" />
        <el-popover v-else-if="sentence.tag === SentenceTag.Emoji" :disabled="emojis.length <= 1" width="250"
            placement="bottom" trigger="hover">
            <el-scrollbar height="120">
                <div v-for="(emoji, index) in emojis" :key="index" class="emoji-tips">
                    <div v-html="emoji.unicode" style="margin-right: 10px" />
                    <div>{{ emoji.name }}</div>
                </div>
            </el-scrollbar>
            <template #reference>
                <span class="emoji" />
            </template>
        </el-popover>
        <span v-else-if="sentence.tag === SentenceTag.FooterIndex" class="footer-index">
            <el-popover placement="bottom" trigger="hover" :title="(sentence.content as FooterIndex)">
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
    display: inline;
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

.sentence .emoji {
    font-size: 0.8em;
}

.emoji-tips {
    display: flex;
    flex-direction: row;
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