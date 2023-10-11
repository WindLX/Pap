declare module "custom-types" {
    export interface CustomWindow extends Window {
        host: string,
        port: number
    }
}