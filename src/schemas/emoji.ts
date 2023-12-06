import { BaseSchema } from "./base"

export interface EmojiSchema extends BaseSchema {
    unicode: string
    name: string
}
