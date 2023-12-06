<script setup lang="ts">
import { ref } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
    ElButton, ElButtonGroup,
    ElPopover, ElInput,
    ElTooltip, ElText
} from 'element-plus'
import { useNoteTabStore } from '@/store/tab'
import { NoteApi } from '@/api/note'
import type { NoteUpdateSchema } from '@/schemas/note'

// props
const props = defineProps<{
    note: NoteUpdateSchema
}>()

// emits
const emits = defineEmits<{
    (e: 'update:note', note: NoteUpdateSchema): void,
    (e: 'remove', id: number): void
}>()

// state
const tabStore = useNoteTabStore()

// data
let renameNoteName = ref<string | null>(null)
let renameVisible = ref<boolean>(false)

async function handleRenameNoteAsync() {
    const data = {
        id: props.note.id,
        name: renameNoteName.value!
    }
    await NoteApi.renameNote(data)
    tabStore.updateTab(data)
    emits("update:note", data)
    handleNoteRenameCancel()
}

async function handleDeleteNoteAsync() {
    const noteId = props.note.id
    await NoteApi.deleteNote(noteId)
    tabStore.deleteTab(noteId)
    emits("remove", noteId)
}

function handleNoteClick() {
    tabStore.addTab(props.note)
}

function handleNoteRename() {
    renameVisible.value = true
    renameNoteName.value = props.note.name
}

function handleNoteRenameCancel() {
    renameVisible.value = false;
    renameNoteName.value = null
}
</script>

<template>
    <span class="note-item">
        <el-tooltip placement="bottom" :content="props.note.name" :hide-after="0">
            <div class="node">
                <div class="label" @click="handleNoteClick()">
                    <font-awesome-icon :icon="['fas', 'file']" class="icon" />
                    <el-text truncated style="max-width: 90%;">{{ props.note.name }}</el-text>
                </div>
                <el-button-group>
                    <el-popover placement="bottom" :visible="renameVisible" :width="200" trigger="click">
                        <p>修改笔记名称</p>
                        <div class="rename">
                            <el-input size="small" style="margin-bottom: 6px;" v-model="renameNoteName" />
                            <el-button size="small" text @click="handleNoteRenameCancel()">取消</el-button>
                            <el-button size="small" type="primary" @click="handleRenameNoteAsync()">确认</el-button>
                        </div>
                        <template #reference>
                            <el-button class="leaf" size="small">
                                <font-awesome-icon :icon="['fas', 'pen']" @click="handleNoteRename()" />
                            </el-button>
                        </template>
                    </el-popover>
                    <el-button size="small" class="leaf">
                        <font-awesome-icon :icon="['fas', 'trash-can']" @click="handleDeleteNoteAsync()" />
                    </el-button>
                </el-button-group>
            </div>
        </el-tooltip>
    </span>
</template>

<style scoped>
.note-item .node {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.note-item .node:hover {
    background-color: var(--el-fill-color-light);
}

.note-item .node .label {
    cursor: pointer;
    width: 62%;
    display: flex;
    align-items: center;
    color: #6d6d6d;
}

.note-item .node p {
    margin-top: 0;
    font-size: 12px;
}

.note-item .node .rename {
    text-align: center;
    margin: 0
}

.note-item .node .icon {
    margin-right: 12px;
}

.note-item .node .leaf {
    height: 18px;
    width: 36px;
}
</style>