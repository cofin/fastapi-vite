import { defineConfig } from 'vite'
import reactRefresh from '@vitejs/plugin-react-refresh'

// const ASSETS_URL = "/static/dist/";

// https://vitejs.dev/config/
export default defineConfig({
  // base: ASSETS_URL,
  clearScreen: false,
  plugins: [
    reactRefresh(),

  ],
  build: {
    target: "esnext",
    outDir: "../../static/dist",
    emptyOutDir: true,
    assetsDir: "_assets",
    manifest: true,

		rollupOptions: {
      input: (
        
        "./assets/javascript/main.tsx"),

			// output: {
      //   assetFileNames: "[name].[ext]",
      //   chunkFileNames: "[name].js",
      //   entryFileNames: "[name].js"
      // },
		},

  },

  root: "./assets/javascript", // You can change the root path as you wish
  server: {
    port: 3000,
    cors: true,
    strictPort: true,
    proxy: {
      // with options
      "/api/": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
})
