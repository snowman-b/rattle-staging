// RATTLE Snake Game - HTML5/JS Conversion
// Best practices, maintainable, secure, efficient

const CELL_SIZE = 20;
const GRID_WIDTH = 30;
const GRID_HEIGHT = 20;
const ARENA_WIDTH = CELL_SIZE * GRID_WIDTH;
const ARENA_HEIGHT = CELL_SIZE * GRID_HEIGHT;
const MARGIN_TOP = 100;
const MARGIN_LEFT = 200;
const MARGIN_RIGHT = 200;
const MARGIN_BOTTOM = 500;
const WIDTH = ARENA_WIDTH + MARGIN_LEFT + MARGIN_RIGHT;
const HEIGHT = ARENA_HEIGHT + MARGIN_TOP + MARGIN_BOTTOM;
const BASE_FPS = 10;
const SPEED_LEVELS = [0.25, 0.5, 0.75, 1.0, 1.25];
let speedIndex = 3; // Start at normal speed
let fps = BASE_FPS * SPEED_LEVELS[speedIndex];

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
let lastFrame = 0;
let running = true;
let direction = {x: 1, y: 0};
let directionQueue = [];
let lastDirection = {x: 1, y: 0};
let snake = [];
let foods = [];
let score = 0;
let elapsedSeconds = 0;
let startTime = null;
let win = false;
let endlessMode = false;
let snakeInMotion = false;

// Example: today's word
const TODAY_WORD = 'SNAKE';

function startSnakeMotion() {
  snakeInMotion = true;
}
function stopSnakeMotion() {
  snakeInMotion = false;
}

function getFoodPositionsForWord(word) {
  // Evenly space letters across a horizontal row (row 10)
  const row = 10; // was 9, now 10
  const spacing = Math.floor(GRID_WIDTH / (word.length + 1));
  let positions = [];
  for (let i = 0; i < word.length; i++) {
    positions.push({
      x: spacing * (i + 1),
      y: row,
      letter: word[i]
    });
  }
  return positions;
}

function resetGame() {
  direction = {x: 1, y: 0};
  directionQueue = [];
  snake = [
    {x: 3, y: GRID_HEIGHT - 3},
    {x: 2, y: GRID_HEIGHT - 3},
    {x: 1, y: GRID_HEIGHT - 3}
  ];
  // Spawn foods for today's word
  foods = getFoodPositionsForWord(TODAY_WORD);
  score = 0;
  elapsedSeconds = 0;
  startTime = Date.now();
  win = false;
  endlessMode = false;
  startSnakeMotion(); // Start motion on game start
  // TODO: Add word logic, food placement, etc.
}

function drawArena() {
  ctx.fillStyle = '#f5f5ff';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  // Draw border flush with grid
  ctx.save();
  ctx.strokeStyle = '#222';
  ctx.lineWidth = 6;
  ctx.strokeRect(3, 3, canvas.width - 6, canvas.height - 6);
  ctx.restore();
}

