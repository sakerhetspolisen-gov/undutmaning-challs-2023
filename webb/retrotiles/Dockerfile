FROM node:latest

WORKDIR /home/ctf

COPY server ./server
COPY client ./client

WORKDIR /home/ctf/server

RUN npm install

EXPOSE 3000
CMD ["node", "app.js"]