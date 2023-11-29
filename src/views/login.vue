<script lang="ts">
import { ref } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { Token } from '@/types/token-types'
import { state } from '@store'
import pFetch from '@utils/fetch'

export default {
    components: {
        FontAwesomeIcon
    },
    setup() {
        let password = ref("")
        const stateStore = state.useStateStore()
        return {
            stateStore,
            password
        }
    },
    methods: {
        async onEnter(e: KeyboardEvent) {
            if (e.key === 'Enter') {
                e.preventDefault()
                await this.login()
            }
        },
        async login() {
            await pFetch('/login/', {
                method: 'POST',
                body: JSON.stringify({ password: this.password }),
                successCallback: async (res) => {
                    if (res.status === 200) {
                        const token = await res.json() as Token
                        localStorage.setItem('token', token.access_token)
                        window.location.replace('/')
                    }
                }
            })
            this.password = ""
        }
    }
}
</script>

<template>
    <div class="login">
        <div class="login-form" @keydown="onEnter">
            <font-awesome-icon :icon="['fas', 'lock']" class="icon" />
            <input v-model="password" type="password" name="password" placeholder="密码" />
            <button @click="login()">登录</button>
        </div>
    </div>
</template>

<style scoped>
.login {
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-image: linear-gradient(135deg, #ABDCFF 10%, #2fa8ff 100%);
    background-size: cover;
}

.login .login-form {
    width: 240px;
    height: 220px;
    display: flex;
    flex-direction: column;
    padding: 40px;
    text-align: center;
    position: relative;
    z-index: 1;
    background-color: #ABDCFF;
    box-shadow: inset 0 0 0 3000px rgba(255, 255, 255, 0.3);
    border-radius: 18px;
    overflow: hidden;
    box-shadow: inset 0 0 0 200px rgba(255, 255, 255, 0.3);
}

.login-form h2 {
    font-size: 18px;
    font-weight: 400;
    color: #3d5245;
}

.login-form input,
.login-form button {
    margin: 6px 0;
    height: 36px;
    border: none;
    background-color: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
    padding: 0 14px;
    color: #3d5245;
}

.login-form input {
    outline: none;
}

.login-form button {
    cursor: pointer;
}

.login-form button:hover {
    background-color: rgba(255, 255, 255, 0.5);
}

.login .icon {
    font-size: 72px;
    color: #65b9f6;
    margin-top: 10px;
    margin-bottom: 30px;
}
</style>