# Blog

Build docker images with "docker compose build"

Start the containers with "docker compose up -d"

copy the .env.exemple file in the backend folder in the same folder and name it .env

Modify the values for the database

Execute the next command to create the laravel application key : "docker compose exec backend php artisan key:generate"

Execute the next command to make the migration of the database : "docker compose exec backend php artisan migrate"