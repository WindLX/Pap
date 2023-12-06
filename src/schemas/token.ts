import { BaseSchema } from "./base"

interface LoginSchema extends BaseSchema {
    password: string
}

interface TokenSchema extends BaseSchema {
    access_token: string
    token_type: string
}

function loginDefault(): LoginSchema {
    return {
        password: "",
    }
}

export type {
    LoginSchema,
    TokenSchema,
}

export {
    loginDefault
}