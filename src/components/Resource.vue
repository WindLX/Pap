<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import type { TreeNodeData } from 'element-plus/lib/components/tree/src/tree.type.js'
import {
    ElTreeV2, ElAutoResizer, ElButton, ElButtonGroup,
    ElNotification, ElPopover, ElInput, ElTooltip, ElText
} from 'element-plus'
import { IContent, IResourceItem, INodeResourceItem } from 'resource-types'
import { TabData } from 'tab-types';
import { useStateStore } from '../store/state'
import { useTabStore, TabDataType, isResourceItem } from '../store/tab'

// state
const stateStore = useStateStore()
const tabStore = useTabStore()

// const
const fileInput = ref<HTMLInputElement | null>(null)
const props = {
    value: 'nodeId',
    label: 'name',
    children: 'contents',
}
const visible = ref<Array<boolean>>([])

// data
const data = ref<Array<INodeResourceItem>>([])
const newContentName = ref<string | null>(null)

// load function
async function getResource() {
    const response = await fetch(`${stateStore.backendHost}/resource/get_resource`, { method: 'GET', mode: 'cors' })
    if (response.status == 200) {
        const newData = await response.json()
        data.value = (newData as Array<IResourceItem>).map(d => {
            return <INodeResourceItem>{
                nodeId: `${isResourceItem(d) ? 'r' : 'c'}${d.id}`,
                ...d
            }
        })
        visible.value = Array(data.value.length).fill(false)
    }
}

// callback function
function openFilePicker() {
    (fileInput.value as HTMLInputElement).click();
}

async function handleFileChange(event: Event) {
    const inputElement = event.target as HTMLInputElement;
    const selectedFile = inputElement.files ? inputElement.files[0] : null;
    if (selectedFile) {
        const formData = new FormData();
        formData.append('file', selectedFile);
        const response = await fetch(`${stateStore.backendHost}/resource/create_resource_item`, {
            method: 'POST',
            mode: 'cors',
            body: formData,
        })
        if (response.status == 201) {
            ElNotification({
                title: '托管成功',
                message: '文件托管成功',
                type: 'success',
                duration: 2000
            })
            await getResource()
        } else if (response.status == 403) {
            ElNotification({
                title: '托管失败',
                message: '不支持的文件格式',
                type: 'error',
                duration: 2000
            })
        }
        else {
            ElNotification({
                title: '托管失败',
                message: response.statusText,
                type: 'error',
                duration: 2000
            })
        }
    }
}

async function handleCreateContent(id: number) {
    if (newContentName.value !== null) {
        const data = {
            name: newContentName.value,
            resource_item_id: id
        }
        visible.value[id] = false
        newContentName.value = null
        const response = await fetch(`${stateStore.backendHost}/content/create_content`, {
            method: 'POST',
            mode: 'cors',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify(data)
        })
        if (response.status == 201) {
            ElNotification({
                title: '创建成功',
                message: '内容文件创建成功',
                type: 'success',
                duration: 2000
            })
            await getResource()
        } else {
            ElNotification({
                title: '创建失败',
                message: response.statusText,
                type: 'error',
                duration: 2000
            })
        }
    } else {
        ElNotification({
            title: '创建失败',
            message: '名称不能为空',
            type: 'error',
            duration: 2000
        })
        visible.value[id] = false
    }
}

async function handleDeleteResourceItem(id: number) {
    const response = await fetch(`${stateStore.backendHost}/resource/delete_resource_item?resource_item_id=${id}`, {
        method: 'DELETE',
        mode: 'cors',
    })
    if (response.status == 200) {
        ElNotification({
            title: '删除成功',
            message: '资源文件删除成功',
            type: 'success',
            duration: 2000
        })
        data.value = data.value.filter((d) => d.id !== id)
        tabStore.flush(data.value)
    } else {
        ElNotification({
            title: '删除失败',
            message: response.statusText,
            type: 'error',
            duration: 2000
        })
    }
}

async function handleDeleteContent(id: number) {
    const response = await fetch(`${stateStore.backendHost}/content/delete_content?content_id=${id}`, {
        method: 'DELETE',
        mode: 'cors',
    })
    if (response.status == 200) {
        ElNotification({
            title: '删除成功',
            message: '内容文件删除成功',
            type: 'success',
            duration: 2000
        })
        await getResource()
        tabStore.flush(data.value)
    } else {
        ElNotification({
            title: '删除失败',
            message: response.statusText,
            type: 'error',
            duration: 2000
        })
    }
}

