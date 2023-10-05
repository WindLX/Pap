import { ITag } from './tag'

export interface IResourceItem {
    name: string,
    url: string,
    tag: Array<ITag>
    content: Array<string>
}