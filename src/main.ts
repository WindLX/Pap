import { createApp } from 'vue'
import './style.css'
import 'element-plus/dist/index.css'
import App from './App.vue'
import { createPinia } from 'pinia'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
    faSearch, faFolder, faFolderOpen, faGear,
    faFile, faRoute, faBars, faGears,
    faMap, faPlus, faTrashCan, faNoteSticky,
    faFilePen, faBoxOpen, faDolly, faMagnifyingGlassPlus,
    faMagnifyingGlassMinus, faCropSimple
} from '@fortawesome/free-solid-svg-icons'

library.add(faSearch, faFolder, faFolderOpen, faGear,
    faFile, faRoute, faBars, faGears,
    faMap, faPlus, faTrashCan, faNoteSticky,
    faFilePen, faBoxOpen, faDolly, faMagnifyingGlassMinus,
    faMagnifyingGlassPlus, faCropSimple)

const pinia = createPinia()

const app = createApp(App)
app.use(pinia)
app.mount("#app")