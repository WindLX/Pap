import { SidebarIndex, ContentIndex, useStateStore } from "./state"
import { useResourceTabStore, useNoteTabStore, isResourceItem } from "./tab"
import { useTagStore, ChooseSource } from "./tag"

export const state = {
    SidebarIndex,
    ContentIndex,
    useStateStore
}

export const tab = {
    useResourceTabStore,
    useNoteTabStore,
    isResourceItem
}

export const tag = {
    useTagStore,
    ChooseSource
}