# Используем базовый образ с установленным Node.js
FROM node:18

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /reactDashTemplate

# Копируем зависимости package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем исходный код
COPY . .

# Собираем приложение React
# RUN npm run build

EXPOSE 3000
# Указываем команду для запуска сервера раздачи статических файлов
CMD ["npm", "run", "dev"]


