import { defineStore } from 'pinia'

interface CustomWindow extends Window {
    host: string,
    port: number
}

export enum SidebarIndex {
    Net = 'net',
    Note = 'note',
    Resource = 'resource',
    Setting = "setting",
}

export enum ContentIndex {
    Net = 'net',
    Note = 'note',
    Resource = 'resource',
}

const sideIndexes = [SidebarIndex.Note, SidebarIndex.Net, SidebarIndex.Resource, SidebarIndex.Setting]
const contentIndexes = [ContentIndex.Note, ContentIndex.Net, ContentIndex.Resource]

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
        backendHost: (state) => `http://${state.host}:${state.port}`,
    },
    actions: {
        isActive(index: number): string {
            return this.sidebarIndex == sideIndexes[index] ? 'active' : ''
        },
        select(index: number) {
            this.sidebarIndex = sideIndexes[index]
            if (index != 3) {
                this.contentIndex = contentIndexes[index]
            }
        },
        ownMiddlebar(): boolean {
            let a = this.sidebarIndex != SidebarIndex.Net
            let b = this.sidebarIndex != SidebarIndex.Resource
            return a && b
        }
    }
})