function drawSnake() {
  ctx.save();
  for (let i = 0; i < snake.length; i++) {
    ctx.fillStyle = '#50c878';
    ctx.fillRect(snake[i].x * CELL_SIZE, snake[i].y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
  }
  ctx.restore();
}

function drawFoods() {
  ctx.save();
  ctx.font = '20px Avenir Next, Arial, sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  for (let food of foods) {
    ctx.fillStyle = '#222';
    ctx.fillRect(food.x * CELL_SIZE, food.y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
    ctx.fillStyle = '#fff';
    ctx.fillText(food.letter, food.x * CELL_SIZE + CELL_SIZE/2, food.y * CELL_SIZE + CELL_SIZE/2);
  }
  ctx.restore();
}

function drawScore() {
  // Remove canvas score drawing
  const scoreboardDiv = document.getElementById('scoreboard');
  if (scoreboardDiv) {
    scoreboardDiv.textContent = 'Score: ' + score;
  }
}

let lastKeyDir = null;
let lastKeyTime = 0;

function getDirFromKey(e) {
  if (e.key === 'ArrowUp') return {x: 0, y: -1};
  if (e.key === 'ArrowDown') return {x: 0, y: 1};
  if (e.key === 'ArrowLeft') return {x: -1, y: 0};
  if (e.key === 'ArrowRight') return {x: 1, y: 0};
  return null;
}

document.addEventListener('keydown', (e) => {
  if (snakeInMotion && ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key)) {
    e.preventDefault();
  }
  const newDir = getDirFromKey(e);
  if (!newDir) return;
  const now = Date.now();
  // If this is the second consecutive press in the same direction within 500ms, treat as speed change
  if (lastKeyDir && newDir.x === lastKeyDir.x && newDir.y === lastKeyDir.y && now - lastKeyTime < 500) {
    // Speed control
    if (newDir.x === direction.x && newDir.y === direction.y) {
      if (speedIndex < SPEED_LEVELS.length - 1) speedIndex++;
    } else if (isOpposite(newDir, direction)) {
      if (speedIndex > 0) speedIndex--;
    }
    fps = BASE_FPS * SPEED_LEVELS[speedIndex];
    lastKeyDir = null; // Reset so only double-tap triggers speed
    return;
  }
  // Otherwise, queue movement
  const last = directionQueue.length ? directionQueue[directionQueue.length - 1] : direction;
  if (!isOpposite(last, newDir)) {
    directionQueue.push(newDir);
  }
  lastKeyDir = newDir;
  lastKeyTime = now;
});

function gameLoop(timestamp) {
  if (!running) return;
  if (!lastFrame) lastFrame = timestamp;
  const delta = timestamp - lastFrame;
  if (delta > 1000 / fps) {
    update();
    render();
    lastFrame = timestamp;
  }
  requestAnimationFrame(gameLoop);
}

function isOpposite(dir1, dir2) {
  return dir1.x === -dir2.x && dir1.y === -dir2.y;
}

function update() {
  // Apply the next direction in the queue, if any
  if (directionQueue.length) {
    const nextDir = directionQueue.shift();
    if (!isOpposite(direction, nextDir)) {
      direction = nextDir;
    }
  }
  // Move snake
  const newHead = {
    x: snake[0].x + direction.x,
    y: snake[0].y + direction.y
  };
  // Edge collision
  if (
    newHead.x < 0 || newHead.x >= GRID_WIDTH ||
    newHead.y < 0 || newHead.y >= GRID_HEIGHT
  ) {
    running = false;
    stopSnakeMotion(); // Stop motion on game over
    showShareModal();
    return;
  }
  // Self collision
  for (let i = 0; i < snake.length; i++) {
    if (snake[i].x === newHead.x && snake[i].y === newHead.y) {
      running = false;
      stopSnakeMotion(); // Stop motion on game over
      showShareModal();
      return;
    }
  }
  // Food eating
  let ateFood = false;
  for (let i = 0; i < foods.length; i++) {
    if (foods[i].x === newHead.x && foods[i].y === newHead.y) {
      score++;
      foods.splice(i, 1); // Remove eaten food
      ateFood = true;
      break;
    }
  }
  snake.unshift(newHead);
  if (!ateFood) {
    snake.pop(); // Only grow if food was eaten
  }
  lastDirection = direction;
}

function render() {
  drawArena();
  drawSnake();
  drawFoods();
  drawScore();
}

function showShareModal() {
  const modal = document.getElementById('shareModal');
  const dateDiv = document.getElementById('modalDate');
  const scoreDiv = document.getElementById('modalScore');
  dateDiv.textContent = new Date().toLocaleDateString('en-US', {month: 'long', day: 'numeric', year: 'numeric'});
  scoreDiv.textContent = 'Score: ' + score;
  modal.style.display = 'flex';
}

function hideShareModal() {
  document.getElementById('shareModal').style.display = 'none';
}

document.getElementById('modalHome').onclick = () => {
  hideShareModal();
  resetGame();
  running = true;
  requestAnimationFrame(gameLoop);
};
document.getElementById('modalClose').onclick = () => {
  hideShareModal();
  // TODO: Show view-only final game screen
};

resetGame();
running = true;
requestAnimationFrame(gameLoop);
