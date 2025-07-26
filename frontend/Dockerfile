# Base image for development and production
FROM node:24-alpine AS base

WORKDIR /app

# Install dependencies
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

# Development stage
FROM base AS dev

# Copy source code
COPY . .

# Expose port and start development server
EXPOSE 3000

CMD ["pnpm", "run", "dev"]

# Production stage
FROM base AS prod

# Copy source code and build artifacts
COPY . .
RUN pnpm run build

# Production image, copy only the standalone output
FROM base AS release
WORKDIR /app
COPY --from=prod /app/.next/standalone ./
COPY --from=prod /app/.next/static ./.next/static
COPY --from=prod /app/public ./public

EXPOSE 3000
CMD ["node", "server.js"]
