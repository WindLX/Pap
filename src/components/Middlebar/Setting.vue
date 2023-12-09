<script setup lang="ts">
import { ref, reactive, onActivated, onMounted } from 'vue'
import {
    ElForm, ElFormItem, ElInput,
    ElCollapse, ElCollapseItem, ElButton,
    ElSlider, ElInputNumber
} from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ConfigApi } from '@/api/config';
import type {
    SystemConfigSchema,
    BasicConfigSchema,
} from '@/schemas/config';
import {
    Section,
    systemConfigDefault,
    basicConfigDefault,
} from '@/schemas/config';
import type { LoginSchema } from '@/schemas/token';
import { loginDefault } from '@/schemas/token';


// const
const marks = reactive<Record<number, string>>({ 0: '调试', 1: '消息', 2: '警告', 3: '错误' })
const levelStringMap = ["DEBUG", "INFO", "WARNING", "ERROR"];
const levelMap = new Map([["DEBUG", 0], ["INFO", 1], ["WARNING", 2], ["ERROR", 3]])

// data
let logLevel = ref(0)
let systemConfig = ref<SystemConfigSchema>(systemConfigDefault())
let basicConfig = ref<BasicConfigSchema>(basicConfigDefault())
let pwd = ref<LoginSchema>(loginDefault())

// tool function
function numberToLogLevel(level: number): string {
    return levelStringMap[level] || "INFO";
}

function logLevelToNumber(level: string): number {
    return levelMap.get(level) || 1;
}

// callback function
function handleSystemSubmit() {
    ConfigApi.setConfig(Section.System, systemConfig.value)
}

function handleBasicSubmit() {
    basicConfig.value.log_level = numberToLogLevel(logLevel.value)
    ConfigApi.setConfig(Section.Basic, basicConfig.value)
}

function handlePwdSubmit() {
    ConfigApi.setPwd(pwd.value)
}

function handleSystemCancel() {
    systemConfig.value = systemConfigDefault()
}

async function handleBasicCancelAsync() {
    basicConfig.value = await ConfigApi.getConfig(Section.Basic) as BasicConfigSchema
    logLevel.value = logLevelToNumber(basicConfig.value.log_level)
}

function handlePwdCancel() {
    pwd.value = loginDefault()
}

// hook
onMounted(async () => {
    handleSystemCancel()
    await handleBasicCancelAsync()
})

onActivated(async () => {
    handleSystemCancel()
    await handleBasicCancelAsync()
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
                        <el-button type="primary" @click="handleSystemSubmit">提交</el-button>
                        <el-button @click="handleSystemCancel">取消</el-button>
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
                        <el-button type="primary" @click="handleBasicSubmit">提交</el-button>
                        <el-button @click="handleBasicCancelAsync">取消</el-button>
                    </el-form-item>
                </el-form>
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
                        <el-button type="primary" @click="handlePwdSubmit">提交</el-button>
                        <el-button @click="handlePwdCancel">取消</el-button>
                    </el-form-item>
                </el-form>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<style scoped>
.setting {
    margin-top: 10px;
    width: 95%;
    transform: translateX(2.5%);
    border-radius: 10px;
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