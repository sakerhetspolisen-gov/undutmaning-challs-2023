function getPosition(element) {
    let xe = 0;
    let ye = 0;
    const w = element.width;
    const h = element.height

    while(element) {
        xe += (element.offsetLeft - element.scrollLeft + element.clientLeft);
        ye += (element.offsetTop - element.scrollTop + element.clientTop);
        element = element.offsetParent;
    }
    return { x: xe - 0.5*w, y: ye - 0.5*h};
}

function relativePos(ev) {
  const canvasPosition = getPosition(ev.touches[0].target);
  let tap = { x:0, y:0 };
  if(ev.touches.length>0){
    let tt = ev.touches[0];
    tap.x = tt.clientX || tt.pageX || tt.screenX ||0;
    tap.y = tt.clientY || tt.pageY || tt.screenY ||0;
  }
  tap.x = tap.x - canvasPosition.x;
  tap.y = tap.y - canvasPosition.y;
  return(tap);
}
export class InputHandler {
  constructor() {
    this.keys = {};

    window.addEventListener('keydown', e => {
      if(( e.key === 'ArrowDown' ||
        e.key === 'ArrowUp' ||
        e.key === 'ArrowLeft' ||
        e.key === 'ArrowRight')
        && !(e.key in this.keys)) {
        this.keys[e.key] = true;
      }
    });

    window.addEventListener('keyup', e => {
      if( e.key === 'ArrowDown' ||
        e.key === 'ArrowUp' ||
        e.key === 'ArrowLeft' ||
        e.key === 'ArrowRight')
        delete this.keys[e.key]
    });
    const canvas = document.getElementById("gamecanvas");
    canvas.addEventListener('touchstart', e => {
      this.keys['touch'] = relativePos(e);
    });
    canvas.addEventListener('touchmove', e => {
      this.keys['touch'] = relativePos(e);
    });
    canvas.addEventListener('touchend', e => {
      delete this.keys['touch']
    });
    canvas.addEventListener('touchcancel', e => {
      delete this.keys['touch']
    });
  }
}


