<script setup lang="ts">
import { computed } from 'vue';
import { useStateStore, SidebarIndex } from '../store/state'
import Resource from './Resource.vue'
import Setting from './Setting.vue';
import Timeline from './Timeline.vue';

// state
const store = useStateStore();

// content
const currentComponent = computed(() => {
    switch (store.sidebarIndex) {
        case SidebarIndex.Resource:
            return Resource
        case SidebarIndex.Timeline:
            return Timeline
        case SidebarIndex.Setting:
            return Setting
        default:
            return Resource
    }
});

const currentTitle = computed(() => {
    switch (store.sidebarIndex) {
        case SidebarIndex.Resource:
            return '工作区'
        case SidebarIndex.Timeline:
            return '时间线'
        case SidebarIndex.Setting:
            return '设置'
        default:
            return '工作区'
    }
});

// style
const isShow = computed(() => store.isMiddleBarShow);
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