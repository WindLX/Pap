<script setup lang="ts">
import { ref } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
    ElButton, ElInput,
    ElNotification, ElPopover,
} from 'element-plus'

const props = defineProps<{
    name: string
    createItemFunc: (item: CreateSchema) => Promise<UpdateSchema>
}>()

const emits = defineEmits<{
    (e: 'create-item', item: UpdateSchema): void
}>()

export interface CreateSchema {
    name: string
}

export interface UpdateSchema {
    id: number
    name: string
}

// data
let newItemName = ref<string | null>(null)
let visible = ref<boolean>(false)

// callback function
async function handleCreateItemAsync() {
    if (newItemName.value !== null) {
        const data = {
            name: newItemName.value,
        }
        const newData = await props.createItemFunc(data)
        emits("create-item", newData)
    } else {
        ElNotification({
            title: '创建失败',
            message: '名称不能为空',
            type: 'error',
            duration: 2000
        })
    }
    handleCreateItemCancel()
}

function handleCreateItemCancel() {
    visible.value = false
    newItemName.value = null
}

function handleCreateItemShow() {
    visible.value = true
}
</script>

<template>
    <el-popover placement="bottom" :visible="visible" :width="200">
        <p class="item-add title">{{ props.name }}名称</p>
        <div class="item-add group">
            <el-input size="small" v-model="newItemName" class="item-add input" />
            <el-button size="small" text @click="handleCreateItemCancel()">取消</el-button>
            <el-button size="small" type="primary" @click="handleCreateItemAsync()">确认</el-button>
        </div>
        <template #reference>
            <el-button class="item-add button" size="small" @click="handleCreateItemShow()">
                <font-awesome-icon :icon="['fas', 'plus']" class="icon" />
            </el-button>
        </template>
    </el-popover>
</template>

<style scoped>
.item-add.title {
    margin-top: 0;
    font-size: 12px;
}

.item-add.group {
    text-align: center;
    margin: 0;
}

.item-add.group .input {
    margin-bottom: 6px;
}

.item-add.button {
    margin: 6px 0;
    width: 60%;
    height: 18px;
}

.item-add.button:not(:hover) .icon {
    color: #6d6d6d;
}
</style>