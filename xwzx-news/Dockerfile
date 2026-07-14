FROM node:20-alpine

WORKDIR /app

# 先复制依赖文件，利用缓存层
COPY package.json package-lock.json ./
RUN npm ci

# 再复制源码
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]