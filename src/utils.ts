import { ref } from 'vue';

export function useFilterName() {
    const filterText = ref('')

    function filterName(name: string): boolean {
        if (filterText.value !== '') {
            const target = name
            const source = filterText.value
            const regex = new RegExp(source, 'i');
            return regex.test(target)
        }
        else
            return true
    }

    return { filterText, filterName }
}

export async function downloadUrlAsync(name: string, url: string) {
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', name);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}