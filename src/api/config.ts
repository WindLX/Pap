import { Section, SystemConfigSchema, BasicConfigSchema } from "@/schemas/config";
import { LoginSchema } from "@/schemas/token";
import { BaseApi } from "./base";
import pFetch from "./fetch";

export class ConfigApi extends BaseApi {
    public static async getConfig(section: Section): Promise<BasicConfigSchema | SystemConfigSchema> {
        return new Promise(function (resolve, reject) {
            pFetch(`/config/get_config/${section}`)
                .then(async res => {
                    const config = await res.json()
                    resolve(config)
                }).catch(e => {
                    reject(e)
                })
        })
    }

    public static async setConfig(section: Section, config: BasicConfigSchema | SystemConfigSchema): Promise<void> {
        return new Promise(function (resolve, reject) {
            const successMsg = () => {
                switch (section) {
                    case Section.Basic:
                        return '基本设置已保存,将在应用重启后生效'
                    case Section.System:
                        return '系统设置已保存,将在应用重启后生效'
                }
            }
            pFetch(`/config/set_config/${section}`, {
                method: 'PUT',
                body: JSON.stringify(config),
                successMsg: successMsg()
            }).then(() => {
                resolve()
            }).catch(e => {
                reject(e)
            })
        })
    }

    public static async setPwd(pwd: LoginSchema): Promise<void> {
        return new Promise(function (resolve, reject) {
            pFetch(`/config/set_pwd`, {
                method: 'PUT',
                body: JSON.stringify(pwd),
                successMsg: '密码修改成功,将在应用重启后生效'
            }).then(() => {
                resolve()
            }).catch(e => {
                reject(e)
            })
        })
    }
}