export enum TabDataType {
    ResourceItem,
    Content,
    Note
}

export enum TabState {
    Lock,
    Save
}

export interface TabData {
    typ: TabDataType
    id: number
    name: string
    state: Set<TabState>
}