import { BaseSchema } from "./base"
import { NoteSchema } from "./note"

interface TagBaseSchema extends BaseSchema {
    name: string
    color: string
}

interface TagCreateSchema extends TagBaseSchema {
    note_id: number
}


interface TagSchema extends TagBaseSchema {
    id: number
}

interface TagSetSchema extends BaseSchema {
    tags_id: Array<number>
}

interface TagRelationshipSchema extends TagSchema {
    notes: Array<NoteSchema>
}

function tagDefault(): TagSchema {
    return {
        id: -1,
        name: "",
        color: "#409EFF"
    }
}

const predefineColors = [
    '#ff4500',
    '#ff8c00',
    '#ffd700',
    '#90ee90',
    '#00ced1',
    '#409EFF',
    '#c71585'
]

export type {
    TagBaseSchema,
    TagCreateSchema,
    TagSchema,
    TagSetSchema,
    TagRelationshipSchema
}

export { tagDefault, predefineColors }