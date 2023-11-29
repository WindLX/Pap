<script setup lang="ts">
import { ref, reactive, onActivated } from 'vue'
import {
    ElForm, ElFormItem, ElInput, ElTooltip,
    ElCollapse, ElCollapseItem, ElButton,
    ElSlider, ElInputNumber
} from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import type { ISystemConfig, IBasicConfig, IPathConfig } from '@/types/config-types'
import { state } from '@store'
import pFetch from '@/utils/fetch';

// const
const marks = reactive<Record<number, string>>({ 0: '调试', 1: '消息', 2: '警告', 3: '错误' })
const levelStringMap = ["DEBUG", "INFO", "WARNING", "ERROR"];
const levelMap = new Map([["DEBUG", 0], ["INFO", 1], ["WARNING", 2], ["ERROR", 3]])

// state
const stateStore = state.useStateStore()

// data
let logLevel = ref(0)
let systemConfig = reactive<ISystemConfig>({
    host: stateStore.host,
    port: stateStore.port
})
let basicConfig = reactive<IBasicConfig>({
    title: "Pap",
    log_level: "INFO"
})
let pathConfig = reactive<IPathConfig>({
    note_dir: ".",
    log_path: ".",
    tag_path: ".",
    emoji_path: "."
})
let pwd = reactive<{ password: string }>({
    password: ""
})

// tool function
function numberToLogLevel(level: number): string {
    return levelStringMap[level] || "INFO";
}

function logLevelToNumber(level: string): number {
    return levelMap.get(level) || 1;
}

async function setHandler(router: string, data: any, successText: string) {
    await pFetch(`/config/set_config/${router}`, {
        method: 'PUT',
        body: JSON.stringify(data),
        successMsg: successText
    })
}

async function getHandler(router: string, callback: (res: Response) => Promise<void>) {
    await pFetch(`/config/get_config/${router}`, {
        successCallback: async (response) => {
            await callback(response)
        }
    })
}

// callback function
async function onSystemSubmitAsync() {
    await setHandler('system', systemConfig, '系统设置修改成功,将在应用重启后生效')
}

async function onPathSubmitAsync() {
    await setHandler('path', pathConfig, '路径设置修改成功')
}

async function onBasicSubmitAsync() {
    basicConfig.log_level = numberToLogLevel(logLevel.value)
    setHandler('basic', basicConfig, '基本设置修改成功,将在应用重启后生效')
}

async function onPwdSubmitAsync() {
    await pFetch(`/config/set_pwd`, {
        method: 'PUT',
        body: JSON.stringify(pwd),
        successMsg: '密码修改成功,将在应用重启后生效'
    })
}

async function onSystemCancelAsync() {
    systemConfig.host = stateStore.host
    systemConfig.port = stateStore.port
}

async function onPathCancelAsync() {
    await getHandler('path', async (response) => {
        const data = await response.json() as IPathConfig
        pathConfig.note_dir = data.note_dir
        pathConfig.log_path = data.log_path
        pathConfig.tag_path = data.tag_path
        pathConfig.emoji_path = data.emoji_path
    })
}

async function onBasicCancelAsync() {
    await getHandler('basic', async (response) => {
        const data = await response.json() as IBasicConfig
        basicConfig.log_level = data.log_level
        basicConfig.title = data.title
        logLevel.value = logLevelToNumber(basicConfig.log_level)
    })
}

async function onPwdCancelAsync() {
    pwd.password = ""
}

// hook
onActivated(() => {
    onSystemCancelAsync()
    onBasicCancelAsync()
    onPathCancelAsync()
})
</script>

<template>
    <div class="setting">
        <el-collapse accordion>
            <el-collapse-item>
                <template #title>
                    <div class="title">
                        <font-awesome-icon :icon="['fas', 'shield-halved']" class="icon" />
                        <p>系统</p>
                    </div>
                </template>
                <el-form class="form" label-position="top">
                    <el-form-item label="主机地址">
                        <el-input v-model="systemConfig.host"></el-input>
                    </el-form-item>
                    <el-form-item label="端口">
                        <el-input-number v-model="systemConfig.port"></el-input-number>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSystemSubmitAsync">提交</el-button>
                        <el-button @click="onSystemCancelAsync">取消</el-button>
                    </el-form-item>
                </el-form>
            </el-collapse-item>
            <el-collapse-item>
                <template #title>
                    <div class="title">
                        <font-awesome-icon :icon="['fas', 'gears']" class="icon" />
                        <p>基础</p>
                    </div>
                </template>
                <el-form class="form" label-position="top">
                    <el-form-item label="窗口标题">
                        <el-input v-model="basicConfig.title"></el-input>
                    </el-form-item>
                    <el-form-item label="日志等级">
                        <el-slider :marks="marks" show-stops :min="0" :max="3" size="small"
                            style="margin: 12px;margin-top: 0px; margin-bottom: 32px;" v-model="logLevel"
                            :format-tooltip="numberToLogLevel"></el-slider>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onBasicSubmitAsync">提交</el-button>
                        <el-button @click="onBasicCancelAsync">取消</el-button>
                    </el-form-item>
                </el-form>
            </el-collapse-item>
            <el-collapse-item>
                <template #title>
                    <div class="title">
                        <font-awesome-icon :icon="['fas', 'map']" class="icon" />
                        <p>路径</p>
                    </div>
                </template>
                <el-form class="form" label-position="top">
                    <el-tooltip content="笔记存放的路径" :offset="6">
                        <el-form-item label="笔记路径">
                            <el-input v-model="pathConfig.note_dir"></el-input>
                        </el-form-item>
                    </el-tooltip>
                    <el-tooltip content="数据库存放的路径" :offset="6">
                        <el-form-item label="数据库路径">
                            <el-input v-model="pathConfig.tag_path"></el-input>
                        </el-form-item>
                    </el-tooltip>
                    <el-tooltip content="日志文件存放的路径" :offset="6">
                        <el-form-item label="日志路径">
                            <el-input v-model="pathConfig.log_path"></el-input>
                        </el-form-item>
                    </el-tooltip>
                    <el-tooltip content="emoji数据库存放的路径" :offset="6">
                        <el-form-item label="emoji路径">
                            <el-input v-model="pathConfig.emoji_path"></el-input>
                        </el-form-item>
                    </el-tooltip>
                    <el-form-item>
                        <el-button type="primary" @click="onPathSubmitAsync">提交</el-button>
                        <el-button @click="onPathCancelAsync">取消</el-button>
                    </el-form-item>
                </el-form>
            </el-collapse-item>
            <el-collapse-item>
                <template #title>
                    <div class="title">
                        <font-awesome-icon :icon="['fas', 'paintbrush']" class="icon" />
                        <p>主题</p>
                    </div>
                </template>
                <!-- todo -->
            </el-collapse-item>
            <el-collapse-item>
                <template #title>
                    <div class="title">
                        <font-awesome-icon :icon="['fas', 'lock']" class="icon" />
                        <p>密码</p>
                    </div>
                </template>
                <el-form class="form" label-position="top">
                    <el-form-item label="新密码">
                        <el-input v-model="pwd.password"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onPwdSubmitAsync">提交</el-button>
                        <el-button @click="onPwdCancelAsync">取消</el-button>
                    </el-form-item>
                </el-form>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<style scoped>
.setting {
    margin-top: 10px;
}

.setting .title {
    display: flex;
    align-items: center;
}

.setting .title .icon {
    font-size: 16px;
    color: #6d6d6d;
    margin-left: 12px;
    margin-right: 6px;
}

.setting .form {
    max-width: 80%;
    margin-left: 20px;
}
</style>