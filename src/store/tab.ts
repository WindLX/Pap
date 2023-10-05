import { defineStore } from 'pinia'
import { IResourceItem, IContent } from '../utils/resource'

export interface TabData {

}

export const useTabStore = defineStore('tabs', {
    state: () => {
        return {
            current: <IContent>{},
            tabs: <Array<IResourceItem | IContent>>[]
        }
    }
})