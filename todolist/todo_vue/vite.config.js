import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
const backendPath = '../django_project';
// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    base: '/static/vite/',
    server: {
        watch: {
            ignored: [],
        },
    },
    build: {
        manifest: true,
        emptyOutDir: true,
        outDir: backendPath + '/core/static/vite/',
        rollupOptions: {
            input: {
                vue_todo_edit: "./src/apps/todo_edit/todo_edit.js",
                vue_todo_create: "./src/apps/todo_create/todo_create.js",
            },
        },
    },
});