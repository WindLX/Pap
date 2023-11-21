export interface ISystemConfig {
    host: string
    port: number
}

export interface IBasicConfig {
    title: string
    log_level: string
}

export interface IPathConfig {
    resource_dir: string
    content_dir: string
    note_dir: string
    log_path: string
    tag_path: string
    emoji_path: string
}
