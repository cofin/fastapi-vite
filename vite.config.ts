import { defineConfig } from 'vite'
import reactRefresh from '@vitejs/plugin-react-refresh'
const Dotenv = require("dotenv");
import path from "path";
Dotenv.config({ path: path.join(__dirname, ".env") });

const STATIC_URL = process.env.STATIC_URL;
// https://vitejs.dev/config/
export default defineConfig({
  base: `${STATIC_URL}`,
  clearScreen: false,
  plugins: [
    reactRefresh(),

  ],
  build: {
    target: "esnext",
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
