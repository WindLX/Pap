<script setup lang="ts">
import { computed, ref } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import type { TreeNode } from "./Tree.vue"

const props = defineProps<{
    treeData: TreeNode;
}>()

const emits = defineEmits<{
    (e: 'nodeClick', line: number): void
}>()

const isFold = ref<boolean>(false)

const isRoot = computed(() => {
    return props.treeData.data == null
})
const ownChildren = computed(() => {
    return props.treeData.children.length > 0
})

function handleFold() {
    isFold.value = !isFold.value
}
</script>

<template>
    <div class="tree-item">
        <div class="tree-label" v-if="!isRoot">
            <font-awesome-icon v-if="ownChildren" :icon="['fas', `chevron-${isFold ? 'right' : 'down'}`]" class="icon"
                @mousedown="handleFold()" />
            <div class="label" @mousedown="$emit('nodeClick', props.treeData.id)" @dblclick="handleFold()">
                {{ props.treeData.data }}
            </div>
        </div>
        <div v-if="ownChildren" v-show="!isFold" class="tree-childen" :class="{ 'root-children': isRoot }">
            <div v-for="(child, index) in props.treeData.children" :key="index">
                <TreeItem :treeData="child" @nodeClick="(id) => $emit('nodeClick', id)" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.tree-item {
    width: 100%;
    display: flex;
    flex-direction: column;
}

.tree-item .tree-label {
    position: relative;
}

.tree-item .tree-label:hover {
    background-color: #f4f4f4;
}

.tree-item .icon {
    font-size: 16px;
    color: #aaa;
    position: absolute;
    top: 8px;
    left: 4px;
}

.tree-item .icon:hover {
    color: var(--el-color-primary);
}

.tree-item .label {
    font-size: 20px;
    cursor: pointer;
    padding-left: 24px;
    overflow: hidden;
    word-break: break-all;
    text-overflow: ellipsis;
    display: block;
}

.tree-item .label:hover {
    text-decoration: underline;
    color: var(--el-color-primary);
}

.tree-item .tree-childen {
    padding-left: 18px;
}

.tree-item .root-children {
    padding-left: 0px;
}
</style>