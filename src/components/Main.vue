<script setup lang="ts">
import Middlebar from "./Middlebar.vue";
import Sidebar from "./Sidebar.vue";
import Content from "./Content.vue";
import { computed } from "vue";
import { useStateStore } from "../store/state";

// state
const store = useStateStore()

// style
const middlebarWidth = computed(() => {
    return store.isMiddleBarShow ? '320px' : '0px'
})
</script>

<template>
    <div class="container">
        <Sidebar></Sidebar>
        <Middlebar></Middlebar>
        <Content></Content>
    </div>
</template>

<style scoped>
.container {
    display: grid;
    grid-template-columns: 48px v-bind(middlebarWidth) 1fr;
    grid-template-areas:
        "sidebar middlebar content";
    gap: 1px;
    height: calc(100vh - 16px);
}
</style>