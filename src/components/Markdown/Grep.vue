<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElInput } from 'element-plus'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

const emits = defineEmits<{
    (e: 'grep', value: string): void
    (e: 'focusLast'): void
    (e: 'focusNext'): void
    (e: 'clear'): void
}>()

let regex = ref('')
const errRegex = computed(() => {
    try {
        new RegExp(regex.value)
        return false
    } catch (e) {
        return true
    }
})

function handleLast() {
    emits('focusLast')
}

function handleNext() {
    emits('focusNext')
}
</script>

<template>
    <div class="grep">
        <el-input v-model="regex" @input="emits('grep', regex)" placeholder="查找" clearable @clear="emits('clear')"
            :class="{ 'err-regex': errRegex }" />
        <font-awesome-icon :icon="['fas', 'arrow-up']" class="icon" @mousedown="handleLast()" />
        <font-awesome-icon :icon="['fas', 'arrow-down']" class="icon" @mousedown="handleNext()" />
    </div>
</template>

<style scoped>
.grep {
    position: absolute;
    right: 0;
    z-index: 99;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    padding: 5px 8px;
    display: flex;
    align-items: center;
}

.grep .icon {
    margin-left: 8px;
    font-size: 16px;
    color: #aaaaaa;
    cursor: pointer;
}

.grep .icon:hover {
    color: var(--el-color-primary);
}
</style>
<style>
.err-regex .el-input__wrapper input {
    color: #f56c6c;
    font-weight: bold;
}
</style>