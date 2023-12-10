<script setup lang="ts">
import { ReactiveVariable } from 'vue/macros';
import { ref, Ref, onMounted, reactive, computed, ComputedRef } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
    ElButton, ElDrawer, ElInput, ElColorPicker, ElDialog,
    ElCollapse, ElCollapseItem, ElForm, ElFormItem,
    ElButtonGroup, ElPopconfirm
} from 'element-plus';
import Tag from './Tag.vue';
import { useTagStore } from '@/store/tag';
import { TagApi } from '@/api/tag';
import { tagDefault, predefineColors } from '@/schemas/tag';
import type { TagSchema, TagRelationshipSchema } from '@/schemas/tag';

// state
const tagStore = useTagStore()

// style
const show = ref(tagStore.show)
const editable = ref(tagStore.editable)
const filterId = ref(tagStore.filterId)
const inputVisible = ref(false)
const chooseVisible = ref(false)

tagStore.$subscribe((_mutation, state) => {
    show.value = state.show
    editable.value = state.editable
    filterId.value = state.filterId
})

tagStore.$onAction(
    ({
        after: after,
    }) => {
        after(() => {
            loadAllTagsAsync()
        })
    }
)

// data
let allTags: Ref<Array<TagRelationshipSchema>> = ref([])
let filterTags: ComputedRef<Array<TagRelationshipSchema>> = computed(() => {
    if (inputValue.value !== '')
        return allTags.value.filter((t) => {
            const target = t.name
            const source = inputValue.value
            const regex = new RegExp(source, 'i');
            return regex.test(target)
        })
    else
        return allTags.value
})
let targetTag: ReactiveVariable<TagSchema> = reactive(tagDefault())
let inputValue: Ref<string> = ref("")

// callback function
async function handleUpdateConfirmAsync() {
    if (targetTag) {
        const tagUpdateData = {
            name: targetTag.name,
            color: targetTag.color,
            id: targetTag.id
        }
        const data = await TagApi.updateTag(tagUpdateData)
        const index = allTags.value.findIndex((t) => { return t.id === data.id })
        allTags.value[index] = data
        tagStore.onUpdate()
    }
    handleUpdateCancel()
}

function handleUpdateCancel() {
    inputVisible.value = false
    targetTag = tagDefault()
}

function handleShowEditDialog(tag: TagRelationshipSchema) {
    inputVisible.value = true;
    targetTag = tag
}

function handleShowChooseDialog(tag: TagRelationshipSchema) {
    chooseVisible.value = true;
    targetTag = tag
}

function handleChooseCancel() {
    chooseVisible.value = false
    targetTag = tagDefault()
}

function handleChooseConfirm() {
    const chooseTagData = {
        name: targetTag.name,
        color: targetTag.color,
        id: targetTag.id
    }
    tagStore.onChoose(chooseTagData)
    chooseVisible.value = false
    targetTag = tagDefault()
}

async function handleDeleteTagAsync(tagId: number) {
    await TagApi.deleteTag(tagId)
    // await loadAllTagsAsync()
    tagStore.onUpdate()
}

async function handleRemoveNoteAsync(tagId: number, resourceItemId: number) {
    await TagApi.removeTag(tagId, resourceItemId)
    // await loadAllTagsAsync()
    tagStore.onUpdate()
}

function handleClose() {
    tagStore.setDefault()
}

// load function
async function loadAllTagsAsync() {
    allTags.value = await TagApi.getTags()
}

function isChoosable(id: number) {
    const tag = allTags.value.find((t) => { return t.id === id })
    if (tag !== undefined) {
        const item = tag.notes.find((r) => { return r.id === filterId.value })
        if (item !== undefined) return false
        else return true
    } else return true
}

// hook
onMounted(() => {
    loadAllTagsAsync()
})
</script>

