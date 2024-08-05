# Utilisez une image Node.js comme image de base
FROM node:22

RUN mkdir -p /app/node_modules && chown -R node:node /app

# Définissez le répertoire de travail
WORKDIR /app

# Copiez les fichiers package.json et package-lock.json
COPY --chown=node:node package*.json ./

USER node

# Installez les dépendances
RUN npm install

# Copiez le reste des fichiers de l'application
COPY --chown=node:node . .

# Construisez l'application
RUN npm run build

# Exposez le port de l'application
EXPOSE 8000

# Démarrez l'application
CMD ["npm", "run", "start"]