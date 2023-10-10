import { defineStore } from 'pinia'
import { INodeResourceItem } from 'resource-types'
import { TabData } from 'tab-types'

export enum TabDataType {
    ResourceItem,
    Content
}

export function isResourceItem(node: any) {
    return (node && 'name' in node && 'url' in node && 'contents' in node && 'tags' in node)
}

export const useTabStore = defineStore('tabs', {
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
        flush(data: Array<INodeResourceItem>) {
            if (data.length === 0) {
                this.tabs = []
            } else {
                this.tabs = this.tabs.filter(item => {
                    if (item.typ === TabDataType.ResourceItem) {
                        return data.some(bItem => bItem.id === item.id);
                    } else {
                        return data.some(bItem => bItem.contents.some(content => content.id === item.id));
                    }
                });
            }
            this.currentIndex = 0
        }
    },
})