# Stage 1: Build the React application
FROM node:22-alpine AS builder

WORKDIR /app

# Copy package files first for better Docker layer caching
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application source code
COPY . .

# Build the production application
RUN npm run build


# Stage 2: Serve the application with Nginx
FROM nginx:alpine

# Copy Vite's production build into Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Nginx listens on port 80
EXPOSE 80

# Keep Nginx running in the foreground
CMD ["nginx", "-g", "daemon off;"]
