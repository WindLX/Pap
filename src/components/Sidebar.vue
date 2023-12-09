<script lang="ts" setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { useStateStore, SidebarIndex } from '@/store/state';
import { ResourceApi } from '@/api/resource';
import { downloadUrlAsync } from '@/utils';

const stateStore = useStateStore();

function select(index: string) {
    if (stateStore.sidebarIndex === (index as SidebarIndex)) {
        stateStore.isMiddleBarShow = !stateStore.isMiddleBarShow
    } else {
        stateStore.sidebarIndex = (index as SidebarIndex)
        stateStore.isMiddleBarShow = true
    }
}

async function exportDataAsync() {
    const url = await ResourceApi.exportData()
    await downloadUrlAsync('data.zip', url)
    await ResourceApi.removeZip()
}

function lock() {
    window.location.replace("/#/login")
    localStorage.removeItem("token")
}
</script>

<template>
    <div class="sidebar">
        <div class="menu">
            <font-awesome-icon :icon="['fas', 'book']" class="icon button" :class="stateStore.isActive(0)"
                @click="select(SidebarIndex.Note)" />
            <font-awesome-icon :icon="['fas', 'circle-nodes']" class="icon button" :class="stateStore.isActive(1)"
                @click="select(SidebarIndex.Net)" />
            <font-awesome-icon :icon="['fas', 'gift']" class="icon button" :class="stateStore.isActive(2)"
                @click=select(SidebarIndex.Resource) />
            <font-awesome-icon :icon="['fas', 'database']" class="icon button" :class="stateStore.isActive(3)"
                @click=select(SidebarIndex.Database) />
            <font-awesome-icon :icon="['fas', 'gear']" class="icon button" :class="stateStore.isActive(4)"
                @click="select(SidebarIndex.Setting)" />
        </div>
        <div class="menu">
            <font-awesome-icon :icon="['fas', 'file-zipper']" class="icon button" @click="exportDataAsync()" />
            <font-awesome-icon :icon="['fas', 'lock']" class="icon button" @click="lock()" />
        </div>
    </div>
</template>

<style scoped>
.sidebar {
    grid-area: sidebar;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.sidebar .menu {
    display: flex;
    flex-direction: column;
    margin: auto 0;
}

.sidebar .menu .icon {
    margin: 12px 0;
}

.sidebar .icon {
    font-size: 20px;
}

.sidebar .button {
    color: #6d6d6d;
    cursor: pointer;
}

.sidebar .button:hover {
    color: var(--el-color-primary);
}

.sidebar .active {
    color: var(--el-color-primary);
}
</style>