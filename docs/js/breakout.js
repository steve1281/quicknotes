// hook into the canvas
var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

// game globals
var x = canvas.width/2;
var y = canvas.height-30;
var dx = 2;
var dy = -2;
var ballRadius = 10;
var paddleHeight = 10;
var paddleWidth = 75;
var paddleX = (canvas.width-paddleWidth)/2;
var rightPressed = false;
var leftPressed = false;
var brickRowCount = 3;
var brickColumnCount = 5;
var brickWidth = 75;
var brickHeight = 20;
var brickPadding=10;
var brickOffsetTop =30;
var brickOffsetLeft = 30;
var bricks = [];
for (c=0; c< brickColumnCount; c++) {
    bricks[c] = [];
    for (r=0; r < brickRowCount; r++) {
        bricks[c][r] = {x:0, y:0, status:1 };
    }
}

var score =0;
var lives=3;

// draw Lives
function drawLives()
{
    ctx.font = "16px Arial";
    ctx.fillStype = "#0095DD";
    ctx.fillText("Lives: " + lives, canvas.width-65, 20);
}

// draw Score
function drawScore()
{
    ctx.font = "16px Arial";
    ctx.fillStyle = "#0095DD";
    ctx.fillText("Score: "+score, 8, 20);
}

// collision detection - bricks
function collisionDetection()
{
    for (c=0; c< brickColumnCount; c++) {
        for(r=0; r< brickRowCount; r++) {
            var b = bricks[c][r];
            if (b.status == 1) {
                // calcs
                if (x > b.x && x < b.x+brickWidth && y > b.y && y < b.y+brickHeight) {
                    dy = -dy;
                    b.status =0;
                    score++;
                    if (score == brickRowCount * brickColumnCount) {
                        alert("you win");
                        document.location.reload();
                    }
                }
            }
        }
    }
}

// drawBricks
function drawBricks() {
    for (c=0; c < brickColumnCount; c++ ) {
        for (r=0; r< brickRowCount; r++ ) {
            if (bricks[c][r].status ==1 ) {
                var brickX = (c*(brickWidth + brickPadding)) + brickOffsetLeft;
                var brickY = (r*(brickHeight + brickPadding)) + brickOffsetTop;

                bricks[c][r].x = brickX;
                bricks[c][r].y = brickY;
                ctx.beginPath();
                ctx.rect(brickX,brickY, brickWidth, brickHeight);
                ctx.fillStyle = "#0095DD"
                ctx.fill();
                ctx.closePath();
            }
        }
    }
} 

// drawBall 
function drawBall() {
    // collision detection
    if (y + dy < ballRadius) {
        dy = -dy;
    } else if (y + dy > canvas.height-ballRadius) {
        if ( x > paddleX && x < paddleX + paddleWidth) {
            dy = -dy;
        } else {
            lives--;
            if (!lives) {
                alert("game over");
                document.location.reload();
            } else {
                x = canvas.width/2;
                y = canvas.height-30;
                dx = 2;
                dy = -2;
                paddleX  = (canvas.width - paddleWidth)/2;
           }
        }
    }
    if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) {
        dx = -dx;
    }
    
    ctx.beginPath();
    ctx.arc(x,y,ballRadius,0, Math.PI*2);
    ctx.fillStyle = "#9500DD";
    ctx.fill();
    ctx.closePath();
}
// drawPaddle
function drawPaddle() {
    if (rightPressed && paddleX < canvas.width-paddleWidth) {
        paddleX += 7;
    } else if (leftPressed && paddleX>0) {
        paddleX -= 7;
    }
    ctx.beginPath();
    ctx.rect(paddleX, canvas.height-paddleHeight, paddleWidth, paddleHeight);
    ctx.fillStyle = "#0095DD";
    ctx.fill();
    ctx.closePath();
}
   
function clearScreen()
{
    ctx.clearRect(0,0, canvas.width, canvas.height);
}

function updateBallPosition()
{
    x += dx;
    y += dy;
} 

// main draw loop
function draw() {
    // request future draw call.
    requestAnimationFrame(draw);
    now = Date.now();
    elapsed = now-last;
    if (elapsed > fpsInterval) {
        last = now - (elapsed % fpsInterval);
        clearScreen();
        drawBricks();
        drawBall();
        drawPaddle();
        collisionDetection();
        drawScore();
        drawLives();
    }
    updateBallPosition();
}

// refresh rate and loop hookup
// setInterval(draw, 10);
var fpsInterval = 1000/60;  
var last=Date.now();
var startTime=last;
draw();

// event listeners
document.addEventListener("keydown", keyDownHandler,  false);
document.addEventListener("keyup", keyUpHandler,  false);
document.addEventListener("mousemove", mouseMoveHandler, false);

function mouseMoveHandler(e) {
    var relativeX = e.clientX - canvas.offsetLeft;
    if (relativeX >0 && relativeX < canvas.width) {
        paddleX = relativeX - paddleWidth/2;
    }
}

function keyDownHandler(e) {
    if (e.keyCode == 39) {
        rightPressed = true;
    } else if (e.keyCode == 37) {
        leftPressed = true;
    }
}

function keyUpHandler(e) {
    if (e.keyCode == 39) {
        rightPressed = false;
    } else if (e.keyCode == 37) {
        leftPressed = false;
    }
}



