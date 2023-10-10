import { defineStore } from 'pinia'
import { ITag, ITagRelationship, ITagEvent } from 'resource-types'

export enum ChooseSource {
    Search,
    Resource,
}

export const useTagStore = defineStore('tagDrawer', {
    state: () => {
        return {
            show: false,
            editable: true,
            filterId: -1
        }
    },
    actions: {
        onCreate() { },
        onUpdate(tag: ITagRelationship) {
            return tag
        },
        onRemove() { },
        onDelete() { },
        onChoose(tag: ITag): ITagEvent {
            return {
                tag: tag,
                filterId: this.filterId
            }
        },
        onAdd() { }
    }
})