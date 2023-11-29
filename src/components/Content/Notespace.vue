<script setup lang="ts">
import { ref, provide } from 'vue'
import { ElTabPane, ElTabs, TabPaneName, ElEmpty } from 'element-plus'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { TabState } from '@/types/tab-types'
import { tab } from '@store';
import Markdown from '@components/Markdown';

// state
const tabStore = tab.useNoteTabStore()

// data
let currentTabIndex = ref(tabStore.currentIndex)
let tabs = ref(tabStore.tabs)

tabStore.$subscribe((_mutation, state) => {
    currentTabIndex.value = state.currentIndex
    tabs.value = state.tabs
})

provide('tabStore', tabStore)

// callback function
async function handleRemoveTabAsync(name: TabPaneName) {
    tabStore.currentIndex = 0
    tabStore.tabs = tabs.value.filter((_tab, index) => index != name)
}
</script>

<template>
    <div class="notespace">
        <el-tabs v-if="tabs.length !== 0" type="border-card" closable :model-value="currentTabIndex"
            @tab-remove="handleRemoveTabAsync" style="height: 100%;">
            <el-tab-pane v-for="(item, index) in tabs" :key="index" :label="item.name" :name="index" style="height: 100%;">
                <template #label>
                    <span id="not-print">
                        <font-awesome-icon v-show="item.state.has(TabState.Lock)" :icon="['fas', 'lock']"
                            class="icon s-icon" />
                        <font-awesome-icon v-show="!item.state.has(TabState.Save)" :icon="['fas', 'clock-rotate-left']"
                            class="icon s-icon" />
                        <font-awesome-icon :icon="['fas', 'file']" class="icon" />
                        <span style="margin-left: 6px;user-select: none;">{{ item.name }}</span>
                    </span>
                </template>
                <Markdown :id="item.id" :is-note="true" @lock="(lock) => tabStore.updateState(TabState.Lock, lock, index)"
                    @save="(save) => tabStore.updateState(TabState.Save, save, index)" />
            </el-tab-pane>
        </el-tabs>
        <el-empty v-else class="empty" />
    </div>
</template>

<style scoped>
.notespace {
    grid-area: content;
    display: flex;
    flex-direction: column;
    height: inherit;
}

.notespace .empty {
    margin: auto;
}

.notespace .icon {
    margin-right: 3px;
}

.notespace .icon.s-icon {
    font-size: 10px;
    vertical-align: baseline;
}
</style>

<style>
.el-tabs__content {
    height: 90%;
}
</style>