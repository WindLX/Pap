<script setup lang="ts">
import { computed } from 'vue';
import { useStateStore, ContentIndex } from '@/store/state'
import Notespace from './Notespace.vue';
import Resourcespace from './Resourcespace.vue';
import Netspace from './Netspace.vue';

// state
const store = useStateStore();

// content
const currentComponent = computed(() => {
    switch (store.contentIndex) {
        case ContentIndex.Note:
            return Notespace
        case ContentIndex.Net:
            return Netspace
        case ContentIndex.Resource:
            return Resourcespace
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