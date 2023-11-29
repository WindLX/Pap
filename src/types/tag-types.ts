import { INote } from "./note-types"

export interface ITag {
    id: number
    name: string
    color: string
}

export interface ITagRelationship {
    id: number
    name: string
    color: string
    notes: Array<INote>
}