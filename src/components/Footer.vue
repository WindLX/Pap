<script setup lang="ts">
import { useTabStore } from '../store/tab';
import { computed } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// state
const store = useTabStore()

// data
const fileName = computed(() => { return store.current.name })

</script>

<template>
    <div class="footer">
        <font-awesome-icon :icon="['fas', 'dolly']" class="icon" />
        <span class="title">{{ fileName }}</span>
    </div>
</template>

<style scoped>
.footer {
    grid-area: footer;
    display: grid;
    grid-template-columns: 24px 300px 1fr;
    grid-template-areas:
        "icon title other";
}

.footer .title {
    grid-area: title;
    font-size: 14px;
}

.footer .icon {
    grid-area: icon;
    color: #6d6d6d;
    margin-top: 2px;
}
</style>