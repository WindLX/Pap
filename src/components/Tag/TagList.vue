<script lang="ts" setup>
import { nextTick, ref, onActivated, onMounted } from 'vue'
import {
    ElButtonGroup, ElButton, ElInput,
    ElColorPicker
} from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { useTagStore, TagEvent } from '@/store/tag';
import { predefineColors } from '@/schemas/tag';
import type { TagSchema } from '@/schemas/tag';
import { TagApi } from '@/api/tag';
import Tag from './Tag.vue';

const props = defineProps<{
    id: number
}>()

const tagStore = useTagStore()

tagStore.$onAction(
    ({
        name: name,
        after: after,
    }) => {
        after((result) => {
            switch (name) {
                case "onUpdate":
                    loadTagsAsync()
                    break;
                case "onChoose":
                    const e = result as TagEvent
                    if (e.filterId === props.id) {
                        handleAddTagAsync(result as TagEvent)
                    }
                    break;
            }
        })
    }
)

// style data
const inputVisible = ref(false)

// componment ref
const InputRef = ref<InstanceType<typeof ElInput>>()
const ColorRef = ref<InstanceType<typeof ElColorPicker>>()

// data
const inputValue = ref('')
const colorValue = ref('#409EFF')
let dynamicTags = ref<Array<TagSchema>>([])

async function handleCloseAsync(tagId: number) {
    await TagApi.removeTag(tagId, props.id)
    dynamicTags.value.splice(dynamicTags.value.findIndex((t) => t.id === tagId), 1)
    tagStore.onUpdate()
}

async function handleInputConfirmAsync() {
    if (inputValue) {
        const tagCreateData = {
            name: inputValue.value,
            color: colorValue.value,
            note_id: props.id
        }
        const data = await TagApi.createTag(tagCreateData)
        dynamicTags.value.push(data)
        tagStore.onUpdate()
        handleInputCancel()
    }
}

async function handleAddTagAsync(tag: TagEvent) {
    const data = await TagApi.addTag(tag.tag.id, props.id)
    dynamicTags.value = data.tags
    tagStore.onUpdate()
    handleInputCancel()
}

function handleInputCancel() {
    inputVisible.value = false
    inputValue.value = ''
}

function handleShowTag() {
    tagStore.setFilterShow(props.id)
}

function handleShowInput() {
    inputVisible.value = true
    nextTick(() => {
        ColorRef.value?.show()
    })
}

async function loadTagsAsync() {
    dynamicTags.value = await TagApi.getNoteTags(props.id)
}

onMounted(async () => {
    await loadTagsAsync()
})

onActivated(async () => {
    await loadTagsAsync()
})
</script>

<template>
    <div class="tag-list">
        <tag v-for="tag in dynamicTags" :key="tag.id" :color="tag.color" closable :disable="false"
            @close="handleCloseAsync(tag.id)">
            {{ tag.name }}
        </tag>
        <span>
            <el-input v-if="inputVisible" ref="InputRef" v-model="inputValue" class="item" size="small"
                style="width: 48px;">
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
        </span>
    </div>
</template>

<style scoped>
.tag-list {
    z-index: 50;
    position: absolute;
    display: flex;
    margin: auto;
    flex-wrap: wrap;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    padding: 4px;
}

.tag-list .item {
    margin: 3px;
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
</style>