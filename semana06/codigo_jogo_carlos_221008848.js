
// VARIÁVEIS DO JOGO

var score = 0;

var speed = 2;





var bunny = createSprite(200, 350);
bunny.setAnimation("bunny1_ready_1"); 
bunny.scale = 0.8; // tamanho do personagem
bunny.setCollider("rectangle", 0, 0, 50, 60);

// objeto que cai (bola de sinuca)
var ball = createSprite(200, 50);
ball.setAnimation("eightball_1");
ball.scale = 0.5;
ball.setCollider("circle", 0, 0, 20);





// fase 1 do jogo 
function drawSimpleBackground(){
  background("lightblue");
  fill("green");
  rect(0, 350, 400, 50);
}

// fase intermediária 
function drawMidBackground(){
  background("purple");
  fill("white");
  ellipse(200, 100, 80, 80);
}

// tela de vitória
function drawWinBackground(){
  background("yellow");
  fill("orange");
  ellipse(200, 100, 100, 100);
}



// FUNÇÃO DE SCORE 

function showScore(){
  fill("black");
  textSize(20);
  text("Score: " + score, 10, 20);
}




// controle do jogador 
function movePlayer(){
  if(keyDown("left")){
    bunny.x = bunny.x - 3;
  }
  if(keyDown("right")){
    bunny.x = bunny.x + 3;
  }
}

// bola caindo
function moveBall(){
  ball.y = ball.y + speed;
}


function resetBall(){
  ball.y = 50;
  ball.x = randomNumber(0, 400);
}



// INTERAÇÕES DO JOGO


function checkBallCatch(){
  if(bunny.isTouching(ball)){
    score = score + 1;   
    speed = speed + 0.2;  
    resetBall();          
  }
}

function checkBallMiss(){
  if(ball.y > 400){
    resetBall();
  }
}




function draw() {

  
  if(score < 5){
    drawSimpleBackground(); 
  } 
  else if(score < 10){
    drawMidBackground(); 
  } 
  else {
    drawWinBackground(); 
  }


  movePlayer();
  moveBall();


  checkBallCatch();
  checkBallMiss();


  showScore();

 
  drawSprites();
}
