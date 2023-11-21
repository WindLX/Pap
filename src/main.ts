import { createApp } from 'vue'
import './style.css'
import 'katex/dist/katex.css'
import 'katex/dist/katex.min.css'
import 'element-plus/dist/index.css'
import App from './App.vue'
import * as VueRouter from 'vue-router'
import { createPinia } from 'pinia'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
    faSearch, faFolder, faFolderOpen, faGear,
    faFile, faRoute, faBars, faGears,
    faMap, faPlus, faTrashCan, faBook,
    faFilePen, faBoxOpen, faDolly, faMagnifyingGlassPlus,
    faMagnifyingGlassMinus, faCropSimple, faCheck, faXmark,
    faTag, faPen, faHand, faQuoteLeft, faInfinity,
    faCode, faSquare, faSquareCheck, faLink,
    faBookmark, faCircleChevronRight, faFloppyDisk,
    faFileExport, faFilePdf, faArrowUp, faFileCircleQuestion,
    faShieldHalved, faPaintBrush, faHouse, faLock, faLockOpen,
    faClockRotateLeft
} from '@fortawesome/free-solid-svg-icons'
import homeVue from './views/home.vue'
import loginVue from './views/login.vue'

library.add(faSearch, faFolder, faFolderOpen, faGear,
    faFile, faRoute, faBars, faGears,
    faMap, faPlus, faTrashCan, faBook,
    faFilePen, faBoxOpen, faDolly, faMagnifyingGlassMinus,
    faMagnifyingGlassPlus, faCropSimple, faCheck,
    faTag, faPen, faXmark, faHand, faQuoteLeft,
    faInfinity, faCode, faSquare, faSquareCheck,
    faLink, faBookmark, faCircleChevronRight,
    faFloppyDisk, faFileExport, faFilePdf, faArrowUp,
    faFileCircleQuestion, faShieldHalved, faPaintBrush,
    faHouse, faLock, faLockOpen, faClockRotateLeft
)

const pinia = createPinia()

const routes = [
    { path: '/', component: homeVue },
    { path: '/login', component: loginVue },
]

const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes,
})

const app = createApp(App)
app.use(pinia)
app.use(router)
app.mount("#app")