function onNodeClick(nodeData: TreeNodeData) {
    function judge(t: TabData) {
        return t.typ === TabDataType.ResourceItem && t.id === data.id
    }
    const data = nodeData as INodeResourceItem
    const flag = tabStore.tabs.find((t) => judge(t))
    if (flag == undefined) {
        tabStore.tabs.push(<TabData>{ typ: TabDataType.ResourceItem, id: data.id, name: data.name })
    }
    tabStore.currentIndex = tabStore.tabs.findIndex((t) => judge(t))
}

function onLeafClick(nodeData: TreeNodeData) {
    function judge(t: TabData) {
        return t.typ === TabDataType.Content && t.id === data.id
    }
    const data = nodeData as IContent
    const flag = tabStore.tabs.find((t) => judge(t))
    if (flag == undefined) {
        tabStore.tabs.push(<TabData>{ typ: TabDataType.Content, id: data.id, name: data.name })
    }
    tabStore.currentIndex = tabStore.tabs.findIndex((t) => judge(t))
}

// hook
onMounted(() => {
    getResource()
})
</script>

<template>
    <div class="resource">
        <input type="file" accept=".pdf" style="display: none;" ref="fileInput" @change="handleFileChange">
        <el-button class="add" @click="openFilePicker">
            <font-awesome-icon :icon="['fas', 'plus']" class="icon" />
        </el-button>
        <el-auto-resizer>
            <template #default="{ height }">
                <el-tree-v2 :data="data" :props="props" :height="height" highlight-current>
                    <template #default="{ node, data }">
                        <el-tooltip placement="bottom" :content="node.label" :hide-after="0">
                            <div class="node" v-if="isResourceItem(data)">
                                <div class="label" @click="onNodeClick(data)">
                                    <font-awesome-icon :icon="['fas', 'file']" class="icon" />
                                    <el-text truncated>{{ node.label }}</el-text>
                                </div>
                                <el-button-group class="button-group">
                                    <el-popover placement="bottom" :visible="visible[data.id]" :width="200" trigger="click">
                                        <p style="margin-top: 0; font-size: 12px;">内容文件名称</p>
                                        <div style="text-align: center; margin: 0">
                                            <el-input size="small" style="margin-bottom: 6px;"
                                                v-model="newContentName"></el-input>
                                            <el-button size="small" text
                                                @click="visible[data.id] = false; newContentName = null">取消</el-button>
                                            <el-button size="small" type="primary"
                                                @click="handleCreateContent(data.id)">确认</el-button>
                                        </div>
                                        <template #reference>
                                            <el-button class="button" size="small">
                                                <font-awesome-icon :icon="['fas', 'file-pen']"
                                                    @click="visible.fill(false); visible[data.id] = true" />
                                            </el-button>
                                        </template>
                                    </el-popover>
                                    <el-button class="button" size="small" @click="handleDeleteResourceItem(data.id)">
                                        <font-awesome-icon :icon="['fas', 'trash-can']" />
                                    </el-button>
                                </el-button-group>
                            </div>
                            <div class="node" v-else>
                                <div class="label" @click="onLeafClick(data)">
                                    <font-awesome-icon :icon="['fas', 'note-sticky']" class="icon" />
                                    <el-text truncated style="max-width: 90%;">{{ node.label }}</el-text>
                                </div>
                                <el-button size="small" class="leaf" style="height: 18px; width: 72px">
                                    <font-awesome-icon :icon="['fas', 'trash-can']" @click="handleDeleteContent(data.id)" />
                                </el-button>
                            </div>
                        </el-tooltip>
                    </template>
                </el-tree-v2>
            </template>
        </el-auto-resizer>
    </div>
</template>

<style scoped>
.resource {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.resource .add {
    margin: 6px 0;
    width: 60%;
    height: 18px;
}

.resource .add:not(:hover) .icon {
    color: #6d6d6d;
}

.resource .node {
    width: 100%;
    display: flex;
    align-items: center;
}

.resource .node .label {
    width: 62%;
    display: flex;
    align-items: center;
}

.resource .node .icon {
    margin-right: 12px;
}

.resource .node .button-group,
.resource .node .leaf {
    position: absolute;
    right: 18px
}

.resource .node .button-group .button {
    height: 18px;
}
</style>