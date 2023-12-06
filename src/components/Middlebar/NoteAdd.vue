<script setup lang="ts">
import { ref } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
    ElButton, ElInput,
    ElNotification, ElPopover,
} from 'element-plus'
import { NoteApi } from '@/api/note'
import { NoteUpdateSchema } from '@/schemas/note'

const emits = defineEmits<{
    (e: 'create-note', note: NoteUpdateSchema): void
}>()

// data
let newNoteName = ref<string | null>(null)
let visible = ref<boolean>(false)

// callback function
async function handleCreateNoteAsync() {
    if (newNoteName.value !== null) {
        const data = {
            name: newNoteName.value,
        }
        const newData = await NoteApi.createNote(data)
        emits("create-note", newData)
    } else {
        ElNotification({
            title: '创建失败',
            message: '名称不能为空',
            type: 'error',
            duration: 2000
        })
    }
    handleCreateNoteCancel()
}

function handleCreateNoteCancel() {
    visible.value = false
    newNoteName.value = null
}

function handleCreateNoteShow() {
    visible.value = true
}
</script>

<template>
    <el-popover placement="bottom" :visible="visible" :width="200">
        <p class="note-add title">笔记文件名称</p>
        <div class="note-add group">
            <el-input size="small" v-model="newNoteName" class="note-add input" />
            <el-button size="small" text @click="handleCreateNoteCancel()">取消</el-button>
            <el-button size="small" type="primary" @click="handleCreateNoteAsync()">确认</el-button>
        </div>
        <template #reference>
            <el-button class="note-add button" size="small" @click="handleCreateNoteShow()">
                <font-awesome-icon :icon="['fas', 'plus']" class="icon" />
            </el-button>
        </template>
    </el-popover>
</template>

<style scoped>
.note-add.title {
    margin-top: 0;
    font-size: 12px;
}

.note-add.group {
    text-align: center;
    margin: 0;
}

.note-add.group .input {
    margin-bottom: 6px;
}

.note-add.button {
    margin: 6px 0;
    width: 60%;
    height: 18px;
}

.note-add.button:not(:hover) .icon {
    color: #6d6d6d;
}
</style>