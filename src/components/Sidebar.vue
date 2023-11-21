<script lang="ts">
import { ElMenu, ElMenuItem, ElButton } from 'element-plus'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { useStateStore, SidebarIndex, ContentIndex } from '@store/state';

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
                if (["house", "resource", "note"].includes(index)) {
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
        <el-button @click="lock()" size="small">
            <font-awesome-icon :icon="['fas', 'lock']" class="icon" @click="lock()" />
        </el-button>
        <el-menu @select="select" default-active="house" style="height: 100%;">
            <el-menu-item class="menu-item" :index="SidebarIndex.House">
                <font-awesome-icon :icon="['fas', 'house']" class="icon" />
            </el-menu-item>
            <el-menu-item class="menu-item" :index="SidebarIndex.Resource">
                <font-awesome-icon :icon="['fas', 'book']" class="icon" />
            </el-menu-item>
            <el-menu-item class="menu-item" :index="SidebarIndex.Note">
                <font-awesome-icon :icon="['fas', 'file']" class="icon" />
            </el-menu-item>
            <el-menu-item class="menu-item" :index="SidebarIndex.Timeline">
                <font-awesome-icon :icon="['fas', 'route']" class="icon" />
            </el-menu-item>
            <el-menu-item class="menu-item" :index="SidebarIndex.Setting">
                <font-awesome-icon :icon="['fas', 'gear']" class="icon" />
            </el-menu-item>
        </el-menu>
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
    font-size: 14px;
}

.sidebar .menu-item .icon {
    font-size: 20px;
}

.sidebar .menu-item:not(.is-active) .icon {
    color: #6d6d6d;
}
</style>