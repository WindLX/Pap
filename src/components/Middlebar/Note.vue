<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
    ElAutoResizer, ElButton,
    ElScrollbar,
    ElInput
} from 'element-plus'
import { useTagStore, TagEvent } from '@/store/tag'
import { NoteApi } from '@/api/note'
import type { NoteUpdateSchema } from '@/schemas/note'
import type { TagSchema } from '@/schemas/tag'
import { useFilterName } from '@/utils';
import NoteItem from './NoteItem.vue'
import MiddlebarItemAdd from './MiddlebarItemAdd.vue'
import Tag from '../Tag/Tag.vue'

// state
const tagStore = useTagStore()

tagStore.$onAction(
    ({
        name: name,
        after: after,
    }) => {
        after((result) => {
            switch (name) {
                case "onUpdate":
                    filterTags.value = []
                    getNoteAsync()
                    break;
                case "onChoose":
                    const e = result as TagEvent
                    if (e.filterId === -1) {
                        filterTags.value = filterTags.value.filter((t) => t.id !== e.tag.id)
                        filterTags.value.push(e.tag)
                    }
                    break;
            }
        })
    }
)

// data
let noteSet = ref<Array<NoteUpdateSchema>>([])
let filterTags = ref<Array<TagSchema>>([])
const { filterText, filterName } = useFilterName();

// load function
async function getNoteAsync() {
    const newData = await NoteApi.getNotes()
    noteSet.value = newData
}

// callback function
function handleShowTag() {
    tagStore.setShow()
}

function handleClose(id: number) {
    filterTags.value = filterTags.value.filter((t) => t.id !== id)
}

// hook
onMounted(async () => {
    await getNoteAsync()
})
</script>

<template>
    <div class="note">
        <middlebar-item-add :name="'笔记文件'" :create-item-func="NoteApi.createNote"
            @create-item="(newNote) => noteSet.push(newNote)" />
        <el-input class="filter-input" v-model="filterText">
            <template #append>
                <el-button @click="handleShowTag">
                    <font-awesome-icon :icon="['fas', 'tag']" class="icon" />
                </el-button>
            </template>
        </el-input>
        <el-scrollbar v-if="filterTags.length != 0" class="filter-container">
            <div class="filter-tags">
                <tag v-for="tag in filterTags" :key="tag.id" :color="tag.color" closable :disable="false"
                    @close="handleClose(tag.id)">
                    {{ tag.name }}
                </tag>
            </div>
        </el-scrollbar>
        <el-auto-resizer>
            <note-item v-for="note in noteSet" :key="note.id" v-show="filterName(note.name)" :note="note"
                @update:note="(value: NoteUpdateSchema) => noteSet.find(item => item.id === value.id)!.name = value.name"
                @remove="(id) => noteSet = noteSet.filter(item => item.id !== id)" />
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

.note .filter-input {
    height: 24px;
    width: 90%;
    margin-bottom: 3px;
}

.note .filter-container {
    height: 32px;
    margin: 8px;
}

.note .filter-tags {
    display: flex;
    margin-bottom: 18px;
    max-width: 50vw;
}
</style>