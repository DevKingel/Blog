# Utilisez une image PHP avec Composer comme image de base
FROM php:8.3-fpm

ARG APP_USER
ARG APP_USER_UID
ARG APP_GROUP
ARG APP_GROUP_UID

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip \
    libpq-dev

# Installez les extensions PHP nécessaires
RUN docker-php-ext-configure pgsql -with-pgsql=/usr/local/pgsql \
    && docker-php-ext-install pdo pdo_pgsql pgsql \
    && docker-php-ext-enable opcache \
    && pecl install xdebug \
    && apt-get autoclean -y \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm -rf /tmp/pear/

# Installez Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Définissez le répertoire de travail
WORKDIR /var/www

# Copiez les fichiers de l'application
COPY . .

RUN groupmod -g $APP_GROUP_UID $APP_GROUP \
    && usermod -u $APP_USER_UID -g $APP_USER_UID $APP_USER

RUN chown -R $APP_USER:$APP_GROUP /var/www

USER $APP_USER:$APP_USER_UID

# Installez les dépendances Laravel
RUN composer install

# Exposez le port de l'application
EXPOSE 9000

# Démarrez le serveur PHP-FPM
CMD ["php-fpm"]