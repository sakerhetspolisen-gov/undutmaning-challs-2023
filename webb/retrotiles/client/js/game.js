import { map } from './map.mjs'
import { Player } from './player.js';
import { InputHandler } from './input.js';
import { io } from "https://cdn.socket.io/4.3.2/socket.io.esm.min.js";

export  class Game {
  constructor(width, height, mapSprite, playerSprites) {
    this.socket = io();
    this.width = width;
    this.height = height;
    this.mapSprite = mapSprite;
    this.playerSprites = playerSprites;
    this.map = map;
    this.frame = 0;
    this.frameInterval = 100;
    this.frameTimer = 0;
    this.player = new Player(this);
    this.input = new InputHandler();
    this.others = {};
    this.taggedPlayer = null;
    this.socket.emit("move", this.player.info())
    this.endScreenMsg = "Reload to restart.";
    this.floaters = [];
    for (let [i, f] of map.floaters.entries()) 
      this.floaters.push({x: f.x, y: f.y, vx: (Math.random()-0.5)*f.jitter, vy: (Math.random()-0.5)*f.jitter})
  }
  update(deltaTime){
    this.player.update(this.input.keys, deltaTime);
    this.updateFloaters();
    if(this.frameTimer > this.frameInterval){
      this.frameTimer = 0;
      this.frame++;
    }
    else
      this.frameTimer += deltaTime;
  }
  updateFloaters(){
    for (let [i, f] of this.floaters.entries()) {
      const fdata = this.map.floaters[i];
      f.x += f.vx*0.1;
      f.y += f.vy*0.1;
      while(f.x < 0) f.x += this.map.width();
      while(f.y < 0) f.y += this.map.height();
      while(f.x > this.map.width()) f.x -= this.map.width();
      while(f.y > this.map.height()) f.y -= this.map.height();
      if(fdata.deadly && 
        ((this.player.x - f.x)**2 + (this.player.y - f.y)**2)**0.5 < this.player.width) {
        this.endScreenMsg = "Killed by Death.";
        this.socket.disconnect();
      }
      if(fdata.name == "Sword" && ((this.player.x - f.x)**2 + (this.player.y - f.y)**2)**0.5 < this.player.width)
        this.player.items="Sword,{\"magical\": false}"
      if(fdata.name == "Cthulhu"){
        if (((this.player.x - f.x)**2 + (this.player.y - f.y)**2)**0.5 < fdata.width)
          this.player.cthulhuEncounter = true
        else 
          this.player.cthulhuEncounter = false
      }

      if(fdata.anchored){
        const dist = ((f.x - fdata.x)**2 + (f.y - fdata.y)**2)**0.5
        if(Math.random() > 0.3 && dist > this.map.floaters[i].jitter){
          f.vx += (Math.random()*fdata.jitter - (f.x - fdata.x))/(dist);
          f.vy += (Math.random()*fdata.jitter - (f.y - fdata.y))/(dist);
        }
      }
      else {
        if(Math.random() > 0.9){
          f.vx += (Math.random()-0.5)*fdata.jitter
          f.vy += (Math.random()-0.5)*fdata.jitter
        }
        if(Math.random() > 0.99){
          f.vx = (Math.random()-0.5)*fdata.jitter
          f.vy = (Math.random()-0.5)*fdata.jitter
        }
      }
      if((f.vx**2+f.vy**2) > fdata.jitter**2) {
        f.vx *= 0.9;
        f.vy *= 0.9;
      }
    }
  }
  drawTag(ctx, x, y){
    const sz = this.player.width
    ctx.beginPath();
    ctx.arc(x + sz*0.5, y + sz*0.5, sz + 3,
      (this.frame % 10 - 1)*0.1*2*Math.PI, (this.frame % 10 + 1)*0.1*2*Math.PI);
    ctx.stroke();
  }
  drawFloaters(ctx, origin){
    for (let [i, f] of this.floaters.entries()) {
      if(f.x >= origin.x && f.x < origin.x + this.width
        && f.y >= origin.y && f.y < origin.y + this.height){
        const item = this.map.floaters[i];
        ctx.drawImage(
          this.mapSprite, item.sx, item.sy, 
          item.width, item.height, 
          f.x - origin.x, f.y - origin.y, 
          item.scale*item.width, item.scale*item.height);
      }
    }
  }
  drawEndScreen(ctx, gfx, msg){
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, this.width, this.height)
    const x = this.width*0.5-2*gfx.width
    ctx.drawImage(
      this.mapSprite, gfx.x, gfx.y, 
      gfx.width, gfx.height, 
      x, 0.2*this.height, 
      4*gfx.width, 4*gfx.height);
    ctx.textAlign = 'center';
    ctx.fillStyle = "white";
    ctx.font = "30px Arial";
    ctx.fillText(msg, 0.5*this.width, 0.8*this.height);
  }
  draw(context){
    if(this.socket.disconnected)
      this.drawEndScreen(context, this.map.skull, this.endScreenMsg)
    else {
      const o = this.player.draw(context);
      const p = this.player
      if(this.taggedPlayer == this.socket.id)
        this.drawTag(context, p.x - o.x, p.y - o.y)
      else 
        for(let i in this.others){
          const p2 = this.others[i]
          if(this.taggedPlayer == i && p2.x >= o.x && p2.x < o.x + this.width
            && p2.y >= o.y && p2.y < o.y + this.height)
            this.drawTag(context, p2.x - o.x, p2.y - o.y)
        }
      this.drawFloaters(context, o);
    }
  }
}


