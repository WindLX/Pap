<script setup lang="ts">
import { ref, reactive, onActivated } from 'vue'
import { ElForm, ElFormItem, ElInput, ElTooltip, ElCollapse, ElCollapseItem, ElButton, ElNotification, ElSlider } from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { IBasicConfig, IPathConfig } from '../utils/config'
import { useStateStore } from '../store/state'

// const
const marks = reactive<Record<number, string>>({ 0: '调试', 1: '消息', 2: '警告', 3: '错误' })
const levelStringMap = ["DEBUG", "INFO", "WARNING", "ERROR"];
const levelMap = new Map([["DEBUG", 0], ["INFO", 1], ["WARNING", 2], ["ERROR", 3]])

// state
const store = useStateStore()

// data
let logLevel = ref(0)
let basicConfig = reactive<IBasicConfig>({
    title: "Pap",
    log_level: "INFO"
})

let pathConfig = reactive<IPathConfig>({
    content_dir: ".",
    log_path: ".",
    tag_path: "."
})

// tool function
function numberToLogLevel(level: number): string {
    return levelStringMap[level] || "INFO";
}

function logLevelToNumber(level: string): number {
    return levelMap.get(level) || 1;
}

// callback function
async function onPathSubmit() {
    const response = await fetch(`${store.backendHost}/config/set_config/path`, {
        method: 'PUT', mode: 'cors', headers: { 'content-type': 'application/json' }, body: JSON.stringify(pathConfig)
    })
    if (response.status == 202) {
        ElNotification({
            title: '修改成功',
            message: '路径设置修改成功',
            type: 'success',
            duration: 2000
        })
    }
    else {
        onPathCancel()
        ElNotification({
            title: '修改失败',
            message: `路径设置修改失败:${response.statusText}`,
            type: 'error',
            duration: 2000
        })
    }
}

async function onBasicSubmit() {
    basicConfig.log_level = numberToLogLevel(logLevel.value)
    const response = await fetch(`${store.backendHost}/config/set_config/basic`, {
        method: 'PUT', mode: 'cors', headers: { 'content-type': 'application/json' }, body: JSON.stringify(basicConfig)
    })
    if (response.status == 202) {
        ElNotification({
            title: '修改成功',
            message: '基础设置修改成功,将在应用重启后生效',
            type: 'success',
            duration: 2000
        })
    } else {
        onBasicCancel()
        ElNotification({
            title: '修改失败',
            message: `基础设置修改失败:${response.statusText}`,
            type: 'error',
            duration: 2000
        })
    }
}

async function onPathCancel() {
    const response = await fetch(`${store.backendHost}/config/get_config/path`, { method: 'GET', mode: 'cors' })
    const data = await response.json() as IPathConfig
    pathConfig.content_dir = data.content_dir
    pathConfig.log_path = data.log_path
    pathConfig.tag_path = data.tag_path
}

async function onBasicCancel() {
    const response = await fetch(`${store.backendHost}/config/get_config/basic`, { method: 'GET', mode: 'cors' })
    const data = await response.json() as IBasicConfig
    basicConfig.log_level = data.log_level
    basicConfig.title = data.title
    logLevel.value = logLevelToNumber(basicConfig.log_level)
}

// hook
onActivated(() => {
    onBasicCancel()
    onPathCancel()
})
</script>

<template>
    <div class="setting">
        <el-collapse accordion>
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
                        <el-button type="primary" @click="onBasicSubmit">提交</el-button>
                        <el-button @click="onBasicCancel">取消</el-button>
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
                    <el-tooltip content="生成的附加内容存放的路径" :offset="6">
                        <el-form-item label="内容路径">
                            <el-input v-model="pathConfig.content_dir"></el-input>
                        </el-form-item>
                    </el-tooltip>
                    <el-tooltip content="标签存放的路径" :offset="6">
                        <el-form-item label="标签路径">
                            <el-input v-model="pathConfig.tag_path"></el-input>
                        </el-form-item>
                    </el-tooltip>
                    <el-tooltip content="日志文件存放的路径" :offset="6">
                        <el-form-item label="日志路径">
                            <el-input v-model="pathConfig.log_path"></el-input>
                        </el-form-item>
                    </el-tooltip>
                    <el-form-item>
                        <el-button type="primary" @click="onPathSubmit">提交</el-button>
                        <el-button @click="onPathCancel">取消</el-button>
                    </el-form-item>
                </el-form>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<style scoped>
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