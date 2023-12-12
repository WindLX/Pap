<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import katex from "katex";
import { ElPopover, ElNotification, ElScrollbar } from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import type { FooterIndex, Link, Paragraph, Text, Sentence } from '@/md/mdexpr';
import { SentenceTag } from '@/md/mdexpr';
import type { EmojiSchema } from '@/schemas/emoji';
import { EmojiApi } from '@/api/emoji';
import { NoteApi } from '@/api/note';
import { useNoteTabStore } from '@/store/tab';
import MdLinkExtend from './MdLinkExtend.vue';

const props = defineProps<{
    paragraph: Paragraph
}>();

const tabStore = useNoteTabStore()
const span = ref<Array<HTMLSpanElement>>()
let emoji_fail = false;
let emojis = ref<Array<EmojiSchema>>([])
let isLinkExtendShow = ref(false)

function isExtend(link: Link): boolean {
    return link.href !== undefined && link.href.startsWith("res://")
}

function jump(id: string) {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" })
}

async function newJump(href: string | undefined) {
    if (href) {
        if (href.startsWith("md://")) {
            const note = await NoteApi.getNoteByName(href.slice(5))
            if (note) {
                tabStore.addTab(note)
            }
        } else if (href.startsWith("res://")) {
            isLinkExtendShow.value = !isLinkExtendShow.value
        }
        else {
            window.open(href, "_blank")
        }
    } else {
        ElNotification({
            title: '跳转失败',
            message: '不存在的链接',
            type: 'error',
            duration: 2000
        })
    }
}

async function getEmojiAsync(emoji: string): Promise<Array<EmojiSchema>> {
    try {
        const emojis = await EmojiApi.getEmoji(emoji)
        return emojis.map(e => {
            const unicodeArray = e.unicode.split(' ');
            const htmlEntities = unicodeArray.map(code => '&#x' + code.slice(2) + ';');
            return { unicode: htmlEntities.join(''), name: e.name }
        })
    } catch (e) {
        if (!emoji_fail && (e as Response).status == 406) {
            emoji_fail = true;
            return [{ unicode: "&#x2757;", name: "failtoload" }]
        } else {
            return [{ unicode: "&#x2753;", name: "failtoload" }]
        }
    }
}

async function renderAsync() {
    props.paragraph.map(async (sentence: Sentence, index: number, _) => {
        if (span.value && span.value[index]) {
            if (sentence.tag === SentenceTag.Math) {
                await Promise.resolve(katex.render((sentence.content as string).replace(/[\t\r\f\n]*/g, ""), span.value[index].children[0] as HTMLSpanElement, {
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
}

watch(props, async () => {
    await renderAsync()
})

onMounted(async () => {
    await renderAsync()
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
        <span v-else-if="sentence.tag === SentenceTag.Link" class="link ref">
            <span class="content" @click="newJump((sentence.content as Link).href)">
                {{ (sentence.content as Link).content }}
            </span>
            <font-awesome-icon class="super" :icon="['fas', 'link']" />
            <MdLinkExtend v-show="isLinkExtendShow" v-if="isExtend(sentence.content as Link)"
                :link="((sentence.content) as Link)" />
        </span>
        <span v-else-if="sentence.tag === SentenceTag.Code" class="code">
            {{ sentence.content as string }}
        </span>
        <span v-else-if="sentence.tag === SentenceTag.Math" class="math" />
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
        <span v-else-if="sentence.tag === SentenceTag.FooterIndex" class="footer-index ref"
            @click="jump((sentence.content as FooterIndex))">
            <span>
                {{ (sentence.content as FooterIndex) }}
            </span>
            <font-awesome-icon class=" super" :icon="['fas', 'bookmark']" />
        </span>
    </span>
</template>

<style scoped>
.sentence {
    white-space: pre-wrap;
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
    font-family: var(--code-font);
}

.sentence .link {
    color: #4D78CC;
}

.sentence .footer-index {
    color: #24af34;
}

.sentence .ref .content {
    cursor: pointer;
}

.sentence .ref:hover .content {
    text-decoration: underline;
}
</style>