import { BaseSchema } from "./base"
import { TagSchema } from "./tag"

interface NoteBaseSchema extends BaseSchema {
    name: string
}

interface NoteCreateSchema extends NoteBaseSchema { }

interface NoteUpdateSchema extends NoteBaseSchema {
    id: number
}

interface NoteSchema extends NoteCreateSchema {
    id: number
    url: string
}

interface NoteRelationshipSchema extends NoteSchema {
    tags: Array<TagSchema>
}

export type {
    NoteBaseSchema,
    NoteCreateSchema,
    NoteUpdateSchema,
    NoteSchema,
    NoteRelationshipSchema
}