<script setup lang="ts">
import { ElMenu, ElMenuItem, ElTooltip } from 'element-plus'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { useStateStore, SidebarIndex } from '../store/state';

// state
const stateStore = useStateStore();

// callback function
function select(index: string) {
    if (stateStore.sidebarIndex === (index as SidebarIndex)) {
        stateStore.isMiddleBarShow = !stateStore.isMiddleBarShow
    } else {
        stateStore.sidebarIndex = (index as SidebarIndex)
        stateStore.isMiddleBarShow = true
    }
}
</script>

<template>
    <div class="sidebar">
        <el-menu @select="select" default-active="resource" style="height: 100%;">
            <el-tooltip content="工作区" placement="right">
                <el-menu-item class="menu-item" index="resource">
                    <font-awesome-icon :icon="['fas', 'file']" class="icon" />
                </el-menu-item>
            </el-tooltip>
            <el-tooltip content="时间线" placement="right">
                <el-menu-item class="menu-item" index="timeline">
                    <font-awesome-icon :icon="['fas', 'route']" class="icon" />
                </el-menu-item>
            </el-tooltip>
            <el-tooltip content="设置" placement="right">
                <el-menu-item class="menu-item" index="setting">
                    <font-awesome-icon :icon="['fas', 'gear']" class="icon" />
                </el-menu-item>
            </el-tooltip>
        </el-menu>
    </div>
</template>

<style scoped>
.sidebar {
    grid-area: sidebar;
}

.sidebar .menu-item {
    justify-content: center;
}

.sidebar .menu-item .icon {
    font-size: 20px;
}

.sidebar .menu-item:not(.is-active) .icon {
    color: #6d6d6d;
}
</style>