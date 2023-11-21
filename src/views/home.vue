<script lang="ts">
import { useStateStore } from "../store/state";
import Middlebar from "../components/Middlebar";
import Sidebar from "../components/Sidebar.vue";
import Content from "../components/Content";
import TagDrawer from "../components/TagDrawer.vue";

export default {
    components: {
        Middlebar,
        Sidebar,
        Content,
        TagDrawer
    },
    setup() {
        const store = useStateStore()
        return {
            store
        }
    },
    computed: {
        middlebarWidth() {
            return this.store.isMiddleBarShow ? '320px' : '0px'
        }
    }
}
</script>

<template>
    <div class="container">
        <Sidebar />
        <Middlebar />
        <Content />
    </div>
    <TagDrawer />
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