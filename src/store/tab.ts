import { defineStore } from 'pinia'
import { NoteUpdateSchema } from '@/schemas/note'
import { TabPaneName } from 'element-plus'

export enum TabState {
    Lock,
    Save
}

interface TabData {
    id: number
    name: string
    state: Set<TabState>
}

export const useNoteTabStore = defineStore('noteTabs', {
    state: () => {
        return {
            currentIndex: <TabPaneName>0,
            tabs: <Array<TabData>>[]
        }
    },
    getters: {
        length: (state) => state.tabs.length
    },
    actions: {
        addTab(data: NoteUpdateSchema) {
            let index = this.tabs.findIndex((t) => t.id === data.id)
            if (index === -1) {
                this.tabs.push({
                    id: data.id,
                    name: data.name,
                    state: new Set([TabState.Save])
                })
                index = this.tabs.length - 1
            }
            this.currentIndex = index
        },
        updateTab(data: NoteUpdateSchema) {
            const target = this.tabs.find(item => item.id === data.id)
            if (target) {
                target.name = data.name
            }
        },
        removeTab(name: TabPaneName) {
            this.tabs = this.tabs.filter((_item, index) => index !== name)
            this.currentIndex = 0
        },
        deleteTab(id: number) {
            this.tabs = this.tabs.filter(item => item.id !== id)
            this.currentIndex = 0
        },
        updateState(state: TabState, isAdd: boolean, index: number) {
            if (isAdd) {
                this.tabs[index].state.add(state)
            } else {
                this.tabs[index].state.delete(state)
            }
        },
    },
})