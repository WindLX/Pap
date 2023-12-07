<script setup lang="ts">
import { onMounted, reactive } from 'vue'
import { JsSystem } from 'sim';
import NetNode from '../Net/NetNode.vue';
import NetLine from '../Net/NetLine.vue';

const nodes = reactive([
    {
        id: 0,
        is_md: true,
        data: "a",
        pos: {
            x: 0,
            y: 0
        }
    },
    {
        id: 1,
        is_md: false,
        data: "b",
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

const config = {
    origin_x: 50.0,
    origin_y: 50.0,
    origin_length: 50.0,
    stiffness: 3.0,
    gravitation_weight: 1.0,
    gravitation_bais: -30.0,
    md_mass: 10.0,
    res_mass: 1.0,
}

function handleShowMd(id: number) {

}

onMounted(() => {
    const system = JsSystem.new(nodes, lines, config)
    let a = system.step()
    console.log(a)
})
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