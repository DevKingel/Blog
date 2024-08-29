mkdir frontend/node_modules

docker compose run --rm frontend npm i
docker compose up -d --build

docker compose exec -d frontend npm run build:watch