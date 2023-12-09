import { BaseSchema } from "./base"

export interface ResourceSchema extends BaseSchema {
    name: string,
    url: string,
}