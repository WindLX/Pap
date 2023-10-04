import { defineStore } from 'pinia'

export enum SidebarIndex {
    Resource = "resource",
    Search = "search",
    Timeline = "timeline",
    Setting = "setting"
}

export interface TabData {

}

export const useStateStore = defineStore('states', {
    state: () => {
        return {
            sidebarIndex: SidebarIndex.Resource,
            isMiddleBarShow: true,
            tabs: []
        }
    }
})