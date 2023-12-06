import { EmojiSchema } from "@/schemas/emoji";
import { BaseApi } from "./base";
import pFetch from "./fetch";

export class EmojiApi extends BaseApi {
    public static async getEmoji(emoji: string): Promise<Array<EmojiSchema>> {
        return new Promise(function (resolve, reject) {
            pFetch(`/emoji/get_emoji?emoji=${emoji}`, {
                isErrTip: false
            })
                .then(async res => {
                    const emoji = await res.json() as Array<EmojiSchema>
                    resolve(emoji)
                })
                .catch(e => reject(e))
        })
    }
}