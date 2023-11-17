import { ITag } from "./resource-types"

export interface TagEvent {
    tag: ITag
    filterId: number
}

export interface TagRemoveEvent {
    tagId: number
    resourceItemId: number
}
