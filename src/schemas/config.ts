import { BaseSchema } from "./base"
import { useStateStore } from "@/store/state"

export const enum Section {
    Basic = "basic",
    System = "system",
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

export type {
    SystemConfigSchema,
    BasicConfigSchema,
}

export {
    systemConfigDefault,
    basicConfigDefault,
}