<template>
    <el-drawer v-model="show" direction="btt" :size="'80%'" @close="handleClose">
        <template #header>
            <div style="display: flex; align-items: center;">
                <font-awesome-icon :icon="['fas', 'tag']" class="icon" />
                <h4 style="margin-left: 10px;">标签集</h4>
            </div>
        </template>
        <template #default>
            <el-input v-model="inputValue" clearable placeholder="查找" />
            <el-collapse>
                <el-collapse-item v-for="tag in filterTags" :key="tag.id" :name="tag.id">
                    <template #title>
                        <tag :color="tag.color" :closable="false" :disable="!isChoosable(tag.id)">
                            {{ tag.name }}
                        </tag>
                    </template>
                    <template #default>
                        <el-button-group style="margin-bottom: 12px; margin-left: 2px;">
                            <el-button size="small" @click="handleShowChooseDialog(tag)" class="button"
                                :disabled="!isChoosable(tag.id)">
                                <font-awesome-icon :icon="['fas', 'hand']" class="icon" />
                            </el-button>
                            <el-button size="small" @click="handleShowEditDialog(tag)" class="button" :disabled="!editable">
                                <font-awesome-icon :icon="['fas', 'pen']" class="icon" />
                            </el-button>
                            <el-popconfirm title="确认删除此标签吗?" confirm-button-text="确认" cancel-button-text="取消"
                                @confirm="handleDeleteTagAsync(tag.id)" :hide-after="0">
                                <template #reference>
                                    <el-button size="small" class="button" :disabled="!editable">
                                        <font-awesome-icon :icon="['fas', 'trash-can']" class="icon" />
                                    </el-button>
                                </template>
                            </el-popconfirm>
                        </el-button-group>
                        <span v-for="resource in tag.notes" class="tag-container">
                            <span class="tag-drawer">
                                <font-awesome-icon :icon="['fas', 'file']" class="icon" />
                                {{ resource.name }}
                            </span>
                            <el-popconfirm title="确认删除此笔记与此标签的关联吗?" confirm-button-text="确认" cancel-button-text="取消"
                                @confirm="handleRemoveNoteAsync(tag.id, resource.id)" :hide-after="0">
                                <template #reference>
                                    <el-button size="small" :disabled="!editable">
                                        <font-awesome-icon :icon="['fas', 'trash-can']" class="icon" />
                                    </el-button>
                                </template>
                            </el-popconfirm>
                        </span>
                    </template>
                </el-collapse-item>
            </el-collapse>
        </template>
    </el-drawer>
    <el-dialog v-model="inputVisible" title="修改标签" width="30%">
        <el-form class="tag-new" :form="targetTag">
            <el-form-item label="名称">
                <el-input v-model="targetTag.name">
                </el-input>
            </el-form-item>
            <el-form-item label="颜色">
                <el-color-picker v-model="targetTag.color" :predefine="predefineColors" />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button size="small" @click="handleUpdateCancel" class="button">
                    <font-awesome-icon :icon="['fas', 'xmark']" class="icon" />
                    <span style="margin-left: 8px;">
                        取消
                    </span>
                </el-button>
                <el-button size="small" type="primary" @click="handleUpdateConfirmAsync" class="button">
                    <font-awesome-icon :icon="['fas', 'check']" class="icon" />
                    <span style="margin-left: 8px;">
                        确认
                    </span>
                </el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog v-model="chooseVisible" title="提示" width="30%">
        <div style="display: flex; align-items: center; flex-direction: column;">
            <tag :color="targetTag?.color" :closable="false" :disable="false">
                {{ targetTag?.name }}
            </tag>
            <span style="margin: 12px;">确定选择此标签吗</span>
        </div>
        <template #footer>
            <span>
                <el-button @click="handleChooseCancel">
                    取消
                </el-button>
                <el-button type="primary" @click="handleChooseConfirm">
                    确认
                </el-button>
            </span>
        </template>
    </el-dialog>
</template>

<style scoped>
.tag {
    border-width: 0;
}

.tag-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-left: 24px;
    margin-right: 32px;
}

.tag-new {
    display: flex;
    flex-direction: column;
}

.tag-drawer {
    display: flex;
    align-items: center;
    font-size: 16px;
}

.tag-drawer .icon {
    margin-right: 8px;
    color: #6d6d6d;
}

.item {
    margin: 0 3px;
    height: 24px;
    min-width: 32px;
    width: fit-content;
}

#group {
    width: 84px;
}
</style>

<style>
.el-drawer__header {
    margin-bottom: 0;
}
</style>