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

const indexes = [SidebarIndex.Note, SidebarIndex.Net, SidebarIndex.Database, SidebarIndex.Setting]

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
    },
    actions: {
        isActive(index: number): string {
            return this.sidebarIndex == indexes[index] ? 'active' : ''
        },
        select(index: number) {
            this.sidebarIndex = indexes[index]
        }
    }
})