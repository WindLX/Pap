<script setup lang="ts">
import { ref } from 'vue'
import { ElTabPane, ElTabs, TabPaneName } from 'element-plus'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { useTabStore } from '../store/tab';
import { TabDataType } from '../types/tab-types';
import PDFViewer from './PDFViewer.vue'

// state
const tabStore = useTabStore()

// data
let currentTabIndex = ref(tabStore.currentIndex)
let tabs = ref(tabStore.tabs)

tabStore.$subscribe((_mutation, state) => {
    currentTabIndex.value = state.currentIndex
    tabs.value = state.tabs
})

// callback function
async function removeTab(name: TabPaneName) {
    tabStore.currentIndex = 0
    tabStore.tabs = tabs.value.filter((_tab, index) => index != name)
}
</script>

<template>
    <div class="content">
        <el-tabs type="border-card" closable :model-value="currentTabIndex" @tab-remove="removeTab" style="height: 100%;">
            <el-tab-pane v-for="(item, index) in tabs" :key="index" :label="item.name" :name="index" style="height: 100%;">
                <template #label>
                    <span>
                        <font-awesome-icon :icon="['fas', item.typ === TabDataType.ResourceItem ? 'file' : 'note-sticky']"
                            class="icon" />
                        <span style="margin-left:9px">{{ item.name }}</span>
                    </span>
                </template>
                <PDFViewer v-if="item.typ === TabDataType.ResourceItem" :id="item.id">
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