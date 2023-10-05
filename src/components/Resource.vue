<script setup lang="ts">
import { ElTreeV2, ElAutoResizer, ElButton, ElButtonGroup, ElNotification, TreeNode } from 'element-plus';
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
    children: 'content',
}

// data
const data = ref<Array<IResourceItem>>([])

// load function
async function getResource() {
    const response = await fetch(`${store.backendHost}/resource/get_resource`, { method: 'GET', mode: 'cors' })
    if (response.status == 200) {
        data.value = await response.json() as Array<IResourceItem>
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
                                <el-button class="button" size="small">
                                    <font-awesome-icon :icon="['fas', 'file-pen']" />
                                </el-button>
                                <el-button class="button" size="small">
                                    <font-awesome-icon :icon="['fas', 'trash-can']" />
                                </el-button>
                            </el-button-group>
                        </div>
                        <div class="node" v-else>
                            <span>
                                <font-awesome-icon :icon="['fas', 'note-sticky']" class="icon" />{{ node.label }}
                            </span>
                            <el-button class="button" size="small">
                                <font-awesome-icon :icon="['fas', 'trash-can']" />
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