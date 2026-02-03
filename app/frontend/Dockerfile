# --- Build stage ---
FROM node:20-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# --- Runtime stage (unprivileged nginx) ---
FROM nginxinc/nginx-unprivileged:1.27-alpine

# Copy our nginx config (overwrites default.conf)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built static site
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080
