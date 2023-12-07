<script setup lang="ts">
import { onMounted, ref } from 'vue';
import TreeItem from './TreeItem.vue';

const props = defineProps<{
    rawData: TreeCreateNode[];
}>()

defineEmits<{
    (e: 'nodeClick', line: number): void
}>()

const tree = ref<TreeNode | null>(null)

export interface TreeCreateNode {
    level: number,
    id: number,
    data: any
}

export interface TreeNode {
    level: number,
    id: number,
    data: any;
    parent?: TreeNode;
    children: TreeNode[];
}

function arrayToTree(rawData: TreeCreateNode[]): TreeNode {
    const tree = <TreeNode>{
        level: 0,
        id: 0,
        data: null,
        children: [],
    }
    var t = tree
    rawData.forEach((data) => {
        const treeNode: TreeNode = {
            id: data.id,
            level: data.level,
            data: data.data,
            children: []
        };
        t = insertTree(t, treeNode)
    });

    return tree;
}

function insertTree(targetNode: TreeNode, newNode: TreeNode): TreeNode {
    if (targetNode.level === newNode.level) {
        newNode.parent = targetNode.parent;
        targetNode.parent!.children.push(newNode);
        return newNode;
    } else if (targetNode.level < newNode.level) {
        if (targetNode.children.length === 0 || targetNode.children.at(-1)!.level > newNode.level) {
            newNode.parent = targetNode;
            targetNode.children.push(newNode);
            return newNode;
        } else {
            return insertTree(targetNode.children.at(-1)!, newNode)
        }
    } else {
        return insertTree(targetNode.parent!, newNode)
    }
}

onMounted(() => {
    tree.value = arrayToTree(props.rawData)
})
</script>

<template>
    <div class="tree-container">
        <TreeItem v-if="tree" :treeData="tree" @nodeClick="(id) => $emit('nodeClick', id)" />
    </div>
</template>

<style scoped>
.tree-container {
    width: 300px;
    max-width: 300px;
}
</style>