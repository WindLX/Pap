import { LoginSchema, TokenSchema } from "@/schemas/token";
import { BaseApi } from "./base";
import pFetch from "./fetch";

export class LoginApi extends BaseApi {
    public static async login(login: LoginSchema): Promise<TokenSchema> {
        return new Promise(function (resolve) {
            pFetch('/login/', {
                method: 'POST',
                body: JSON.stringify(login),
            }).then(async res => {
                if (res.status === 200) {
                    const token = await res.json() as TokenSchema
                    resolve(token)
                }
            })
        })
    }
}