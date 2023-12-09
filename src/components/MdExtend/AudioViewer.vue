<script setup lang="ts">
import { ref, watch, onMounted, onActivated } from 'vue'
import { ElLoading } from 'element-plus';
import { ResourceApi } from '@/api/resource';

const props = defineProps<{
    name: string,
    url: string,
    config: string | null
}>()

interface Config {
}

let url = ref<string | null>(null)
let config = ref<Config | null>(null)

async function loadUrlAsync(newUrl: string) {
    const loadingInstance = ElLoading.service({ target: "#audio-loader", fullscreen: false })
    if (newUrl.startsWith('./')) {
        url.value = await ResourceApi.getStreamUrl(newUrl)
    } else {
        url.value = newUrl
    }
    loadingInstance.close()
}

function loadConfig(newConfig: string | null) {
    if (newConfig) {
        const configJson = JSON.parse(newConfig) as Config
        config.value = configJson
    }
}

watch(props, async () => {
    await loadUrlAsync(props.url)
    loadConfig(props.config)
})

onMounted(async () => {
    await loadUrlAsync(props.url)
    loadConfig(props.config)
})

onActivated(async () => {
    await loadUrlAsync(props.url)
    loadConfig(props.config)
})
</script>

<template>
    <div class="audio-viewer" id="audio-loader">
        <audio controls :src="url" />
    </div>
</template>

<style scoped></style>