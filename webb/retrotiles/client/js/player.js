export class Player {
  constructor(game) {
    this.game = game;
    this.width = 16;
    this.height = 16;
    do {
      this.x = Math.random() * (this.game.width-this.width);
      this.y = Math.random() * (this.game.height - this.height);
    } while(!game.map.accessible(this.x, this.y, this.width, this.height))
    this.dir = 'down';
    this.health = 100;
    setInterval(function ()
      {
        if(this.game.taggedPlayer && 
          this.game.taggedPlayer != this.game.socket.id)
      this.health -= 1;
      
    if(this.health < 0)
      this.game.socket.disconnect()
    }.bind(this), 1000)
    this.tagged = false
    this.frame = 0;
    this.frameInterval = 100;
    this.frameTimer = 0;
    this.name = "player " + Math.floor(Math.random() * 1000);
    this.items = ""
    this.cthulhuEncounter = false
    this.speed = 1 + Math.random();
    this.charno = Math.floor(Math.random() * game.playerSprites.length)
  }
  info() {
    return({name: this.name, health: this.health, x: this.x, y: this.y, dir: this.dir, 
      frame: this.frame, charno: this.charno, tile: this.game.map.getTileCoord(this.x, this.y),
    cthulhuEncounter: this.cthulhuEncounter, items: this.items})
  }
  update(input, deltaTime){
    if(!game.socket)
      return;
    let dr = {x: 0, y: 0}
    if('ArrowRight' in input) {
      dr.x += this.speed;
    }
    else if ('ArrowLeft' in input) {
      dr.x -= this.speed;
    }
    if('ArrowUp' in input) {
      dr.y -= this.speed;
    }
    else if ('ArrowDown' in input) {
      dr.y += this.speed;
    }
    if('touch' in input){
      let t = input['touch']
      const o = this.viewPortOrigin()
      const rt = {x: t.x + o.x, y: t.y + o.y}
      dr = {x: rt.x - this.x, y: rt.y - this.y}
      const l = Math.sqrt(dr.x*dr.x + dr.y*dr.y)
      dr.x = dr.x/l*this.speed
      dr.y = dr.y/l*this.speed
    }
      if(this.game.map.accessible(this.x + dr.x, this.y + dr.y, 
        this.width, this.height)){
      this.x += dr.x
      this.y += dr.y
      // set direction
      if(Math.abs(dr.x) > Math.abs(dr.y)) {
        dr.x < 0 ? this.dir = 'left' : this.dir = 'right';
      }
        else {
        dr.y < 0 ? this.dir = 'up' : this.dir = 'down';
      }
    }
    if(this.x < 0) this.x = 0;
    if(this.x > this.game.map.width() - this.width) 
      this.x = this.game.map.width() - this.width;
    if(this.y < 0) this.y = 0;
    if(this.y > this.game.map.height() - this.height) 
      this.y = this.game.map.height() - this.height;
    if(Object.keys(input).length > 0 && this.frameTimer > this.frameInterval){
      this.frameTimer = 0;
      this.frame++;
      this.game.socket.emit("move", this.info())
    }
    else
      this.frameTimer += deltaTime;
  }
  viewPortOrigin(){
    let vw = this.game.width
    let vh = this.game.height
    let mw = this.game.map.width()
    let mh = this.game.map.height()
    let c = {
      x: this.x - vw*0.5,
      y: this.y - vh*0.5
    }
    if(c.x < 0)
      c.x = 0
    if(c.x + vw >= mw)
      c.x = mw-vw 
    if(c.y < 0)
      c.y = 0
    if(c.y + vh >= mh)
      c.y = mh-vh 
    return(c)
  }
  drawMap(context, tiles, o){
    const vw = this.game.width
    const vh = this.game.height
    const map = this.game.map
    let start = map.getTileCoord(o.x, o.y)
    let end = { ...start};
    end.x += Math.round(vw / map.tsize);
    end.y += Math.round(vh / map.tsize);
    if(end.x >= map.cols) end.x = map.cols - 1;
    if(end.y >= map.rows) end.y = map.rows - 1;
    const offsetX = -o.x + start.x * map.tsize;
    const offsetY = -o.y + start.y * map.tsize;
    for (var c = start.x; c <= end.x; c++) {
      for (var r = start.y; r <= end.y; r++) {
        var tile = map.getTile(c, r, tiles);
        var x = (c - start.x) * map.tsize + offsetX;
        var y = (r - start.y) * map.tsize + offsetY;
        if (tile !== 0) { // 0 => empty tile
          context.drawImage(
            this.game.mapSprite, // image
            map.tileOrigin[tile].x, // source x
            map.tileOrigin[tile].y, // source y
            map.tsize, // source width
            map.tsize, // source height
            Math.round(x),  // target x
            Math.round(y), // target y
            map.tsize, // target width
            map.tsize // target height
          );
        }
      }
    }
  }
  drawPlayer(p, context, o){

    // select player sprite from direction
    let imdx;
    if(p.dir == 'down')
      imdx = 0;
    else if(p.dir == 'up')
      imdx = 1;
    else if(p.dir == 'left')
      imdx = 2;
    else if(p.dir == 'right')
      imdx = 3;
    let x,y;
    x = p.x - o.x
    y = p.y - o.y
    const sprite = this.game.playerSprites[p.charno % this.game.playerSprites.length] 
    if(!sprite) {
      return(false);
    }
    context.drawImage(sprite, this.width * imdx, this.height * (p.frame % 4), 
      this.width, this.height, 
      x, y, 
      this.width, this.height);
    context.font = "10px Arial";
    context.fillStyle = "black";
    context.fillText(p.name, x, y - (0.5 * this.height));
  }
  drawHealth(context) {
    context.font = "12px Arial";
    context.fillStyle = "black";
    context.fillText(`\u2764\ufe0f ${this.health}`, this.game.width*0.95, 12);
    if(this.items.match(/Sword/)){
      const sword = this.game.map.floaters[1]
    context.drawImage(this.game.mapSprite, sword.sx, sword.sy, 
      sword.width, sword.height, 
      this.game.width*0.85, 2, 
      16, 16);
    }
  }
  draw(context){
    const o = this.viewPortOrigin()
    this.drawMap(context, this.game.map.tiles, o)
    this.drawMap(context, this.game.map.obstacles, o)
    this.drawHealth(context)
    for(let i in this.game.others) {
      const p = this.game.others[i]
      if(p.x >= o.x && p.x < o.x + this.game.width
        && p.y >= o.y && p.y < o.y + this.game.height){
        this.drawPlayer(p, context, o)
      }
    }
    this.drawPlayer(this, context, o)
    return o;
  }
}
