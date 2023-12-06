<script setup lang="ts">
import { reactive } from 'vue'
import NetNode from '../Net/NetNode.vue';
import NetLine from '../Net/NetLine.vue';

const nodes = reactive([
    {
        id: 0,
        isMd: true,
        text: "a",
        pos: {
            x: 0,
            y: 0
        }
    },
    {
        id: 1,
        isMd: false,
        text: "b",
        pos: {
            x: 0,
            y: 0
        }
    }
])

const lines = [
    {
        source: 0,
        target: 1
    }
]

function handleShowMd(id: number) {

}

</script>

<template>
    <div class="net-space">
        <svg class="net-svg">
            <defs>
                <filter id="back" x="-0.5" y="0" width="2" height="1">
                    <feFlood result="bg" flood-color="rgba(0, 0, 0, 0.3)" />
                    <feMerge>
                        <feMergeNode in="bg" />
                        <feMergeNode in="SourceGraphic" />
                    </feMerge>
                </filter>
            </defs>
            <NetLine v-for="(line, index) in lines" :key="index" :source="nodes[line.source].pos"
                :target="nodes[line.target].pos" />
            <NetNode v-for="(node, index) in nodes" :key="node.id" :id="node.id" :is-md="node.isMd" :pos="node.pos"
                :text="node.text" @update:pos="(pos) => nodes[index].pos = pos" @click="handleShowMd(node.id)" />
        </svg>
    </div>
</template>

<style scoped>
.net-space {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    user-select: none;
}

.net-space .net-svg {
    width: 100%;
    height: 100%;
}
</style>