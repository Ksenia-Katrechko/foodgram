# build env
FROM node:21.7.1-alpine
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build
CMD cp -r build result_build
