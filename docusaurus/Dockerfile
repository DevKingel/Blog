FROM node:24-alpine AS base

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

# Development stage
FROM base AS dev

# Copy source code
COPY . .

# Expose port and start development server
EXPOSE 3000

CMD ["pnpm", "run", "start"]

# Production stage
FROM base AS prod

# Copy source code and build artifacts
COPY . .
RUN pnpm run build

# Production image, copy only the standalone output
FROM base AS release
WORKDIR /app

EXPOSE 3000
CMD ["node", "server.js"]
