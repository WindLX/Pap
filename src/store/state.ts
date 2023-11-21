import { defineStore } from 'pinia'
import { CustomWindow } from '@/types/custom-types'

export enum SidebarIndex {
    House = 'house',
    Note = 'note',
    Resource = "resource",
    Timeline = "timeline",
    Setting = "setting",
}

export enum ContentIndex {
    House = 'house',
    Note = 'note',
    Resource = "resource",
}

export const useStateStore = defineStore('states', {
    state: () => {
        return {
            sidebarIndex: SidebarIndex.House,
            contentIndex: ContentIndex.House,
            isMiddleBarShow: true,
            host: (window as unknown as CustomWindow).host,
            port: (window as unknown as CustomWindow).port
        }
    },
    getters: {
        backendHost: (state) => `http://${state.host}:${state.port}`
    }
})