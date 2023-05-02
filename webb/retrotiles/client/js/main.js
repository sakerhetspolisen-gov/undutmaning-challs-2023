import {loadSprites} from './loader.js';
import { Game} from './game.js';

window.addEventListener('load', async function(){
  const canvas = document.getElementById('gamecanvas');
  const ctx = canvas.getContext('2d');
  canvas.width = 500;
  canvas.height = 500;
  // show loading screen
  const txt = "Loading...";
  ctx.font = "48px Arial";
  const txtWidth = ctx.measureText(txt).width
  ctx.fillText(txt, (canvas.width/2) - (txtWidth / 2), 250);
  ctx.font = "10px Arial";
  // load sounds
  const sndNew = new Audio('/snd/new.ogg')
  const sndEnd = new Audio('/snd/end.ogg')
  // load graphics files
  const mapSprite = await loadSprites('./assets/fantasy-tileset.png');
  let playerSprites = []
  let loader = []
  for(let i = 1; i <= 23; i++) {
    loader.push(loadSprites('./assets/characters/' + i + '.png'));
  }
  await Promise.all(loader).then((values) => {playerSprites = values});

  const game = new Game(canvas.width, canvas.height, mapSprite, playerSprites);
  window.game = game

  game.socket.on("new", data => {
    if(data != game.socket.id){
      game.others[data] = {}
      sndNew.play();
    }

  });
  game.socket.on("tag", data => {
    game.taggedPlayer = data;
  });
  game.socket.on("quitter", data => {
    console.log(data)
    delete game.others[data];
    if(data == game.taggedPlayer)
      game.taggedPlayer = null
    sndEnd.play();
  });
  game.socket.on("move", msg => {
    if(msg.id != game.socket.id)
    game.others[msg.id] = msg.data
  });
  game.socket.on("players", msg => {
    game.others = msg
  });
  game.socket.on("msg", msg => {
    if (msg.startsWith('undut{')) {
      console.log(msg)
      game.endScreenMsg = "Check the console!"
    }
    else game.endScreenMsg = msg
  });
  game.socket.on("die", () => {
    game.socket.disconnect();
  });
  game.socket.on("disconnect", () => {
    //game.socket = null;
  });
  game.socket.emit("new", game.player.info())

  let lastTime = 0;

  function animate(timeStamp) {
    const deltaTime = timeStamp - lastTime;
    game.update(deltaTime);
    lastTime = timeStamp;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    game.draw(ctx, timeStamp);
    requestAnimationFrame(animate);
  }
  animate(0);
});
