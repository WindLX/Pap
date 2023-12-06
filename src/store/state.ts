import { defineStore } from 'pinia'

interface CustomWindow extends Window {
    host: string,
    port: number
}

export enum SidebarIndex {
    Net = 'net',
    Note = 'note',
    Database = 'database',
    Setting = "setting",
}

export enum ContentIndex {
    Net = 'net',
    Database = 'database',
    Note = 'note',
}

export const useStateStore = defineStore('states', {
    state: () => {
        return {
            sidebarIndex: SidebarIndex.Note,
            contentIndex: ContentIndex.Note,
            isMiddleBarShow: true,
            host: (window as unknown as CustomWindow).host,
            port: (window as unknown as CustomWindow).port
        }
    },
    getters: {
        backendHost: (state) => `http://${state.host}:${state.port}`
    }
})