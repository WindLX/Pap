<script setup lang="ts">
import { ElLoading, ElEmpty, ElInput, ElButton } from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { ResourceSchema } from '@/schemas/resource';
import ResourceAdd from '../Resource/ResourceAdd.vue';
import ResourceCard from '../Resource/ResourceCard.vue';
import { ResourceApi } from '@/api/resource';
import { onMounted, ref } from 'vue';
import { useFilterName } from '@/utils';

let resources = ref<Array<ResourceSchema>>([]);
const { filterText, filterName } = useFilterName();

function handleDeleteResource(index: number) {
    resources.value = resources.value.filter((_, i) => i !== index);
}

function handleAddNewResource(newResource: ResourceSchema) {
    resources.value.push(newResource);
}

onMounted(async () => {
    const loadingInstance = ElLoading.service({ target: "#cards-loader", fullscreen: true })
    resources.value = await ResourceApi.getResources()
    loadingInstance.close()
})
</script>

<template>
    <div class="resource">
        <h1 class="title">托管资源</h1>
        <ResourceAdd @upload="handleAddNewResource" :is-card="false" />
        <el-input class="filter-input" v-model="filterText">
            <template #append>
                <el-button @click="filterText = ''">
                    <font-awesome-icon :icon="['fas', 'xmark']" class="icon" />
                </el-button>
            </template>
        </el-input>
        <div class="cards" id="cards-loader" v-if="resources.length !== 0">
            <ResourceCard v-for="(resource, index) in resources" :key="index" :name="resource.name" :url="resource.url"
                @delete="handleDeleteResource(index)" v-show="filterName(resource.name)">
            </ResourceCard>
            <ResourceAdd @upload="handleAddNewResource" :is-card="true" />
        </div>
        <ElEmpty v-else class="empty" description="暂无托管资源" />
    </div>
</template>

<style scoped>
.resource {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: calc(100vw - 50px);
    height: 100%;
    user-select: none;
    overflow-y: auto;
}

.resource .title {
    margin-bottom: 10px;
}

.resource .filter-input {
    width: 60%;
    margin: 10px;
}

.resource .cards {
    display: grid;
    grid-template-columns: repeat(5, calc((100vw - 50px)/8));
    grid-gap: 5vw;
}

.resource .empty {
    margin: auto;
}
</style>