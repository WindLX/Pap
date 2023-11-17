import { defineStore } from 'pinia'
import { CustomWindow } from '@/types/custom-types'

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
            host: (window as unknown as CustomWindow).host,
            port: (window as unknown as CustomWindow).port
        }
    },
    getters: {
        backendHost: (state) => `http://${state.host}:${state.port}`
    }
})