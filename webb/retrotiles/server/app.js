import * as mapmod from '../client/js/map.mjs';
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const env = require('dotenv').config()
const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);

const map = mapmod.map
const socketio = require("socket.io")(server, {
});

app.use( express.static('../client') );

let players = {};
let tagged = null;
let timeTagged = 0;

function tagRandom() {
  const keys = Object.keys(players)
  if(keys.length < 2) {
    tagged = null
  }
  else {
    if (!tagged){
      const i = keys.length * Math.random() << 0
      const id = Object.keys(players)[i]
      tagged = id;
      timeTagged = Date.now()
      console.log("Tagging ", id)
    }
  }
  socketio.emit("tag", tagged)
}

function invalidMoveMsg(m){
  const re = /(player|haxor) [0-9]{1,3}/;
  if(!m.hasOwnProperty("name") || !m.name.match(re))
    return(true)
  if(isNaN(parseInt(m.x)) || isNaN(parseInt(m.y)))
    return(true)
  if(isNaN(parseInt(m.frame)) || parseInt(m.frame) < 0)
    return(true)
  if(isNaN(parseInt(m.charno)) || parseInt(m.charno) < 0)
    return(true)
  if(isNaN(parseInt(m.health)) || parseInt(m.health) < 0 || parseInt(m.health) > 100)
    return(true)
  if(!m.hasOwnProperty("tile") || isNaN(parseInt(m.tile.x)) || isNaN(parseInt(m.tile.y)))
    return(true)
  if(!m.hasOwnProperty("dir") || !m.dir.match(/(up|down|left|right)/))
    return(true)
  if(m.hasOwnProperty("items")){
    let items=m.items.split(",")
    m.items = {}
    for(let i = 0; i<items.length-1;i+=2){
      try {
      m.items[items[i]] = JSON.parse(items[i+1])
      } catch(e) {
        console.log(e)
        return(true)
      }
    }
  }
  if(m.items && m.items.hasOwnProperty("MagicalSword"))
    return(true)

  return(false)
}

function releaseFlag(m) {
  if(m.tile.x == map.flagTile.x && m.tile.y == map.flagTile.y)
    return(process.env.FLAG_1);
  if(m.cthulhuEncounter && m.items) {
    if(m.items.MagicalSword)
      return(process.env.FLAG_2);
    if(m.items.Sword)
      return("A sword? DEATH by CTHULHU.");
  }
  return(null);
}


server.listen(3000, () => {
  console.log("Listening at :3000...");
});

socketio.on("connection", socket => {
  console.log("connect: ", socket.id)
  socket.emit("players", players)
  tagRandom()
  socket.emit("tag", tagged)
  socket.on("move", msg => {
    if(invalidMoveMsg(msg)) {
      socket.emit("msg", "Haxor detected.");
      socket.emit("die")
    }
    else {
      let flagStr = releaseFlag(msg)
      if(flagStr){
        socket.emit("msg", flagStr);
        socket.emit("die")
      }
      players[socket.id] = msg
      if(tagged && Date.now()-timeTagged > 1000 && tagged != socket.id && 
        Object.values(players).find(p => p.tile.x == msg.tile.x
          && p.tile.y == msg.tile.y && p == players[tagged])){
        tagged = socket.id
        timeTagged = Date.now()
        socketio.emit("tag", tagged)
      }
      else if(tagged == socket.id && Date.now()-timeTagged > 1000){
        const taggable = Object.keys(players).filter(q => q != tagged && 
          players[q].tile && players[q].tile.x == msg.tile.x
          && players[q].tile.y == msg.tile.y)
        if(taggable.length > 0){
          tagged = taggable[Math.floor(Math.random() * taggable.length)]
          timeTagged = Date.now()
          socketio.emit("tag", tagged)
        }
      }
      socketio.emit("move", {id: socket.id, data: {x: msg.x, y: msg.y, name: msg.name, 
        charno: msg.charno, dir: msg.dir, frame: msg.frame}})
    }
  });

  socket.on("disconnecting", (reason) => {
    delete players[socket.id];
    if(socket.id == tagged)
      tagged = null
    for (const room of socket.rooms) {
      if (room == socket.id) {
        socketio.emit("quitter", socket.id)
        tagRandom()
      }
    }

  });
});


