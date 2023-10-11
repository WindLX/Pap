declare module "config-types" {
    export interface ISystemConfig {
        host: string
        port: int
    }

    export interface IBasicConfig {
        title: string
        log_level: string
    }

    export interface IPathConfig {
        resource_dir: string
        content_dir: string
        log_path: string
        tag_path: string
    }
}
