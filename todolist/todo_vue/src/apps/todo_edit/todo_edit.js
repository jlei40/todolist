import 'vite/modulepreload-polyfill';
import { createApp } from 'vue';
import AppEdit from './TodoEdit.vue'

createApp(AppEdit).mount("#appedit")