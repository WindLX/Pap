import { createApp } from 'vue'
import './style.css'
import 'element-plus/dist/index.css'
import App from './App.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faSearch, faFolder, faFolderOpen, faGear, faFile, faCodeBranch, faBars } from '@fortawesome/free-solid-svg-icons'
import { createPinia } from 'pinia'

library.add(faSearch, faFolder, faFolderOpen, faGear, faFile, faCodeBranch, faBars)

const pinia = createPinia()

const app = createApp(App)
app.use(pinia)
app.mount("#app")