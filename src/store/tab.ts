import { defineStore } from 'pinia'
import { IResourceItem, IContent } from '../utils/resource'

export const useTabStore = defineStore('tabs', {
    state: () => ({
        currentIndex: 0,
        tabs: <Array<IResourceItem | IContent>>[]
    }),
    getters: {
        current(state) {
            return state.tabs[state.currentIndex]
        }
    },
    actions: {
        flush(data: IResourceItem | IContent) {
            this.tabs.filter((t) => {
                isResultItem(t) && isResultItem(data) && t.id
            })
        }
    },
})

// tool function
export function isResultItem(node: any) {
    return (node && 'name' in node && 'url' in node && 'contents' in node && 'tags' in node)
}