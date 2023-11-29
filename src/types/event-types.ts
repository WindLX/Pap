import { ITag } from "./tag-types"

export interface TagEvent {
    tag: ITag
    filterId: number
}

export interface TagRemoveEvent {
    tagId: number
    noteId: number
}
