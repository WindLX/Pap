<script setup lang="ts">
import { ElTreeV2, ElAutoResizer, ElButton, ElButtonGroup, ElNotification, TreeNode, ElPopover, ElInput } from 'element-plus';
import type { TreeNodeData } from 'element-plus/lib/components/tree/src/tree.type.js';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ref, onMounted } from 'vue'
import { useStateStore } from '../store/state'
import { useTabStore } from '../store/tab'
import { IResourceItem } from '../utils/resource'

// state
const store = useStateStore()
const tabStore = useTabStore()

// const
const fileInput = ref<HTMLInputElement | null>(null)
const props = {
    value: 'url',
    label: 'name',
    children: 'contents',
}
const visible = ref(false)

// data
const data = ref<Array<IResourceItem>>([])
const newContentName = ref<string | null>(null)

// load function
async function getResource() {
    const response = await fetch(`${store.backendHost}/resource/get_resource`, { method: 'GET', mode: 'cors' })
    if (response.status == 200) {
        const newData = await response.json()
        console.log(newData)
        data.value = newData as Array<IResourceItem>
    }
}

// tool function
function isResultItem(node: any) {
    return (node && 'name' in node && 'url' in node && 'contents' in node && 'tags' in node)
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
        const response = await fetch(`${store.backendHost}/resource/create_resource_item`, {
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
        } else {
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
        visible.value = false
        newContentName.value = null
        const response = await fetch(`${store.backendHost}/resource/create_content`, {
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
        visible.value = false
    }
}

async function handleDeleteResourceItem(id: number) {
    const response = await fetch(`${store.backendHost}/resource/delete_resource_item?resource_item_id=${id}`, {
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
    const response = await fetch(`${store.backendHost}/resource/delete_content?content_id=${id}`, {
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
    } else {
        ElNotification({
            title: '删除失败',
            message: response.statusText,
            type: 'error',
            duration: 2000
        })
    }
}

function onNodeClick(data: TreeNodeData, _node: TreeNode, _e: MouseEvent) {
    tabStore.current.name = data.name
}

// hook
onMounted(() => {
    getResource()
})
</script>

<template>
    <div class="resource">
        <input type="file" style="display: none;" ref="fileInput" @change="handleFileChange">
        <el-button class="add" @click="openFilePicker">
            <font-awesome-icon :icon="['fas', 'plus']" class="icon" />
        </el-button>
        <el-auto-resizer>
            <template #default="{ height }">
                <el-tree-v2 :data="data" :props="props" :height="height" highlight-current @node-click="onNodeClick">
                    <template #default="{ node, data }">
                        <div class="node" v-if="isResultItem(data)">
                            <span>
                                <font-awesome-icon :icon="['fas', 'file']" class="icon" />{{ node.label }}
                            </span>
                            <el-button-group class="button-group">
                                <el-popover placement="bottom" :visible="visible" :width="200" trigger="click">
                                    <p style="margin-top: 0; font-size: 12px;">内容文件名称</p>
                                    <div style="text-align: center; margin: 0">
                                        <el-input size="small" style="margin-bottom: 6px;"
                                            v-model="newContentName"></el-input>
                                        <el-button size="small" text
                                            @click="visible = false; newContentName = null">取消</el-button>
                                        <el-button size="small" type="primary"
                                            @click="handleCreateContent(data.id)">确认</el-button>
                                    </div>
                                    <template #reference>
                                        <el-button class="button" size="small">
                                            <font-awesome-icon :icon="['fas', 'file-pen']" @click="visible = true" />
                                        </el-button>
                                    </template>
                                </el-popover>
                                <el-button class="button" size="small" @click="handleDeleteResourceItem(data.id)">
                                    <font-awesome-icon :icon="['fas', 'trash-can']" />
                                </el-button>
                            </el-button-group>
                        </div>
                        <div class="node" v-else>
                            <span>
                                <font-awesome-icon :icon="['fas', 'note-sticky']" class="icon" />{{ node.label }}
                            </span>
                            <el-button size="small" style="margin-right: 27px; height: 18px; width: 48px;">
                                <font-awesome-icon :icon="['fas', 'trash-can']" @click="handleDeleteContent(data.id)" />
                            </el-button>
                        </div>
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
    justify-content: space-between;
}

.resource .node .icon {
    margin-right: 18px;
}

.resource .node .button-group {
    margin-right: 18px;
}

.resource .node .button-group .button {
    height: 18px;
}
</style>