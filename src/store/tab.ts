import { defineStore } from 'pinia'

export interface TabData {

}

export const useTabStore = defineStore('tabs', {
    state: () => {
        return {
            tabs: []
        }
    }
})