import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";
import { nodePolyfills } from "vite-plugin-node-polyfills";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  console.log("env", env);
  return {
    plugins: [
      react(),
      nodePolyfills({
        globals: {
          Buffer: true,
        },
      }),
    ],
    base: env.BASE_PATH || "",
  };
});
