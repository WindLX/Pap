import { BaseApi } from "./base";
import pFetch from "./fetch";

export class ResourceApi extends BaseApi {
    public static async getResource(url: string): Promise<any> {
        return new Promise(function (resolve, reject) {
            pFetch(`/${url}`)
                .then(async res => {
                    const text = await res.text()
                    resolve(text)
                })
                .catch(e => reject(e))
        })
    }
}