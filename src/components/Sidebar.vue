<script lang="ts">
import { ElMenu, ElMenuItem, ElButton } from 'element-plus'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { useStateStore, SidebarIndex, ContentIndex } from '@/store/state';

export default {
    components: {
        ElMenu,
        ElMenuItem,
        ElButton,
        FontAwesomeIcon
    },
    setup() {
        const stateStore = useStateStore();
        return {
            stateStore,
            SidebarIndex
        }
    },
    methods: {
        select(index: string) {
            if (this.stateStore.sidebarIndex === (index as SidebarIndex)) {
                this.stateStore.isMiddleBarShow = !this.stateStore.isMiddleBarShow
            } else {
                this.stateStore.sidebarIndex = (index as SidebarIndex)
                if (["net", "note", "database"].includes(index)) {
                    this.stateStore.contentIndex = (index as ContentIndex)
                }
                this.stateStore.isMiddleBarShow = true
            }
        },
        lock() {
            window.location.replace("/#/login")
            localStorage.removeItem("token")
        }
    }
}

</script>

<template>
    <div class="sidebar">
        <el-menu @select="select" default-active="note">
            <el-menu-item class="menu-item" :index="SidebarIndex.Note">
                <font-awesome-icon :icon="['fas', 'book']" class="icon" />
            </el-menu-item>
            <el-menu-item class="menu-item" :index="SidebarIndex.Net">
                <font-awesome-icon :icon="['fas', 'circle-nodes']" class="icon" />
            </el-menu-item>
            <el-menu-item class="menu-item" :index="SidebarIndex.Database">
                <font-awesome-icon :icon="['fas', 'database']" class="icon" />
            </el-menu-item>
            <el-menu-item class="menu-item" :index="SidebarIndex.Setting">
                <font-awesome-icon :icon="['fas', 'gear']" class="icon" />
            </el-menu-item>
        </el-menu>
        <font-awesome-icon :icon="['fas', 'lock']" class="icon button" @click="lock()" />
    </div>
</template>

<style scoped>
.sidebar {
    grid-area: sidebar;
    display: flex;
    flex-direction: column;
}

.sidebar .menu-item {
    justify-content: center;
}

.sidebar .icon {
    font-size: 20px;
}

.sidebar .menu-item .icon {
    font-size: 20px;
}

.sidebar .menu-item:not(.is-active) .icon {
    color: #6d6d6d;
}

.sidebar .button {
    color: #6d6d6d;
    cursor: pointer;
    margin-top: 16px;
}

.sidebar .button:hover {
    color: var(--el-color-primary);
}
</style>
<style>
.el-menu {
    border-right: none;
}

.el-menu-item {
    height: 48px;
}
</style>