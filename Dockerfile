FROM node:18-alpine
WORKDIR /app

# install deps
COPY package.json package-lock.json* ./
RUN npm ci --only=production || npm install --production

# copy sources
COPY . .

EXPOSE 8080
CMD ["node", "index.js"]
