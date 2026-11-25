import {defineConfig} from 'vite'
import {resolve} from 'node:path'

export default defineConfig({
    // Match Django's STATIC_URL.
    base: '/static/',

    build: {
        // Writes bundles into Django's static files.
        outDir: resolve(__dirname, '../static/bundler'),
        emptyOutDir: true,
        manifest: true,

        // Django supplies the HTML, so use JS/CSS as the entry point.
        rollupOptions: {
            input: {
                main: resolve(__dirname, 'src/main.js'),
            },
        },
    },
})