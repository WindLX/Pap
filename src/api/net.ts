import { NetSchema } from "@/schemas/net";
import { BaseApi } from "./base";
import pFetch from "./fetch";

export class NetApi extends BaseApi {
    public static async get_net(): Promise<NetSchema> {
        return new Promise(function (resolve) {
            pFetch('/net/get_net').then(async res => {
                if (res.status === 200) {
                    const net = await res.json() as NetSchema
                    resolve(net)
                }
            })
        })
    }
}