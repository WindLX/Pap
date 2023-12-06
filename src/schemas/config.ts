import { BaseSchema } from "./base"
import { useStateStore } from "@/store/state"

export const enum Section {
    Basic = "basic",
    System = "system",
    Path = "path",
}

interface BaseConfigSchema extends BaseSchema { }

interface SystemConfigSchema extends BaseConfigSchema {
    host: string
    port: number
}

interface BasicConfigSchema extends BaseConfigSchema {
    title: string
    log_level: string
}

interface PathConfigSchema extends BaseConfigSchema {
    note_dir: string
    log_path: string
    tag_path: string
    emoji_path: string
}

function systemConfigDefault(): SystemConfigSchema {
    const stateStore = useStateStore()
    return {
        host: stateStore.host,
        port: stateStore.port,
    }
}

function basicConfigDefault(): BasicConfigSchema {
    return {
        title: "Pap",
        log_level: "INFO"
    }
}

function pathConfigDefault(): PathConfigSchema {
    return {
        note_dir: ".",
        log_path: ".",
        tag_path: ".",
        emoji_path: "."
    }
}

export type {
    SystemConfigSchema,
    BasicConfigSchema,
    PathConfigSchema
}

export {
    systemConfigDefault,
    basicConfigDefault,
    pathConfigDefault
}