<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ElNotification } from 'element-plus';
import { ResourceApi } from '@/api/resource';
import { downloadUrlAsync } from '@/utils';

const props = defineProps<{
    name: string,
    url: string,
}>()

const emits = defineEmits<{
    (e: 'delete'): void
}>()

let background = ref('');

async function handleExportAsync() {
    const url = await ResourceApi.getBlobUrl(props.url)
    await downloadUrlAsync(props.name, url)
}

function handleCopy() {
    const url = `res://${props.url}`
    navigator.clipboard.writeText(url)
        .then(function () {
            ElNotification({
                title: "复制成功",
                message: url,
                type: 'success',
                duration: 2000
            })
        })
        .catch(function (err) {
            ElNotification({
                title: "复制失败",
                message: err,
                type: 'error',
                duration: 2000
            })
        });
}

function handleDelete() {
    ResourceApi.deleteResource(props.url).then(() => {
        emits('delete')
    })
}

async function loadAsync() {
    if (props.url.endsWith('png') || props.url.endsWith('jpg') || props.url.endsWith('jpeg') || props.url.endsWith('gif')) {
        const url = await ResourceApi.getBlobUrl(props.url)
        background.value = `url("${url}")`
    }
}

watch(props, async () => {
    await loadAsync()
})

onMounted(async () => {
    await loadAsync()
})
</script>

<template>
    <div class="card">
        <div class="buttons">
            <font-awesome-icon :icon="['fas', 'file-export']" class="icon button" @click="handleExportAsync()" />
            <font-awesome-icon :icon="['fas', 'copy']" class="icon button" @click="handleCopy()" />
            <font-awesome-icon :icon="['fas', 'xmark']" class="icon button" @click="handleDelete()" />
        </div>
        <h1 class="title">{{ props.name }}</h1>
    </div>
</template>

<style scoped>
.card {
    width: 14vw;
    height: 20vw;
    border-radius: 8px;
    margin: 10px;
    transition: 0.2s ease-in-out;
    border: 1px solid #ccc;
    position: relative;
    background-image: v-bind(background);
    background-size: cover;
    user-select: all;
}

@media screen and (max-width: 540px) {
    .card {
        width: 40vw;
        height: 57vw;
    }
}

@media screen and (max-width: 900px) and (min-width:540px) {
    .card {
        width: 25vw;
        height: 35.7vw;
    }
}

.card:hover {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    transform: scale(1.05);
}

.card .title {
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    position: absolute;
    font-size: 24px;
    text-overflow: ellipsis;
    overflow: hidden;
    max-width: 11vw;
    background-color: #ffffff77;
    padding: 5px;
    border-radius: 5px;
}

.card .title:hover {
    max-width: 100vw;
}

.card .buttons {
    position: absolute;
    right: 2%;
    background-color: #ffffff77;
    margin: 5px;
    padding: 0 5px;
    border-radius: 3px;
    z-index: 1;
}

.card .icon {
    font-size: 20px;
    margin: 5px;
}

.card .button {
    color: #232323;
    cursor: pointer;
}

.card .button:hover {
    color: var(--el-color-primary);
}
</style>