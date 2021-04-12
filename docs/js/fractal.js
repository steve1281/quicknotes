var currentWorker =0;
const canvas = document.getElementById("canvas");
const c = canvas.getContext("2d");
var fractalworkers = [devon(),mandel(), bluerose(), topdownpyr()];

canvas.width = innerWidth;
canvas.height = innerHeight;
canvas.style.border="1px black solid";

// resized window, reset canvas
addEventListener("resize", () => {
    canvas.width = innerWidth;
    canvas.height = innerHeight;
    init();
});
canvas.addEventListener("click", () =>{
    currentWorker++;
    if (currentWorker == fractalworkers.length) currentWorker=0;

})
function init() {
    //console.log(`${innerWidth} ${innerHeight}`);
}

function animate() {
    requestAnimationFrame(animate);
    c.clearRect(0,0,canvas.width, canvas.height);
    draw(fractalworkers[currentWorker]);
}


function draw(fractal) {
    var imageData = c.getImageData(0, 0, 1024, 1024);
    var data = imageData.data;
    var x = 0, y = 0;
    for (var i = 0, len = data.length; i < len;) {
      data[i++] = fractal.red(x, y);
      data[i++] = fractal.green(x, y);
      data[i++] = fractal.blue(x, y);
      data[i++] = 255;
      if (++x === 1024) x = 0, y++;
    }
    c.putImageData(imageData, 0, 0);
  }
init();
animate();
