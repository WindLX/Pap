<script lang="ts" setup>
import Middlebar from "@/components/Middlebar";
import Sidebar from "@/components/Sidebar.vue";
import Content from "@/components/Content";
import TagDrawer from "@/components/Tag/TagDrawer.vue";
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
    grid-template-columns: 48px auto 1fr;
    grid-template-areas:
        "sidebar middlebar content";
    gap: 1px;
    height: calc(100vh - 16px);
}

@media screen and (max-width: 900px) {
    .container {
        grid-template-columns: 48px 1fr;
        grid-template-areas:
            "sidebar content";
        gap: 1px;
        height: calc(100vh - 16px);
    }
}
</style>