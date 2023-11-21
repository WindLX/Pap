<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
    ElAutoResizer, ElButton,
    ElNotification, ElPopover,
    ElInput, ElTooltip, ElText
} from 'element-plus'
import { INote } from '@/types/note-types'
import { TabData, TabDataType, TabState } from '@/types/tab-types'
import { tab } from '@store'
import pFetch from '@/utils/fetch'

// state
const tabStore = tab.useNoteTabStore()

// data
let noteSet = ref<Array<INote>>([])
let newNoteName = ref<string | null>(null)
let filterText = ref<string>("")
let visible = ref<boolean>(false)

// load function
async function getNoteAsync() {
    await pFetch(`/note/get_notes`, {
        successCallback: async (response) => {
            const newData = await response.json()
            noteSet.value = newData as Array<INote>
        }
    })
}

// callback function
async function handleCreateNoteAsync() {
    if (newNoteName.value !== null) {
        const data = {
            name: newNoteName.value,
        }
        visible.value = false
        newNoteName.value = null
        await pFetch(`/note/create_note`, {
            method: 'POST',
            body: JSON.stringify(data),
            successMsg: '笔记文件创建成功',
            successCallback: async () => {
                await getNoteAsync()
            }
        })
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

async function handleDeleteNoteAsync(noteId: number) {
    await pFetch(`/note/delete_note?note_id=${noteId}`, {
        method: 'DELETE',
        successMsg: '笔记文件删除成功',
        successCallback: async () => {
            await getNoteAsync()
            tabStore.flush(noteSet.value)
        }
    })
}

function onNoteClick(note: INote) {
    function judge(t: TabData) {
        return t.typ === TabDataType.Note && t.id === note.id
    }
    const flag = tabStore.tabs.find((t) => judge(t))
    if (flag == undefined) {
        tabStore.tabs.push(<TabData>{ typ: TabDataType.Note, id: note.id, name: note.name, state: new Set([TabState.Save]) })
    }
    tabStore.currentIndex = tabStore.tabs.findIndex((t) => judge(t))
}

// tool function
function filterName(name: string): boolean {
    if (filterText.value !== '') {
        const target = name
        const source = filterText.value
        const regex = new RegExp(source, 'i');
        return regex.test(target)
    }
    else
        return true
}

// hook
onMounted(async () => {
    await getNoteAsync()
})
</script>

<template>
    <div class="note">
        <el-popover placement="bottom" :visible="visible" :width="200">
            <p style="margin-top: 0; font-size: 12px;">内容文件名称</p>
            <div style="text-align: center; margin: 0">
                <el-input size="small" style="margin-bottom: 6px;" v-model="newNoteName"></el-input>
                <el-button size="small" text @click="newNoteName = null; visible = false">取消</el-button>
                <el-button size="small" type="primary" @click="handleCreateNoteAsync()">确认</el-button>
            </div>
            <template #reference>
                <el-button class="add" size="small" @click="visible = true">
                    <font-awesome-icon :icon="['fas', 'plus']" />
                </el-button>
            </template>
        </el-popover>
        <el-input style="height: 24px; width: 90%; margin-bottom: 3px;" v-model="filterText" />
        <el-auto-resizer>
            <span v-for="(note, index) in noteSet" v-show="filterName(note.name)" :key="index">
                <el-tooltip placement="bottom" :content="note.name" :hide-after="0">
                    <div class="node">
                        <div class="label" @click="onNoteClick(note)">
                            <font-awesome-icon :icon="['fas', 'file']" class="icon" />
                            <el-text truncated style="max-width: 90%;">{{ note.name }}</el-text>
                        </div>
                        <el-button size="small" class="leaf" style="height: 18px; width: 72px">
                            <font-awesome-icon :icon="['fas', 'trash-can']" @click="handleDeleteNoteAsync(note.id)" />
                        </el-button>
                    </div>
                </el-tooltip>
            </span>
        </el-auto-resizer>
    </div>
</template>

<style scoped>
.note {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.note .add {
    margin: 6px 0;
    width: 60%;
    height: 18px;
}

.note .add:not(:hover) .icon {
    color: #6d6d6d;
}

.note .node {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.note .node:hover {
    background-color: var(--el-fill-color-light);
}

.note .node .label {
    cursor: pointer;
    width: 62%;
    display: flex;
    align-items: center;
    color: #6d6d6d;
}

.note .node .icon {
    margin-right: 12px;
}

.note .node .leaf {
    right: 18px
}

.note .node .button {
    height: 18px;
}
</style>