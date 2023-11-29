import { defineStore } from 'pinia'
import { INodeResourceItem } from '../types/tag-types'
import { INote } from '../types/note-types'
import { TabData, TabDataType, TabState } from '../types/tab-types'

export function isResourceItem(node: any) {
    return (node && 'name' in node && 'url' in node && 'contents' in node && 'tags' in node)
}

export const useResourceTabStore = defineStore('workspaceTabs', {
    state: () => ({
        currentIndex: 0,
        tabs: <Array<TabData>>[]
    }),
    getters: {
        current(state) {
            return state.tabs[state.currentIndex]
        }
    },
    actions: {
        updateState(typ: TabState, state: boolean, index: number) {
            if (state) {
                this.tabs[index].state.add(typ)
            } else {
                this.tabs[index].state.delete(typ)
            }
        },
        flush(data: Array<INodeResourceItem>) {
            if (data.length === 0) {
                this.tabs = []
            } else {
                this.tabs = this.tabs.filter(item => {
                    if (item.typ === TabDataType.ResourceItem) {
                        return data.some(bItem => bItem.id === item.id);
                    } else {
                        return data.some(bItem => bItem.contents.some(content => {
                            if (content.id === item.id) {
                                item.name = content.name
                                return true
                            } else {
                                return false
                            }
                        }));
                    }
                });
            }
            this.currentIndex = 0
        },
    },
})

export const useNoteTabStore = defineStore('noteTabs', {
    state: () => ({
        currentIndex: 0,
        tabs: <Array<TabData>>[]
    }),
    getters: {
        current(state) {
            return state.tabs[state.currentIndex]
        }
    },
    actions: {
        updateState(typ: TabState, state: boolean, index: number) {
            if (state) {
                this.tabs[index].state.add(typ)
            } else {
                this.tabs[index].state.delete(typ)
            }
        },
        flush(data: Array<INote>) {
            if (data.length === 0) {
                this.tabs = []
            } else {
                this.tabs = this.tabs.filter(item => {
                    if (item.typ === TabDataType.Note) {
                        return data.some(bItem => {
                            if (bItem.id === item.id) {
                                item.name = bItem.name
                                return true
                            } else {
                                return false
                            }
                        });
                    }
                });
            }
            this.currentIndex = 0
        },
    },
})