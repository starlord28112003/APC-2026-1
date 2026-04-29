
// VARIÁVEIS DO JOGO


// pontuação do jogador
var score = 0;

// velocidade da bola 
var speed = 2;



// CRIAÇÃO DOS SPRITES



var bunny = createSprite(200, 350);
bunny.setAnimation("bunny1_ready_1"); // imagem inicial do coelho
bunny.scale = 0.8; // tamanho do personagem
bunny.setCollider("rectangle", 0, 0, 50, 60); // área de colisão

// objeto que cai (bola de sinuca)
var ball = createSprite(200, 50);
ball.setAnimation("eightball_1");
ball.scale = 0.5;
ball.setCollider("circle", 0, 0, 20);



// FUNÇÕES DE BACKGROUND


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



// FUNÇÃO DE SCORE (PLACAR)


// mostra o score na tela
function showScore(){
  fill("black");
  textSize(20);
  text("Score: " + score, 10, 20);
}



// MOVIMENTO DOS SPRITES


// controle do jogador com teclado
function movePlayer(){
  if(keyDown("left")){
    bunny.x = bunny.x - 3;
  }
  if(keyDown("right")){
    bunny.x = bunny.x + 3;
  }
}

// bola caindo automaticamente
function moveBall(){
  ball.y = ball.y + speed;
}



// RESET DA BOLA


// reposiciona a bola no topo da tela
function resetBall(){
  ball.y = 50;
  ball.x = randomNumber(0, 400);
}



// INTERAÇÕES DO JOGO


// quando o coelho pega a bola
function checkBallCatch(){
  if(bunny.isTouching(ball)){
    score = score + 1;   // aumenta score
    speed = speed + 0.2;  // deixa o jogo mais difícil
    resetBall();          // respawna bola
  }
}

// quando a bola cai fora da tela
function checkBallMiss(){
  if(ball.y > 400){
    resetBall();
  }
}




function draw() {

  // escolha do cenário baseado no score
  if(score < 5){
    drawSimpleBackground(); // fase inicial
  } 
  else if(score < 10){
    drawMidBackground(); // fase intermediária
  } 
  else {
    drawWinBackground(); // vitória
  }


  movePlayer();
  moveBall();


  checkBallCatch();
  checkBallMiss();


  showScore();

 
  drawSprites();
}
