# Utilisez une image nginx comme image de base
FROM nginx:latest

RUN rm -rf /etc/nginx/conf.d/default.conf

# Copiez le fichier de configuration nginx
COPY ./nginx/backend.conf /etc/nginx/conf.d/backend.conf

# RUN groupmod -g $APP_GROUP_UID $APP_GROUP \
#     && usermod -u $APP_USER_UID -g $APP_USER_UID $APP_USER

# RUN chown -R $APP_USER:$APP_GROUP /var/www

# USER $APP_USER:$APP_USER_UID