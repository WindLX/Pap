<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { computed, ref } from 'vue';

const props = defineProps<{
    color: string,
    closable: boolean
    disable: boolean
}>()

const emits = defineEmits<{
    (e: 'close'): void
    (e: 'click'): void
}>()

let hover = ref(false)
let actualColor = computed(() => {
    return props.disable ? desaturateColor(props.color) : props.color
})

function handleClick() {
    if (!props.disable) {
        emits('click')
    }
}

function desaturateColor(hexColor: string): string {
    hexColor = hexColor.replace('#', '');

    const bigint = parseInt(hexColor, 16);
    const r = (bigint >> 16) & 255;
    const g = (bigint >> 8) & 255;
    const b = bigint & 255;

    let hsl = rgbToHsl(r, g, b);
    hsl[1] = hsl[1] * 0.3;
    const rgb = hslToRgb(hsl[0], hsl[1], hsl[2]);
    const desaturatedHex = `#${(1 << 24 | rgb[0] << 16 | rgb[1] << 8 | rgb[2]).toString(16).slice(1)}`;

    return desaturatedHex;
}

function rgbToHsl(r: number, g: number, b: number): number[] {
    r /= 255;
    g /= 255;
    b /= 255;

    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    let h = 0;
    let s = 0;
    const l = (max + min) / 2;

    if (max !== min) {
        const d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch (max) {
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }

    return [h, s, l];
}

function hslToRgb(h: number, s: number, l: number): number[] {
    let r, g, b;

    if (s === 0) {
        r = g = b = l;
    } else {
        const hue2rgb = function hue2rgb(p: number, q: number, t: number): number {
            if (t < 0) t += 1;
            if (t > 1) t -= 1;
            if (t < 1 / 6) return p + (q - p) * 6 * t;
            if (t < 1 / 2) return q;
            if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
            return p;
        };

        const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        const p = 2 * l - q;
        r = hue2rgb(p, q, h + 1 / 3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1 / 3);
    }

    return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
}
</script>
<template>
    <span class="tag" @click="handleClick">
        <slot>
        </slot>
        <span v-if="props.closable" @mouseover="hover = true" @mouseleave="hover = false" @click="$emit('close')">
            <font-awesome-icon :icon="['fas', 'xmark']" class="icon" :class="{ 'icon-hover': hover }" />
        </span>
    </span>
</template>
<style scoped>
.tag {
    background-color: v-bind(actualColor);
    color: #fff;
    font-size: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 32px;
    height: 24px;
    width: fit-content;
    border-radius: 3px;
    margin: 0 2px;
    padding: 0 6px;
    transition: background-color .2s ease-in-out;
}

.icon {
    font-size: 12px;
    color: #fff;
    margin-left: 6px;
    padding: 0 1.5px;
}

.icon-hover {
    color: v-bind(color);
    background-color: #f1f1f1;
    border-radius: 3px;
}
</style>