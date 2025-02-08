import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Load environment variables
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
  },
  define: {
    "process.env": {}, // Ensure compatibility for older libraries
  },
});
