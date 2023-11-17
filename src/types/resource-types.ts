export interface INodeResourceItem {
    nodeId: string
    id: number
    name: string
    url: string
    tags: Array<ITag>
    contents: Array<IContent>
}

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

export interface ITagRelationship {
    id: number
    name: string
    color: string
    resource_items: Array<IResourceItem>
}

export interface IContent {
    id: number
    name: string
    url: string
}