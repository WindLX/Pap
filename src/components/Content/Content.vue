<script setup lang="ts">
import { computed } from 'vue';
import { state } from '@store'
import House from './House.vue';
import Notespace from './Notespace.vue'

// state
const store = state.useStateStore();

// content
const currentComponent = computed(() => {
    switch (store.contentIndex) {
        case state.ContentIndex.House:
            return House
        case state.ContentIndex.Note:
            return Notespace
        default:
            return House
    }
});
</script>

<template>
    <keep-alive>
        <component :is="currentComponent" />
    </keep-alive>
</template>

<style scoped></style>