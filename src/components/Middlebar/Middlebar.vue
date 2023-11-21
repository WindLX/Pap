<script lang="ts">
import { state } from '@store'
import House from './House.vue';
import Resource from './Resource.vue'
import Note from './Note.vue';
import Setting from './Setting.vue';
import Timeline from './Timeline.vue';

export default {
    setup() {
        const stateStore = state.useStateStore()
        return {
            stateStore
        }
    },
    computed: {
        currentComponent() {
            switch (this.stateStore.sidebarIndex) {
                case state.SidebarIndex.House:
                    return House
                case state.SidebarIndex.Resource:
                    return Resource
                case state.SidebarIndex.Note:
                    return Note
                case state.SidebarIndex.Timeline:
                    return Timeline
                case state.SidebarIndex.Setting:
                    return Setting
                default:
                    return Resource
            }
        },
        currentTitle() {
            switch (this.stateStore.sidebarIndex) {
                case state.SidebarIndex.House:
                    return '主页'
                case state.SidebarIndex.Resource:
                    return '工作区'
                case state.SidebarIndex.Note:
                    return '笔记区'
                case state.SidebarIndex.Timeline:
                    return '时间线'
                case state.SidebarIndex.Setting:
                    return '设置'
                default:
                    return '主页'
            }
        },
        isShow() {
            return this.stateStore.isMiddleBarShow;
        }
    }
}
</script>

<template>
    <div class="middlebar" v-show="isShow">
        <p>{{ currentTitle }}</p>
        <keep-alive>
            <component :is="currentComponent"></component>
        </keep-alive>
    </div>
</template>

<style scoped>
.middlebar {
    grid-area: middlebar;
    display: flex;
    flex-direction: column;
    user-select: none;
}

.middlebar p {
    font-size: 14px;
    margin: 0;
    margin-left: 2.5%;
    padding: 0;
    padding-left: 8px;
    width: 92%;
    background-color: #f4f4f4;
}
</style>