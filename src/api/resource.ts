import { BaseApi } from "./base";
import { ResourceSchema } from '@/schemas/resource';
import pFetch from "./fetch";

export class ResourceApi extends BaseApi {
    public static async getResource(url: string): Promise<string> {
        return new Promise(function (resolve, reject) {
            pFetch(`/${url}`)
                .then(async res => {
                    const text = await res.text()
                    resolve(text)
                })
                .catch(e => reject(e))
        })
    }

    public static async getBlobUrl(url: string): Promise<string> {
        return new Promise(function (resolve, reject) {
            pFetch(`/${url}`)
                .then(async res => {
                    const blob = await res.blob()
                    const objectURL = URL.createObjectURL(blob);
                    resolve(objectURL)
                })
                .catch(e => reject(e))
        })
    }

    public static async getResources(): Promise<Array<ResourceSchema>> {
        return new Promise(function (resolve, reject) {
            pFetch(`/resource/get_resources`)
                .then(async res => {
                    const resources = await res.json()
                    resolve(resources)
                })
                .catch(e => reject(e))
        })
    }

    public static async uploadResource(file: FormData): Promise<ResourceSchema> {
        return new Promise(function (resolve, reject) {
            pFetch(`/resource/upload_resource`, {
                method: 'POST',
                successMsg: "文件上传成功",
                body: file,
                isForm: true,
            }).then(async res => {
                const resource = await res.json()
                resolve(resource)
            }).catch(e => reject(e))
        })
    }

    public static async deleteResource(url: string): Promise<void> {
        return new Promise(function (resolve, reject) {
            pFetch(`/resource/delete_resource?url=${url}`, {
                method: 'DELETE',
                successMsg: "文件删除成功"
            }).then(() => {
                resolve()
            }).catch(e => reject(e))
        })
    }

    public static async exportData(): Promise<string> {
        return new Promise(function (resolve, reject) {
            pFetch(`/resource/export_data`).then(async (res) => {
                const blob = await res.blob()
                const objectURL = URL.createObjectURL(blob);
                resolve(objectURL)
            }).catch(e => reject(e))
        })
    }

    public static async removeZip(): Promise<void> {
        return new Promise(function (_resolve, reject) {
            pFetch(`/resource/remove_zip`, {
                method: "DELETE",
                successMsg: "导出成功"
            }).catch(e => reject(e))
        })
    }
}