import { defineStore } from 'pinia'
import { TagSchema } from '@/schemas/tag'

export interface TagEvent {
    tag: TagSchema
    filterId: number
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
        setDefault() {
            this.show = false
            this.editable = true
            this.filterId = -1
        },
        setShow() {
            this.show = true
            this.editable = true
            this.filterId = -1
        },
        setFilterShow(targetId: number) {
            this.show = true
            this.editable = false
            this.filterId = targetId
        },
        onUpdate() { },
        onChoose(tag: TagSchema): TagEvent {
            return {
                tag: tag,
                filterId: this.filterId
            }
        },
    }
})