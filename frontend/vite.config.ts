import { defineConfig } from 'vite';
import viteTsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  resolve: { alias: { '@': '/src' } },
  plugins: [viteTsconfigPaths()],
  server: {
    //origin: 'http://127.0.0.1:3000',
    host: true,
    port: 3000,
  }
})