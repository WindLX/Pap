<script setup lang="ts">
import { ElTabPane, ElTabs, TabPaneName } from 'element-plus'
import { ref } from 'vue'
import { useTabStore, isResultItem } from '../store/tab';
import { useStateStore } from '../store/state';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import PDFViewer from './PDFViewer.vue'

// state
const store = useTabStore()
const stateStote = useStateStore()

// data
let currentTabIndex = ref(store.currentIndex)
let tabs = ref(store.tabs)
// const pdfFile = ref()

store.$subscribe((_mutation, state) => {
    currentTabIndex.value = state.currentIndex
    tabs.value = state.tabs
})

// callback function
async function removeTab(name: TabPaneName) {
    store.currentIndex = 0
    store.tabs = tabs.value.filter((_tab, index) => index != name)
}
</script>

<template>
    <div class="content">
        <el-tabs type="border-card" closable :model-value="currentTabIndex" @tab-remove="removeTab" style="height: 100%;">
            <el-tab-pane v-for="(item, index) in tabs" :key="index" :label="item.name" :name="index" style="height: 100%;">
                <template #label>
                    <span>
                        <font-awesome-icon :icon="['fas', isResultItem(item) ? 'file' : 'note-sticky']" class="icon" />
                        <span style="margin-left:9px">{{ item.name }}</span>
                    </span>
                </template>
                <PDFViewer :pdf="`${stateStote.backendHost}/${item.url}`" :id="`${isResultItem(item) ? 'r' : 'c'}${item.id}`"
                    v-if="isResultItem(item)">
                </PDFViewer>
                <!-- <iframe v-else width="100%" height="100%" /> -->
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<style scoped>
.content {
    grid-area: content;
    display: flex;
    flex-direction: column;
    height: inherit;
}
</style>

<style>
.el-tabs__content {
    height: 90%;
}
</style>