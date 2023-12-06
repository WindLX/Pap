<script setup lang="ts">
import { ElTabPane, ElTabs, TabPaneName, ElEmpty } from 'element-plus'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { useNoteTabStore, TabState } from '@/store/tab';
import Markdown from '@/components/Markdown';

// state
const tabStore = useNoteTabStore()

// callback function
function handleRemoveTab(name: TabPaneName) {
    tabStore.removeTab(name)
}
</script>

<template>
    <div class="notespace">
        <el-tabs v-if="tabStore.length !== 0" type="border-card" closable :model-value="tabStore.currentIndex"
            @update:model-value="(value) => tabStore.currentIndex = value" @tab-remove="handleRemoveTab" class="pane">
            <el-tab-pane v-for="(item, index) in tabStore.tabs" :key="item.id" :label="item.name" :name="index"
                class="pane">
                <template #label>
                    <span id="not-print">
                        <font-awesome-icon v-show="item.state.has(TabState.Lock)" :icon="['fas', 'lock']"
                            class="icon s-icon" />
                        <font-awesome-icon v-show="!item.state.has(TabState.Save)" :icon="['fas', 'clock-rotate-left']"
                            class="icon s-icon" />
                        <font-awesome-icon :icon="['fas', 'file']" class="icon" />
                        <span class="pane-title">{{ item.name }}</span>
                    </span>
                </template>
                <Markdown :id="item.id" @lock="(lock) => tabStore.updateState(TabState.Lock, lock, index)"
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
    height: calc(100vh - 16px);
}

.notespace .pane {
    height: 100%;
}

.notespace .pane-title {
    margin-left: 6px;
    user-select: none;
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