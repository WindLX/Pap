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
        <div id="file-name">
            <font-awesome-icon :icon="['fas', 'box-open']" class="icon" />
            <span>{{ fileName }}</span>
        </div>
    </div>
</template>

<style scoped>
.footer {
    grid-area: footer;
    display: grid;
    grid-template-columns: 48px 24px 1fr;
    grid-template-areas:
        "title title title";
}

.footer #file-name {
    margin: 0;
    grid-area: title;
    font-size: 14px;
    display: flex;
    align-items: center;
}

.footer .icon {
    color: #6d6d6d;
    margin-right: 6px;
}
</style>