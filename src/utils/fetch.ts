import { ElNotification } from "element-plus"
import { state } from "@/store"

export default async function pFetch(input: RequestInfo | URL, options?:
    {
        method?: string,
        isForm?: boolean,
        body?: any,
        isErrTip?: boolean,
        successMsg?: string
        successCallback?: (res: Response) => Promise<void>
    }): Promise<Response> {
    const stateStore = state.useStateStore()
    const method = options?.method || 'GET'
    const body = options?.body || null
    const isForm = options?.isForm || false
    const isErrTip = options?.isErrTip || true
    const successCallback = options?.successCallback
    const errTitle = new Map([
        ['GET', '获取失败'],
        ['POST', '提交失败'],
        ['DELETE', '删除失败'],
        ['PUT', '修改失败']
    ])
    const successTitle = new Map([
        ['GET', '获取成功'],
        ['POST', '提交成功'],
        ['DELETE', '删除成功'],
        ['PUT', '修改成功']
    ])

    let init: RequestInit = {
        mode: 'cors',
        method: method,
        body: body
    }

    let headers: Headers = new Headers();
    headers.append('Authorization', `Bearer ${localStorage.getItem('token')}`)
    headers.append('Cache-Control', 'no-cache')
    if (!isForm) {
        headers.append('Content-Type', 'application/json')
    }

    init.headers = headers

    if (input.toString().startsWith('/')) {
        input = `${stateStore.backendHost}${input} `
    } else {
        input = `${stateStore.backendHost}/${input}`
    }

    return new Promise(function (resolve, reject) {
        fetch(input, init)
            .then(async res => {
                if (res.status === 401) {
                    ElNotification({
                        title: '鉴权失败',
                        message: res.statusText,
                        type: 'error',
                        duration: 2000
                    })
                    window.location.replace('/#/login')
                } else if (Math.floor(res.status / 100) !== 2) {
                    if (isErrTip) {
                        ElNotification({
                            title: errTitle.get(method),
                            message: res.statusText,
                            type: 'error',
                            duration: 2000
                        })
                    }
                } else if (successCallback) {
                    if (options?.successMsg) {
                        ElNotification({
                            title: successTitle.get(method),
                            message: options?.successMsg,
                            type: 'success',
                            duration: 2000
                        })
                    }
                    await successCallback(res)
                }
                resolve(res)
            })
            .catch(err => {
                if (err.status === 401) {
                    window.location.replace('/#/login')
                    reject(err)
                }
            })
    })
}