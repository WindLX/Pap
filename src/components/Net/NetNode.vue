<script setup lang="ts">
import { computed, ref, reactive } from 'vue';

const props = defineProps<{
    id: number
    isMd: boolean
    text: string
    pos: Vector
}>()

const emits = defineEmits<{
    (e: 'update:pos', pos: Vector): void
    (e: 'click'): void
}>()

const isHover = ref(false)
let isDragging = ref(false);
const pos = reactive(props.pos);

type Vector = {
    x: number,
    y: number
}

const radius = computed(() => {
    return props.isMd ? 30 : 15
})

const color = computed(() => {
    return props.isMd ? '#409eff' : '#e6a23c'
})

function handleDrag(event: MouseEvent) {
    if (isDragging.value) {
        pos.x = event.clientX - 50;
        pos.y = event.clientY;
        emits("update:pos", pos)
    }
}

function handleClick() {
    if (props.isMd) {
        emits('click')
    }
}
</script>

<template>
    <g @mouseenter="isHover = true" @mouseleave="isHover = false" @dblclick="handleClick" class="node"
        @mousedown="isDragging = true" @mousemove="handleDrag" @mouseup="isDragging = false">
        <circle :cx="pos.x" :cy="pos.y" :r="radius" :fill="color" />
        <Transition name="fade">
            <text v-show="isHover" :x="pos.x" :y="pos.y" alignment-baseline="middle" text-anchor="middle" fill="#fff"
                filter="url(#back)">{{ props.text }}</text>
        </Transition>
    </g>
</template>

<style scoped>
.node {
    cursor: grab;
}

.fade-enter-active {
    animation: fade 0.5s;
}

.fade-leave-active {
    animation: fade 0.5s reverse;
}

@keyframes fade {
    0% {
        opacity: 0;
    }

    100% {
        opacity: 1;
    }
}
</style>