<script setup lang="ts">
import { onActivated, onDeactivated, onMounted, ref } from 'vue'
import { JsSystem } from 'sim';
import { Vector, NetConfig, NetNodeSchema, NetLinkSchema } from "@/schemas/net";
import { useNoteTabStore } from '@/store/tab';
import { useStateStore } from '@/store/state';
import { NoteApi } from '@/api/note';
import { NetApi } from "@/api/net";
import NetNode from '../Net/NetNode.vue';
import NetLine from '../Net/NetLine.vue';

const nodes = ref<Array<NetNodeSchema>>([])

const lines = ref<Array<NetLinkSchema>>([])

const stateStore = useStateStore()
const tabStore = useNoteTabStore()

let system: JsSystem | null = null
let config: NetConfig | null = null

const svgRef = ref<SVGSVGElement | null>(null)
const timer = ref<number | null>(null)

const netStep = () => {
    if (config !== null && system && nodes.value.length > 0) {
        let pos = system.step()
        nodes.value.forEach((n, index) => {
            let new_pos = pos[index]
            if (Number.isNaN(new_pos.x) || Number.isNaN(new_pos.y)) {
                let radius = n.is_md ? config!.md_radius : config!.res_radius
                new_pos.x = config!.max_x - radius
                new_pos.y = config!.max_y - radius
            }
            n.pos = new_pos
        })
    }
}

function handleShowMd(id: number) {
    NoteApi.getNote(id).then((note) => {
        tabStore.addTab(note)
        stateStore.select(0)
    })
}

function handleUpdatePos(index: number, pos: Vector) {
    nodes.value[index].pos = pos
    if (system) {
        system.set_pos(index, pos)
    }
}

async function loadNetAsync() {
    const net = await NetApi.get_net()
    nodes.value = net.nodes
    lines.value = net.links
    system = JsSystem.new(nodes.value, lines.value, config)
    timer.value = window.setInterval(netStep, 20)
}

onMounted(async () => {
    let max_x = 100
    let max_y = 100
    if (svgRef) {
        max_x = svgRef.value?.clientWidth!
        max_y = svgRef.value?.clientHeight!
    }
    config = {
        md_radius: 30,
        res_radius: 15,
        md_length: 80.0,
        res_length: 50.0,
        origin_x: max_x / 2,
        origin_y: max_y / 2,
        max_x,
        max_y,
        stiffness: 30,
        gravitation_weight: 1,
        gravitation_bais: 150,
        md_mass: 5,
        res_mass: 1,
        mu: 30
    }
    await loadNetAsync()
})

onActivated(async () => {
    await loadNetAsync()
})

onDeactivated(() => {
    if (timer.value) {
        window.clearInterval(timer.value);
    }
})
</script>

<template>
    <div class="net-space">
        <h1 class="net-top">
            引用网络
        </h1>
        <svg class="net-svg" ref="svgRef">
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
            <NetNode v-if="config" v-for="(node, index) in nodes" :key="index"
                :radius="[config.md_radius, config.res_radius]" :is-md="node.is_md" :pos="node.pos"
                :bound="[config.max_x, config.max_y]" :text="node.data" @update:pos="(pos) => handleUpdatePos(index, pos)"
                @click="handleShowMd(node.id)" />
        </svg>
    </div>
</template>

<style scoped>
.net-space {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: calc(100vw);
    height: 100%;
    user-select: none;
}

.net-space .net-top {
    font-size: 32px;
    font-weight: bold;
}

.net-space .net-svg {
    width: 100%;
    height: 100%;
}
</style>