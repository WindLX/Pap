<script setup lang="ts">
import { ElLoading, ElButton } from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { ref } from 'vue';
import { ResourceApi } from '@/api/resource';
import { ResourceSchema } from '@/schemas/resource';

const props = defineProps<{
    isCard: boolean
}>()

const emits = defineEmits<{
    (e: 'upload', newResource: ResourceSchema): void
}>()

const fileInputRef = ref<HTMLInputElement | null>(null);
const uploadRef = ref<HTMLDivElement | null>(null);

async function handleDragUploadAsync(event: DragEvent) {
    if (props.isCard) {
        event.preventDefault();
        if (event.dataTransfer && fileInputRef.value) {
            const file = event.dataTransfer.files[0]
            const loadingInstance = ElLoading.service({ target: "#cards-loader", fullscreen: true })
            const formData = await createFormDataAsync(file)
            loadingInstance.close()
            const newResource = await ResourceApi.uploadResource(formData)
            emits('upload', newResource)
        }
        uploadRef.value?.classList.remove('active');
    }
}

async function handleDragOverAsync(event: DragEvent) {
    if (props.isCard) {
        event.preventDefault();
        uploadRef.value?.classList.add('active');
    }
}

async function createFormDataAsync(file: File): Promise<FormData> {
    return new Promise((resolve) => {
        const formData = new FormData();
        formData.append("file", file);
        resolve(formData);
    });
}

async function uploadFileAsync() {
    const loadingInstance = ElLoading.service({ target: "#cards-loader", fullscreen: true })
    const file = fileInputRef.value!.files![0];
    const formData = await createFormDataAsync(file)
    const newResource = await ResourceApi.uploadResource(formData)
    loadingInstance.close()
    emits('upload', newResource)
}
</script>

<template>
    <div :class="props.isCard ? 'resource-add-card' : 'resource-add'" ref="uploadRef" @dragover="handleDragOverAsync"
        @drop="handleDragUploadAsync">
        <input type="file" ref="fileInputRef" style="display: none;" @change="uploadFileAsync" />
        <el-button class="button" @click="fileInputRef!.click()">
            <font-awesome-icon :icon="['fas', 'plus']" class="icon" />
        </el-button>
    </div>
</template>

<style scoped>
.resource-add {
    margin: 10px;
    display: flex;
    width: 20%;
}

.resource-add-card {
    width: 14vw;
    height: 20vw;
    border-radius: 8px;
    margin: 10px;
    transition: 0.2s ease-in-out;
    border: 1px solid #ccc;
    display: flex;
    align-items: center;
    justify-content: center;
}

@media screen and (max-width: 540px) {
    .resource-add-card {
        width: 40vw;
        height: 57vw;
    }
}

@media screen and (max-width: 900px) and (min-width:540px) {
    .resource-add-card {
        width: 25vw;
        height: 35.7vw;
    }
}

.resource-add-card:hover {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    transform: scale(1.05);
}

.resource-add-card.active {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    transform: scale(1.05);
}

.resource-add-card.active .button {
    color: var(--el-button-hover-text-color);
    background-color: var(--el-button-hover-bg-color);
    outline: 0;
}

.resource-add-card .button {
    border: none;
    height: 80%;
    font-size: 24px;
    text-overflow: ellipsis;
    overflow: hidden;
    max-width: 11vw;
}

.button {
    width: 100%;
}
</style>