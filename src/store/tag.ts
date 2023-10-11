import { defineStore } from 'pinia'
import { ITag } from 'resource-types'
import { TagEvent, TagRemoveEvent } from 'event-types'

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
        onUpdate(tag: ITag) {
            return tag
        },
        onRemove(tagId: number, resourceItemId: number): TagRemoveEvent {
            return { tagId: tagId, resourceItemId: resourceItemId }
        },
        onDelete(tagId: number) {
            return tagId
        },
        onChoose(tag: ITag): TagEvent {
            return {
                tag: tag,
                filterId: this.filterId
            }
        },
        onAdd() { },
    }
})