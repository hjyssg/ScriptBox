const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(express.static(__dirname + '/public'));

io.on('connection', (socket) => {
  console.log('A user connected');

  // 监听来自客户端的消息
  socket.on('chat message', (msg) => {
    console.log('message: ' + msg);
    // 将消息广播给所有客户端
    io.emit('chat message', msg);
  });

  // 监听客户端断开连接事件
  socket.on('disconnect', () => {
    console.log('A user disconnected');
  });
});

server.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});
