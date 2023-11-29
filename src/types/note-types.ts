import { ITag } from "./tag-types"

export interface INote {
    id: number,
    name: string,
    url: string,
    tags: Array<ITag>
}