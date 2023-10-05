export interface IResourceItem {
    id: number
    name: string
    url: string
    tags: Array<ITag>
    contents: Array<IContent>
}

export interface ITag {
    id: number
    name: string
    color: string
}

export interface IContent {
    id: number
    name: string
    url: string
}