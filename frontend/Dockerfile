# Utilisez une image Node.js comme image de base
FROM node:18

# Définissez le répertoire de travail
WORKDIR /app

# Copiez les fichiers package.json et package-lock.json
COPY package*.json ./

# Installez les dépendances
RUN npm install

# Copiez le reste des fichiers de l'application
COPY . .

# Construisez l'application
RUN npm run build

# Exposez le port de l'application
EXPOSE 8000

# Démarrez l'application
CMD ["npm", "run", "serve"]