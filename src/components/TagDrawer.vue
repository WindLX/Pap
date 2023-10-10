<script setup lang="ts">
import { ReactiveVariable } from 'vue/macros';
import { ref, Ref, onMounted, reactive, computed, ComputedRef } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
    ElButton, ElDrawer, ElInput, ElColorPicker, ElDialog,
    ElNotification, ElCollapse, ElCollapseItem, ElForm, ElFormItem,
    ElButtonGroup, ElPopconfirm
} from 'element-plus';
import { ITag, ITagRelationship } from 'resource-types';
import Tag from './Tag.vue';
import { useStateStore } from '../store/state';
import { useTagStore } from '../store/tag';

// state
const stateStore = useStateStore()
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
        name: name,
        after: after,
    }) => {
        after(() => {
            switch (name) {
                case "onCreate":
                    loadAllTags()
                    break;
                case "onAdd":
                    loadAllTags()
                    break;
                case "onRemove":
                    loadAllTags()
                    break;
                default:
                    break;
            }
        })
    }
)
// const
const defaultTag = {
    id: -1,
    name: "",
    color: "#409EFF"
}
const predefineColors = [
    '#ff4500',
    '#ff8c00',
    '#ffd700',
    '#90ee90',
    '#00ced1',
    '#409EFF',
    '#c71585'
]

// data
let allTags: Ref<Array<ITagRelationship>> = ref([])
let filterTags: ComputedRef<Array<ITagRelationship>> = computed(() => {
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
let targetTag: ReactiveVariable<ITag> = reactive(defaultTag)
let inputValue: Ref<string> = ref("")

// callback function
async function handleUpdateConfirm() {
    if (targetTag) {
        const tagUpdateData = {
            name: targetTag.name,
            color: targetTag.color,
            id: targetTag.id
        }
        const response = await fetch(`${stateStore.backendHost}/tag/update_tag`, {
            method: 'PUT',
            mode: 'cors',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify(tagUpdateData)
        })
        if (response.status != 202) {
            ElNotification({
                title: '更新失败',
                message: response.statusText,
                type: 'error',
                duration: 2000
            })
        } else {
            const data = await response.json() as ITagRelationship
            const index = allTags.value.findIndex((t) => { return t.id === data.id })
            allTags.value[index] = data
            tagStore.onUpdate(data)
            ElNotification({
                title: '更新成功',
                message: '标签更新成功',
                type: 'success',
                duration: 2000
            })
        }
    }
    inputVisible.value = false
    targetTag = defaultTag
}

function handleUpdateCancel() {
    inputVisible.value = false
    targetTag = defaultTag
}

function handleShowDialog(tag: ITagRelationship) {
    inputVisible.value = true;
    targetTag.name = tag.name
    targetTag.color = tag.color
    targetTag.id = tag.id
}

function handleShowChooseDialog(tag: ITagRelationship) {
    chooseVisible.value = true;
    targetTag.name = tag.name
    targetTag.color = tag.color
    targetTag.id = tag.id
}

function handleChooseCancel() {
    chooseVisible.value = false
    targetTag = defaultTag
}

function handleChooseConfirm() {
    const chooseTagData = {
        name: targetTag.name,
        color: targetTag.color,
        id: targetTag.id
    }
    tagStore.onChoose(chooseTagData)
    chooseVisible.value = false
    targetTag = defaultTag
}

async function handleDeleteTag(tagId: number) {
    const response = await fetch(`${stateStore.backendHost}/tag/delete_tag?tag_id=${tagId}`, {
        method: 'DELETE',
        mode: 'cors',
    })
    if (response.status != 200) {
        ElNotification({
            title: '删除失败',
            message: response.statusText,
            type: 'error',
            duration: 2000
        })
    } else {
        loadAllTags()
        tagStore.onDelete()
        ElNotification({
            title: '删除成功',
            message: '标签删除成功',
            type: 'success',
            duration: 2000
        })
    }
}

async function handleRemoveResourceItem(tagId: number, resourceItemId: number) {
    const response = await fetch(`${stateStore.backendHost}/resource/remove_resource_item?tag_id=${tagId}&resource_item_id=${resourceItemId}`, {
        method: 'PUT',
        mode: 'cors',
    })
    if (response.status == 202) {
        loadAllTags()
        tagStore.onRemove()
        ElNotification({
            title: '移除成功',
            message: '标签关联对象移除成功',
            type: 'success',
            duration: 2000
        })
    } else {
        ElNotification({
            title: '移除失败',
            message: response.statusText,
            type: 'error',
            duration: 2000
        })
    }
}

function handleClose() {
    tagStore.show = false;
    tagStore.editable = true;
    tagStore.filterId = -1
}

// load function
async function loadAllTags() {
    const response = await fetch(`${stateStore.backendHost}/tag/get_tags`, {
        method: 'GET',
        mode: 'cors',
    })
    if (response.status != 200) {
        ElNotification({
            title: '查找失败',
            message: response.statusText,
            type: 'error',
            duration: 2000
        })
    } else {
        const data = await response.json()
        allTags.value = data as Array<ITagRelationship>
    }
}

function isChoosable(id: number) {
    const tag = allTags.value.find((t) => { return t.id === id })
    if (tag !== undefined) {
        const item = tag.resource_items.find((r) => { return r.id === filterId.value })
        if (item !== undefined) return false
        else return true
    } else return true
}

// hook
onMounted(async () => {
    loadAllTags()
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
            <el-input v-model="inputValue" clearable />
            <el-collapse>
                <el-collapse-item v-for="tag in filterTags" :key="tag.id" :name="tag.id">
                    <template #title>
                        <tag :color="tag.color" :closable="false" :disable="!isChoosable(tag.id)"
                            @click="handleShowChooseDialog(tag)">
                            {{ tag.name }}
                        </tag>
                    </template>
                    <template #default>
                        <el-button-group style="margin-bottom: 12px; margin-left: 2px;">
                            <el-button size="small" @click="handleShowDialog(tag)" class="button" :disabled="!editable">
                                <font-awesome-icon :icon="['fas', 'pen']" class="icon" />
                            </el-button>
                            <el-popconfirm title="确认删除此标签吗?" confirm-button-text="确认" cancel-button-text="取消"
                                @confirm="handleDeleteTag(tag.id)" :hide-after="0">
                                <template #reference>
                                    <el-button size="small" class="button" :disabled="!editable">
                                        <font-awesome-icon :icon="['fas', 'trash-can']" class="icon" />
                                    </el-button>
                                </template>
                            </el-popconfirm>
                        </el-button-group>
                        <span v-for="resource in tag.resource_items" class="tag-container">
                            <span class="tag-drawer">
                                <font-awesome-icon :icon="['fas', 'file']" class="icon" />
                                {{ resource.name }}
                            </span>
                            <el-popconfirm title="确认删除此资源与此标签的关联吗?" confirm-button-text="确认" cancel-button-text="取消"
                                @confirm="handleRemoveResourceItem(tag.id, resource.id)" :hide-after="0">
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
                <el-button size="small" type="primary" @click="handleUpdateConfirm" class="button">
                    <font-awesome-icon :icon="['fas', 'check']" class="icon" />
                    <span style="margin-left: 8px;">
                        确认
                    </span>
                </el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog v-model="chooseVisible" title="提示" width="30%">
        <div style="display: flex; align-items: center;">
            <tag :color="targetTag?.color" :closable="false" :disable="false">
                {{ targetTag?.name }}
            </tag>
            <span style="margin-left: 12px;">确定选择此标签吗</span>
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