<script lang="ts">
import { useStateStore, SidebarIndex } from '@/store/state';
import Note from './Note.vue';
import Database from './Database.vue';
import Setting from './Setting.vue';

export default {
    setup() {
        const stateStore = useStateStore()
        return {
            stateStore,
            SidebarIndex
        }
    },
    computed: {
        currentComponent() {
            switch (this.stateStore.sidebarIndex) {
                case SidebarIndex.Note:
                    return Note
                case SidebarIndex.Database:
                    return Database
                case SidebarIndex.Setting:
                    return Setting
                default:
                    return Note
            }
        },
        currentTitle() {
            switch (this.stateStore.sidebarIndex) {
                case SidebarIndex.Note:
                    return '笔记'
                case SidebarIndex.Database:
                    return '数据库'
                case SidebarIndex.Setting:
                    return '设置'
                default:
                    return '笔记'
            }
        },
    }
}
</script>

<template>
    <transition name="accept">
        <div class="middlebar" v-show="stateStore.isMiddleBarShow" v-if="stateStore.sidebarIndex != SidebarIndex.Net">
            <p class="title">{{ currentTitle }}</p>
            <keep-alive>
                <transition name="change">
                    <component :is="currentComponent" />
                </transition>
            </keep-alive>
        </div>
    </transition>
</template>

<style scoped>
.middlebar {
    grid-area: middlebar;
    flex-direction: column;
    user-select: none;
    width: 320px;
}

.accept-enter-active {
    animation: accept-in 0.3s;
}

.accept-leave-active {
    animation: accept-in 0.3s reverse;
}

@keyframes accept-in {
    0% {
        width: 0px;
        opacity: 0;
    }

    100% {
        opacity: 1;
    }
}

.change-enter-active {
    animation: change-in 0.3s;
}

.change-leave-active {
    animation: change-in 0.3s reverse;
}

.change-leave-to {
    display: none;
}

@keyframes change-in {
    0% {
        opacity: 0;
    }

    100% {
        opacity: 1;
    }
}

.middlebar p {
    font-size: 14px;
    margin: 0;
    margin-top: 10px;
    padding: 0;
    padding-left: 8px;
    width: 92%;
    text-align: center;
}

@media screen and (max-width: 900px) and (min-width:540px) {
    .middlebar {
        z-index: 100;
        left: 57px;
        width: 320px;
        height: calc(100vh - 12px);
        position: absolute;
        display: flex;
        flex-direction: column;
        user-select: none;
        background-color: #fff;
        border: 1px solid #e5e5e5;
    }

    .middlebar .title {
        margin-top: 6px;
    }

    .accpet-enter-active {
        animation: por-width-in 0.3s;
    }

    .accpet-leave-active {
        animation: por-width-in 0.3s reverse;
    }
}

@media screen and (max-width: 540px) {
    .middlebar {
        z-index: 100;
        left: 57px;
        width: calc(100vw - 60px);
        height: calc(100vh - 12px);
        position: absolute;
        display: flex;
        flex-direction: column;
        user-select: none;
        background-color: #fff;
        border: 1px solid #e5e5e5;
    }

    .middlebar .title {
        margin-top: 6px;
    }

    .accpet-enter-active {
        animation: por-width-in 0.3s;
    }

    .accpet-leave-active {
        animation: por-width-in 0.3s reverse;
    }
}

@keyframes por-width-in {
    0% {
        width: 0px;
        opacity: 0;
    }

    100% {
        width: calc(100vw - 60px);
        opacity: 1;
    }
}
</style>