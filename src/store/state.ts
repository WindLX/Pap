import { defineStore } from 'pinia'

export enum SidebarIndex {
    Resource = "resource",
    Search = "search",
    Timeline = "timeline",
    Setting = "setting"
}

export const useStateStore = defineStore('states', {
    state: () => {
        return {
            sidebarIndex: SidebarIndex.Resource,
            isMiddleBarShow: true,
            backendHost: "http://127.0.0.1:8001",
        }
    }
})