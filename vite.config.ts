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
    target: "es2016",
    outDir: "../static",
    emptyOutDir: true,
    assetsDir: "",
    manifest: true,

		rollupOptions: {
      input:  "./assets/javascript/main.tsx"
		},

  },

  root: "assets/", // You can change the root path as you wish

})
