<script setup lang="ts">
import { computed } from 'vue';
import { useStateStore, SidebarIndex } from '@/store/state'
import Notespace from './Notespace.vue'
import Databasespace from './Databasespace.vue';
import Settingspace from './Settingspace.vue';
import Netspace from './Netspace.vue';

// state
const store = useStateStore();

// content
const currentComponent = computed(() => {
    switch (store.sidebarIndex) {
        case SidebarIndex.Net:
            return Netspace
        case SidebarIndex.Note:
            return Notespace
        case SidebarIndex.Database:
            return Databasespace
        case SidebarIndex.Setting:
            return Settingspace
        default:
            return Notespace
    }
});
</script>

<template>
    <keep-alive>
        <component :is="currentComponent" />
    </keep-alive>
</template>