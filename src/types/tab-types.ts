export enum TabDataType {
    ResourceItem,
    Content
}

export interface TabData {
    typ: TabDataType,
    id: number
    name: string
}