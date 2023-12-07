<script setup lang="ts">
import { Vector } from '@/schemas/net';

const props = defineProps<{
    source: Vector,
    target: Vector,
}>()

</script>

<template>
    <line :x1="props.source.x" :y1="props.source.y" :x2="props.target.x" :y2="props.target.y" class="line" />
</template>

<style scoped>
.line {
    stroke: #f0f0f0;
    stroke-width: 2;
}
</style>@/schemas/net