<script setup lang="ts">
import { computed, ref, reactive, watchEffect } from 'vue';
import { Vector } from '@/schemas/net';

const props = defineProps<{
    radius: [number, number]
    bound: [number, number]
    isMd: boolean
    text: string
    pos: Vector
}>()

const emits = defineEmits<{
    (e: 'update:pos', pos: Vector): void
    (e: 'click'): void
}>()

const isShowText = ref(false)
const isDragging = ref(false);
const pos = reactive(props.pos);

const radius = computed(() => {
    return props.isMd ? props.radius[0] : props.radius[1]
})

const color = computed(() => {
    return props.isMd ? '#409eff' : '#e6a23c'
})

function handleDrag(event: MouseEvent) {
    if (isDragging.value) {
        let x = Math.min((props.bound[0] - radius.value), (event.clientX - 50));
        x = Math.max(radius.value, x)
        pos.x = x
        let y = Math.min((props.bound[1] - radius.value), (event.clientY - 100));
        y = Math.max(radius.value, y)
        pos.y = y
        emits("update:pos", pos)
    }
}

function handleTouchDrag(event: TouchEvent) {
    const touch = event.touches[0]
    if (isDragging.value) {
        let x = Math.min((props.bound[0] - radius.value), (touch.clientX - 50));
        x = Math.max(radius.value, x)
        pos.x = x
        let y = Math.min((props.bound[1] - radius.value), (touch.clientY - 100));
        y = Math.max(radius.value, y)
        pos.y = y
        emits("update:pos", pos)
    }
}

function handleClick() {
    if (props.isMd) {
        emits('click')
    }
}

function handleTouchClick(event: TouchEvent) {
    isDragging.value = true;
    if (event.touches.length === 2 && props.isMd) {
        emits('click')
    }
}

watchEffect(() => {
    pos.x = props.pos.x
    pos.y = props.pos.y
})
</script>

<template>
    <g @dblclick="handleClick" @click="isShowText = !isShowText" class="node" @mousedown="isDragging = true"
        @mousemove="handleDrag" @mouseup="isDragging = false" @mouseover="isDragging = false" @touchstart="handleTouchClick"
        @touchmove="handleTouchDrag" @touchend="isDragging = false" @touchcancel="isDragging = false">
        <circle :cx="pos.x" :cy="pos.y" :r="radius" :fill="color" />
        <Transition name="fade">
            <text v-show="isShowText" :x="pos.x" :y="pos.y" alignment-baseline="middle" text-anchor="middle" fill="#fff"
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