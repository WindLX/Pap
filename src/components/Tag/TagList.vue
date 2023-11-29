<script lang="ts" setup>
import { nextTick, ref, Ref } from 'vue'
import {
    ElScrollbar, ElButtonGroup, ElButton, ElInput,
    ElColorPicker
} from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import type { ITag, IResourceItem } from '@/types/resource-types';
import type { TagEvent } from '@/types/event-types';
import { tag } from '@store';
import pFetch from '@/utils/fetch';
import Tag from './Tag.vue';

const props = defineProps<{
    isNote: boolean
    id: number
}>()

const tagStore = tag.useTagStore()

tagStore.$onAction(
    ({
        name: name,
        after: after,
    }) => {
        after((result) => {
            switch (name) {
                case "onUpdate":
                    loadResourceItemAsync()
                    break;
                case "onRemove":
                    loadResourceItemAsync()
                    break;
                case "onDelete":
                    loadResourceItemAsync()
                    break;
                case "onChoose":
                    const e = result as TagEvent
                    if (e.filterId === props.id) {
                        handleAddTagAsync(result as TagEvent)
                    }
                    break;
                default:
                    break;
            }
        })
    }
)

// const
const predefineColors = [
    '#ff4500',
    '#ff8c00',
    '#ffd700',
    '#90ee90',
    '#00ced1',
    '#409EFF',
    '#c71585'
]
const target = props.isNote ? "note_id" : "resource_item_id"

// style data
const inputVisible = ref(false)

// componment ref
const InputRef = ref<InstanceType<typeof ElInput>>()
const ColorRef = ref<InstanceType<typeof ElColorPicker>>()

// data
const inputValue = ref('')
const colorValue = ref('#409EFF')
let dynamicTags: Ref<Array<ITag>> = ref([])

async function loadResourceItemAsync() {
}

async function handleCloseAsync(tagId: number) {
    await pFetch(`/tag/remove_tag?tag_id=${tagId}&${target}=${props.id}`, {
        method: 'PUT',
        successCallback: async () => {
            dynamicTags.value.splice(dynamicTags.value.findIndex((t) => t.id === tagId), 1)
            tagStore.onRemove(tagId, props.id)
        }
    })
}

async function handleInputConfirmAsync() {
    if (inputValue) {
        const tagCreateData = {
            name: inputValue,
            color: colorValue,
            resource_item_id: props.id
        }
        await pFetch(`/tag/create_tag`, {
            method: 'POST',
            body: JSON.stringify(tagCreateData),
            successCallback: async (response) => {
                const data = await response.json()
                dynamicTags.value.push(data as ITag)
                tagStore.onCreate()
            }
        })
    }
    handleInputCancel()
}

async function handleAddTagAsync(tag: TagEvent) {
    await pFetch(`/tag/add_tag?tag_id=${tag.tag.id}&${target}=${props.id}`, {
        method: 'PUT',
        successCallback: async (response) => {
            const data = await response.json() as IResourceItem
            dynamicTags.value = data.tags
            tagStore.onAdd()
            handleInputCancel()
        }
    })
}

function handleInputCancel() {
    inputVisible.value = false
    inputValue.value = ''
}

function handleShowTag() {
    tagStore.show = true
    tagStore.editable = false
    tagStore.filterId = props.id
}

function handleShowInput() {
    inputVisible.value = true
    nextTick(() => {
        ColorRef.value?.show()
    })
}
</script>

<template>
    <div class="tag-list">
        <el-scrollbar>
            <div class="list">
                <tag v-for="tag in dynamicTags" :key="tag.id" :color="tag.color" closable :disable="false"
                    @close="handleCloseAsync(tag.id)">
                    {{ tag.name }}
                </tag>
            </div>
        </el-scrollbar>
        <el-input v-if="inputVisible" ref="InputRef" v-model="inputValue" class="item" size="small" style="width: 48px;">
        </el-input>
        <el-color-picker v-if="inputVisible" size="small" ref="ColorRef" v-model="colorValue"
            :predefine="predefineColors" />
        <el-button-group v-if="inputVisible" class="item" id="group">
            <el-button size="small" type="primary" @click="handleShowTag" class="button">
                <font-awesome-icon :icon="['fas', 'tag']" class="icon" />
            </el-button>
            <el-button size="small" type="primary" @click="handleInputConfirmAsync" class="button">
                <font-awesome-icon :icon="['fas', 'check']" class="icon" />
            </el-button>
            <el-button size="small" type="primary" @click="handleInputCancel" class="button">
                <font-awesome-icon :icon="['fas', 'xmark']" class="icon" />
            </el-button>
        </el-button-group>
        <el-button v-else class="item" size="small" @click="handleShowInput">
            + 新标签
        </el-button>
    </div>
</template>

<style scoped>
.tag-list {
    display: flex;
}

.tag-list .list {
    display: flex;
    margin-bottom: 18px;
    max-width: 50vw;
}

.tag-list .item {
    margin: 0 3px;
    height: 24px;
    min-width: 32px;
    width: fit-content;
}

.tag {
    border-width: 0;
}

.tag-list #group {
    width: 84px;
}

.tag-list .button {
    height: 24px;
    width: 28px;
}
</style>@/types/tag-types