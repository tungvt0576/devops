# Stage 1: Build Vue.js app
FROM node:18.16.0 as builder
RUN apt-get update && apt-get install -y apache2-utils
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

RUN npm i

# Install dependencies
RUN npm ci --quiet

# Copy the entire project
COPY . .

# Build the Vue.js app
RUN npm run build
# Generate .htpasswd file
RUN htpasswd -bc /app/.htpasswd admin admin

# Stage 2: Serve the built app using Nginx
FROM nginx:1.21-alpine
ENV NGINX_PROFILE="dev"
# Copy the built app from the previous stage
COPY --from=builder /app/dist /var/www/html
COPY --from=builder /app/.htpasswd /etc/nginx/.htpasswd
# Copy Nginx configuration file
COPY nginx.conf.template.dev /etc/nginx/nginx.conf.template.dev
COPY nginx.conf.template.stg /etc/nginx/nginx.conf.template.stg
COPY nginx.conf.template.prd /etc/nginx/nginx.conf.template.prd
# Expose the container's port
EXPOSE 8078

# Start Nginx server
# CMD ["nginx", "-g", "daemon off;"]
ENV BE_HOST=192.168.0.125
ENV BE_PORT=8081
ENV FE_PORT=8078
# CMD envsubst "\$BE_HOST\$BE_PORT\$FE_PORT" < ./etc/nginx/nginx.conf.template.${NGINX_PROFILE} > /etc/nginx/nginx.conf && nginx -g 'daemon off;'
#CMD ["sh", "-c", "cp /etc/nginx/nginx.conf.template.$NGINX_PROFILE /etc/nginx/nginx.conf.template", "&& envsubst "\$BE_HOST\$BE_PORT\$FE_PORT" < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'"]
CMD sh -c 'cp /etc/nginx/nginx.conf.template.$NGINX_PROFILE /etc/nginx/nginx.conf.template && envsubst "\$BE_HOST \$BE_PORT \$FE_PORT" < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g "daemon off;"'

