FROM node:24-alpine

RUN corepack enable

WORKDIR /app

COPY package.json pnpm-lock.yaml ./

COPY . ./

CMD [ "pnpm", "run", "dev" ]