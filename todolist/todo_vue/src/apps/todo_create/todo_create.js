import 'vite/modulepreload-polyfill';
import { createApp } from 'vue';
import AppCreate from './TodoCreate.vue'

createApp(AppCreate).mount("#appcreate")