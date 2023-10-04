<script setup lang="ts">
import { ElTabPane, ElTabs, TabPaneName } from 'element-plus';
import { ref } from 'vue'

// let tabIndex = 2
const editableTabsValue = ref('2')
const editableTabs = ref([
    {
        title: 'Tab 1',
        name: '1',
        content: 'Tab 1 content',
    },
    {
        title: 'Tab 2',
        name: '2',
        content: 'Tab 2 content',
    },
])

// const addTab = (targetName: string) => {
//     const newTabName = `${++tabIndex}`
//     editableTabs.value.push({
//         title: 'New Tab',
//         name: newTabName,
//         content: 'New Tab content',
//     })
//     editableTabsValue.value = newTabName
// }
const removeTab = (targetName: TabPaneName) => {
    const tabs = editableTabs.value
    let activeName = editableTabsValue.value
    if (activeName === targetName) {
        tabs.forEach((tab, index) => {
            if (tab.name === targetName) {
                const nextTab = tabs[index + 1] || tabs[index - 1]
                if (nextTab) {
                    activeName = nextTab.name
                }
            }
        })
    }

    editableTabsValue.value = activeName
    editableTabs.value = tabs.filter((tab) => tab.name !== targetName)
}
</script>

<template>
    <div class="content">
        <el-tabs v-model="editableTabsValue" type="border-card" class="demo-tabs" closable @tab-remove="removeTab"
            style="height: 100%;">
            <el-tab-pane v-for="item in editableTabs" :key="item.name" :label="item.title" :name="item.name"
                style="height: 100%;">
                {{ item.content }}
                <!-- <embed src="./src/assets/riscv-sbi.pdf" type="application/pdf" width="100%" height="100%" /> -->
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<style scoped>
.content {
    grid-area: content;
    display: flex;
    flex-direction: column;
}
</style>