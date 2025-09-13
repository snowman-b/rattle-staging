// Main game speed slider logic (for in-game real-time speed adjustment)
document.addEventListener('DOMContentLoaded', function() {
  const mainSpeedSlider = document.getElementById('mainSpeedSlider');
  if (mainSpeedSlider) {
    mainSpeedSlider.addEventListener('input', function() {
      let selectedSpeed = parseInt(mainSpeedSlider.value) || 3;
      speedIndex = selectedSpeed - 1; // SPEED_LEVELS is 0-indexed
      fps = BASE_FPS * SPEED_LEVELS[speedIndex];
    });
  }
});
// Respawn snake after loss (wall/self collision)
function respawnSnakeAfterLoss() {
  setTimeout(() => {
    direction = {x: 1, y: 0};
    directionQueue = [];
    // Snake starts at 10% from left, 85% from top, 3 segments long horizontally
    const startX = Math.floor(GRID_WIDTH * 0.10);
    const startY = Math.floor(GRID_HEIGHT * 0.85);
    snake = [
      {x: startX, y: startY},
      {x: startX - 1, y: startY},
      {x: startX - 2, y: startY}
    ];
    collectedLetters = [];
    // Foods remain as per today's word
    const todayWord = getTodayWord();
    foods = getFoodPositionsForWord(todayWord);
    running = true;
    win = false;
    startSnakeMotion();
    lastFrame = 0;
    // Timer resumes
    if (!timerInterval) {
      startTime = Date.now();
      timerInterval = setInterval(() => {
        if (running) {
          elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);
          drawTimer();
        }
      }, 1000);
    }
    requestAnimationFrame(gameLoop);
  }, 2000);
}
let submittedWords = new Set();
// Track which rows are filled with a valid word
let wordRowsFilled = { 1: false, 2: false, 3: false, 4: false, 5: false, 6: false };

function checkWinCondition() {
  for (let i = 1; i <= 6; i++) {
    if (!wordRowsFilled[i]) return false;
  }
  return true;
}
// Update word collection UI: show word in corresponding row, one letter per box
// Update garbage collection UI: show invalid word in corresponding row, one letter per box
function updateGarbageCollectionUI(word) {
  // Show the invalid word as a single string with strikethrough at a random location in the word collection card
  const container = document.getElementById('invalidWordsContainer');
  if (container) {
    const span = document.createElement('span');
    span.textContent = word.toUpperCase();
    span.style.position = 'absolute';
    span.style.textDecoration = 'line-through';
    span.style.fontSize = '2vw';
    span.style.color = '#a00';
    // Container: full size of wordCollectionCard, but avoid center region (letter boxes)
    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;
    // Avoid center 60% horizontally, 60% vertically
    let left, top;
    if (Math.random() < 0.5) {
      // Left side
      left = Math.random() * (containerWidth * 0.15);
    } else {
      // Right side
      left = containerWidth * 0.85 + Math.random() * (containerWidth * 0.15 - 50);
    }
    top = Math.random() * (containerHeight * 0.8);
    span.style.left = left + 'px';
    span.style.top = top + 'px';
    // Random tilt between -20 and +20 degrees
    const tilt = (Math.random() * 40 - 20).toFixed(2);
    span.style.transform = `rotate(${tilt}deg)`;
    span.style.pointerEvents = 'none';
    container.appendChild(span);
    // Optionally fade out after a few seconds
    setTimeout(() => { span.remove(); }, 4000);
  }
}
function updateWordCollectionUI(word) {
  const len = word.length;
  if (len < 1 || len > 6) return;
  const row = document.getElementById('wordRow' + len);
  if (!row) return;
  const boxes = row.getElementsByClassName('word-box');
  // Clear all boxes in the row
  for (let i = 0; i < boxes.length; i++) {
    boxes[i].textContent = '';
  }
  // Fill boxes with letters of the word
  for (let i = 0; i < word.length && i < boxes.length; i++) {
    boxes[i].textContent = word[i].toUpperCase();
  }
}
  submittedWords.clear();
let collectedLetters = [];
let wordsSet = null;
// Load all_words.txt once and cache
function loadWordList() {
  window.fetch('all_words.txt')
    .then(response => response.text())
    .then(text => {
      wordsSet = new Set(text.split(/\r?\n/).map(w => w.trim().toLowerCase()));
    });
}
loadWordList();

// --- Daily Words CSV Loader ---
let dailyWordsMap = null;
let dailyWordsLoaded = false;

function loadDailyWordsCSV() {
  return window.fetch('daily-words.csv')
    .then(response => response.text())
    .then(text => {
      dailyWordsMap = {};
      const lines = text.split(/\r?\n/);
      for (let i = 1; i < lines.length; i++) { // skip header
        const [date, word] = lines[i].split(',');
        if (date && word) dailyWordsMap[date.trim()] = word.trim();
      }
      dailyWordsLoaded = true;
    });
}
// Load CSV on page load
loadDailyWordsCSV();
  collectedLetters = [];
// RATTLE Snake Game - HTML5/JS Conversion
// Best practices, maintainable, secure, efficient

const GRID_WIDTH = 24;
const GRID_HEIGHT = 16;
let cellWidth = 20;
let cellHeight = 20;
// cellWidth and cellHeight will be recalculated in resizeArenaCanvas after DOM is ready
function resizeArenaCanvas() {
  // Get arenaCard container
  const arenaCard = document.getElementById('arenaCard');
  if (!arenaCard || !canvas) return;
  // Calculate width: 90vw, max 800px
  const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
  let width = Math.min(vw * 0.9, 800);
  let height = width * 2 / 3;
  // Set container size (for flex alignment)
  arenaCard.style.width = width + 'px';
  arenaCard.style.height = height + 'px';
  // Set canvas size
  canvas.width = width;
  canvas.height = height;
  // Update cell size for grid
  cellWidth = width / GRID_WIDTH;
  cellHeight = height / GRID_HEIGHT;
  // Redraw everything
  if (typeof render === 'function') render();
}

// Resize on load and window resize
window.addEventListener('resize', resizeArenaCanvas);
window.addEventListener('DOMContentLoaded', resizeArenaCanvas);
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
let timerInterval = null;
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

function getTodayWord() {
  const today = new Date();
  const todayStr = `${today.getMonth()+1}/${today.getDate()}/${today.getFullYear()}`;
  if (dailyWordsLoaded && dailyWordsMap) {
    return dailyWordsMap[todayStr] || 'rattle';
  }
  // If not loaded yet, fallback
  return 'rattle';
}

function getFoodPositionsForWord(word) {
  // Evenly space letters across a horizontal row, 7 snake lengths from the bottom
  const row = GRID_HEIGHT - 7;
  const spacing = Math.floor(GRID_WIDTH / (word.length + 1));
  // Deterministic shuffle based on today's date
  function seededShuffle(array, seed) {
    let arr = array.slice();
    let rng = mulberry32(seed);
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(rng() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }
  // Simple seeded RNG
  function mulberry32(a) {
    return function() {
      var t = a += 0x6D2B79F5;
      t = Math.imul(t ^ t >>> 15, t | 1);
      t ^= t + Math.imul(t ^ t >>> 7, t | 61);
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    }
  }
  // Use date as seed
  const today = new Date();
  const seed = today.getFullYear() * 10000 + (today.getMonth()+1) * 100 + today.getDate();
  let letters = word.split('');
  letters = seededShuffle(letters, seed);
  // Fixed positions for 6 letters: 5,8,11,14,17,20
  const fixedPositions = [4, 7, 10, 13, 16, 19];
  let positions = [];
  for (let i = 0; i < Math.min(letters.length, fixedPositions.length); i++) {
    positions.push({
      x: fixedPositions[i],
      y: row,
      letter: letters[i].toUpperCase()
    });
  }
  return positions;
}

function resetGame() {
  direction = {x: 1, y: 0};
  directionQueue = [];
  // Snake starts at 10% from left, 85% from top, 3 segments long horizontally
  const startX = Math.floor(GRID_WIDTH * 0.10);
  const startY = Math.floor(GRID_HEIGHT * 0.85);
  snake = [
    {x: startX, y: startY},
    {x: startX - 1, y: startY},
    {x: startX - 2, y: startY}
  ];
  // Use today's word from word-list
  const todayWord = getTodayWord();
  foods = getFoodPositionsForWord(todayWord);
  score = 0;
  elapsedSeconds = 0;
  startTime = Date.now();
  win = false;
  endlessMode = false;
  startSnakeMotion(); // Start motion on game start
  // Start timer
  if (timerInterval) clearInterval(timerInterval);
  timerInterval = setInterval(() => {
    if (!win) {
      elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);
      drawTimer();
    }
  }, 1000);
  drawTimer();
  // TODO: Add word logic, food placement, etc.
function drawTimer() {
  const timerDiv = document.getElementById('timer');
  if (timerDiv) {
    const minutes = Math.floor(elapsedSeconds / 60);
    const seconds = elapsedSeconds % 60;
    const mm = String(minutes).padStart(2, '0');
    const ss = String(seconds).padStart(2, '0');
    timerDiv.textContent = `Time: ${mm}:${ss}`;
  }
}
}

function drawArena() {
  ctx.fillStyle = '#f5f5ff';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.save();
  // Walls: grid-aligned
  ctx.strokeStyle = '#222';
  ctx.lineWidth = 6;
  // Left wall
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.lineTo(0, GRID_HEIGHT * cellHeight);
  ctx.stroke();
  // Right wall
  ctx.beginPath();
  ctx.moveTo(GRID_WIDTH * cellWidth, 0);
  ctx.lineTo(GRID_WIDTH * cellWidth, GRID_HEIGHT * cellHeight);
  ctx.stroke();
  // Top wall
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.lineTo(GRID_WIDTH * cellWidth, 0);
  ctx.stroke();
  // Bottom wall
  ctx.beginPath();
  ctx.moveTo(0, GRID_HEIGHT * cellHeight);
  ctx.lineTo(GRID_WIDTH * cellWidth, GRID_HEIGHT * cellHeight);
  ctx.stroke();
  // Portals: grid-aligned
  const portalThickness = cellWidth * 1.5;
  const portalBorder = cellWidth * 0.1;
  // Red portal (left)
  const redPortalStartRow = Math.floor(GRID_HEIGHT * 0.80);
  const redPortalEndRow = Math.floor(GRID_HEIGHT * 0.95);
  const redPortalX = 0;
  const redPortalStartY = redPortalStartRow * cellHeight;
  const redPortalEndY = redPortalEndRow * cellHeight;
  ctx.save();
  ctx.strokeStyle = '#ff4d4d';
  ctx.lineWidth = portalThickness;
  ctx.beginPath();
  ctx.moveTo(redPortalX, redPortalStartY);
  ctx.lineTo(redPortalX, redPortalEndY);
  ctx.stroke();
  // Black border around red portal
  ctx.strokeStyle = '#222';
  ctx.lineWidth = portalBorder;
  // Left edge
  ctx.beginPath();
  ctx.moveTo(redPortalX - portalThickness / 2, redPortalStartY);
  ctx.lineTo(redPortalX - portalThickness / 2, redPortalEndY);
  ctx.stroke();
  // Right edge
  ctx.beginPath();
  ctx.moveTo(redPortalX + portalThickness / 2, redPortalStartY);
  ctx.lineTo(redPortalX + portalThickness / 2, redPortalEndY);
  ctx.stroke();
  // Top edge
  ctx.beginPath();
  ctx.moveTo(redPortalX - portalThickness / 2, redPortalStartY);
  ctx.lineTo(redPortalX + portalThickness / 2, redPortalStartY);
  ctx.stroke();
  // Bottom edge
  ctx.beginPath();
  ctx.moveTo(redPortalX - portalThickness / 2, redPortalEndY);
  ctx.lineTo(redPortalX + portalThickness / 2, redPortalEndY);
  ctx.stroke();
  ctx.restore();
  // Green portal (right)
  const greenPortalStartRow = Math.floor(GRID_HEIGHT * 0.80);
  const greenPortalEndRow = Math.floor(GRID_HEIGHT * 0.95);
  const greenPortalX = GRID_WIDTH * cellWidth;
  const greenPortalStartY = greenPortalStartRow * cellHeight;
  const greenPortalEndY = greenPortalEndRow * cellHeight;
  ctx.save();
  ctx.strokeStyle = '#00c800';
  ctx.lineWidth = portalThickness;
  ctx.beginPath();
  ctx.moveTo(greenPortalX, greenPortalStartY);
  ctx.lineTo(greenPortalX, greenPortalEndY);
  ctx.stroke();
  // Black border around green portal
  ctx.strokeStyle = '#222';
  ctx.lineWidth = portalBorder;
  // Left edge
  ctx.beginPath();
  ctx.moveTo(greenPortalX - portalThickness / 2, greenPortalStartY);
  ctx.lineTo(greenPortalX - portalThickness / 2, greenPortalEndY);
  ctx.stroke();
  // Right edge
  ctx.beginPath();
  ctx.moveTo(greenPortalX + portalThickness / 2, greenPortalStartY);
  ctx.lineTo(greenPortalX + portalThickness / 2, greenPortalEndY);
  ctx.stroke();
  // Top edge
  ctx.beginPath();
  ctx.moveTo(greenPortalX - portalThickness / 2, greenPortalStartY);
  ctx.lineTo(greenPortalX + portalThickness / 2, greenPortalStartY);
  ctx.stroke();
  // Bottom edge
  ctx.beginPath();
  ctx.moveTo(greenPortalX - portalThickness / 2, greenPortalEndY);
  ctx.lineTo(greenPortalX + portalThickness / 2, greenPortalEndY);
  ctx.stroke();
  ctx.restore();
  ctx.restore();
}

function drawSnake() {
  ctx.save();
  for (let i = 0; i < snake.length; i++) {
  ctx.fillStyle = '#00c800'; // Match portal green
  ctx.fillRect(snake[i].x * cellWidth, snake[i].y * cellHeight, cellWidth, cellHeight);
  // Draw only the true outer perimeter of the snake in black
  if (snake.length > 0) {
    ctx.save();
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    for (let i = 0; i < snake.length; i++) {
      const seg = snake[i];
  const x = seg.x * cellWidth;
  const y = seg.y * cellHeight;
      // Helper to check if a segment is sequential (previous or next)
      function isSequential(j) {
        return (i > 0 && snake[j].x === snake[i-1].x && snake[j].y === snake[i-1].y) ||
               (i < snake.length-1 && snake[j].x === snake[i+1].x && snake[j].y === snake[i+1].y);
      }
      // Top edge
      const topIdx = snake.findIndex(s => s.x === seg.x && s.y === seg.y - 1);
      if (topIdx === -1 || !isSequential(topIdx)) {
        ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(x + cellWidth, y);
        ctx.stroke();
      }
      // Bottom edge
      const botIdx = snake.findIndex(s => s.x === seg.x && s.y === seg.y + 1);
      if (botIdx === -1 || !isSequential(botIdx)) {
        ctx.beginPath();
  ctx.moveTo(x, y + cellHeight);
  ctx.lineTo(x + cellWidth, y + cellHeight);
        ctx.stroke();
      }
      // Left edge
      const leftIdx = snake.findIndex(s => s.x === seg.x - 1 && s.y === seg.y);
      if (leftIdx === -1 || !isSequential(leftIdx)) {
        ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(x, y + cellHeight);
        ctx.stroke();
      }
      // Right edge
      const rightIdx = snake.findIndex(s => s.x === seg.x + 1 && s.y === seg.y);
      if (rightIdx === -1 || !isSequential(rightIdx)) {
        ctx.beginPath();
  ctx.moveTo(x + cellWidth, y);
  ctx.lineTo(x + cellWidth, y + cellHeight);
        ctx.stroke();
      }
    }
    ctx.restore();
  }
    // Draw collected letters: newest always in second segment, older letters shift toward tail
    if (i > 0 && i <= collectedLetters.length) {
      ctx.save();
  ctx.font = (cellHeight * 0.9) + 'px Avenir Next, Arial, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = '#000';
      // Place newest letter in second segment, older letters shift toward tail
      let letterIndex = collectedLetters.length - i;
      if (letterIndex >= 0) {
  ctx.fillText(collectedLetters[letterIndex], snake[i].x * cellWidth + cellWidth/2, snake[i].y * cellHeight + cellHeight/2 + 2);
      }
      ctx.restore();
    }
  }
  ctx.restore();
}

function drawFoods() {
  ctx.save();
  ctx.font = (cellHeight * 0.9) + 'px Avenir Next, Arial, sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  for (let food of foods) {
    ctx.fillStyle = '#000';
  ctx.fillText(food.letter, food.x * cellWidth + cellWidth/2, food.y * cellHeight + cellHeight/2);
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
  // Removed double-tap speed control logic
  // Otherwise, queue movement
  const last = directionQueue.length ? directionQueue[directionQueue.length - 1] : direction;
  if (!isOpposite(last, newDir)) {
    directionQueue.push(newDir);
  }
  lastKeyDir = newDir;
  lastKeyTime = now;
});

  // Make on-screen arrow buttons functional
  ['arrowUp','arrowDown','arrowLeft','arrowRight'].forEach(id => {
    const btn = document.getElementById(id);
    if (btn) {
      btn.addEventListener('click', function() {
        const keyMap = {
          arrowUp: 'ArrowUp',
          arrowDown: 'ArrowDown',
          arrowLeft: 'ArrowLeft',
          arrowRight: 'ArrowRight'
        };
        // Create a synthetic KeyboardEvent for the corresponding arrow key
        const event = new KeyboardEvent('keydown', { key: keyMap[id] });
        document.dispatchEvent(event);
      });
    }
  });

function gameLoop(timestamp) {
  if (!running || win) return;
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
  let newHead = {
    x: snake[0].x + direction.x,
    y: snake[0].y + direction.y
  };
  // Responsive portal logic: green portal (right) to red portal (left)
  const portalStartRow = Math.floor(GRID_HEIGHT * 0.80);
  const portalEndRow = Math.floor(GRID_HEIGHT * 0.95);
  let onGreenPortal = (
    snake[0].x === GRID_WIDTH - 1 &&
    snake[0].y >= portalStartRow &&
    snake[0].y < portalEndRow &&
    direction.x === 1
  );
  if (onGreenPortal) {
    // Teleport to red portal
    newHead.x = 0;
    // Check if collected letters form a valid word
    if (collectedLetters.length > 0 && wordsSet) {
      const formedWord = collectedLetters.join('').toLowerCase();
      if (wordsSet.has(formedWord) && !submittedWords.has(formedWord)) {
  score += collectedLetters.length;
  drawScore();
  submittedWords.add(formedWord);
  updateWordCollectionUI(formedWord);
  // Mark row as filled
  let len = formedWord.length;
  if (len >= 1 && len <= 6) {
    wordRowsFilled[len] = true;
  }
  // Check win condition
  if (checkWinCondition()) {
    win = true;
    running = false;
    stopSnakeMotion();
    if (timerInterval) clearInterval(timerInterval);
    showShareModal();
    return;
  }
      }
          // Word is not valid: update garbage container
          // Only show in garbage if truly invalid (not in wordsSet or already submitted)
          // Only show in garbage if truly invalid (not in wordsSet or already submitted)
          if (
            formedWord.length > 0 &&
            !wordsSet.has(formedWord.toLowerCase())
          ) {
            updateGarbageCollectionUI(formedWord);
          }
    }
    // Respawn all collected letters to their original locations
    collectedLetters = [];
    const todayWord = getTodayWord();
    foods = getFoodPositionsForWord(todayWord);
  }
  // Edge collision (except for portal)
  let collided = false;
  if (
    (newHead.x < 0 || newHead.x >= GRID_WIDTH || newHead.y < 0 || newHead.y >= GRID_HEIGHT)
    && !onGreenPortal
  ) {
    collided = true;
  }
  if (collided) {
  running = false;
  stopSnakeMotion(); // Stop motion on game over
  // Do not show splash page; respawn after 2 seconds
  collectedLetters = [];
  respawnSnakeAfterLoss();
  return;
  }
  // Self collision
  for (let i = 0; i < snake.length; i++) {
    if (snake[i].x === newHead.x && snake[i].y === newHead.y) {
      running = false;
      stopSnakeMotion(); // Stop motion on game over
      // Do not show splash page; respawn after 2 seconds
      collectedLetters = [];
      respawnSnakeAfterLoss();
      return;
    }
  }
  // Food eating
  let ateFood = false;
  for (let i = 0; i < foods.length; i++) {
    if (foods[i].x === newHead.x && foods[i].y === newHead.y) {
      collectedLetters.push(foods[i].letter);
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
  const timeDiv = document.getElementById('modalTime');
  dateDiv.textContent = new Date().toLocaleDateString('en-US', {month: 'long', day: 'numeric', year: 'numeric'});
  scoreDiv.textContent = 'Score: ' + score;
  // Show final time in MM:SS format
  const minutes = Math.floor(elapsedSeconds / 60);
  const seconds = elapsedSeconds % 60;
  const mm = String(minutes).padStart(2, '0');
  const ss = String(seconds).padStart(2, '0');
  if (timeDiv) {
    timeDiv.textContent = `Time: ${mm}:${ss}`;
  }
  modal.style.display = 'flex';
}

function hideShareModal() {
  document.getElementById('shareModal').style.display = 'none';
}

document.getElementById('modalHome').onclick = () => {
  hideShareModal();
  // Show splash page, hide game
  document.getElementById('splashPage').style.display = 'flex';
  document.getElementById('mainGame').style.display = 'none';
  // Optionally, re-initialize snake at spawn
  initializeSnakeAtSpawn();
  running = false;
};
document.getElementById('modalClose').onclick = () => {
  hideShareModal();
  // TODO: Show view-only final game screen
};


// Only initialize snake at spawn, motionless, timer stopped
function initializeSnakeAtSpawn() {
  direction = {x: 1, y: 0};
  directionQueue = [];
  speedIndex = 2; // Start one level slower than normal ONLY on initialization
  fps = BASE_FPS * SPEED_LEVELS[speedIndex];
  // Snake starts at 10% from left, 85% from top, 3 segments long horizontally
  const startX = Math.floor(GRID_WIDTH * 0.10);
  const startY = Math.floor(GRID_HEIGHT * 0.85);
  snake = [
    {x: startX, y: startY},
    {x: startX - 1, y: startY},
    {x: startX - 2, y: startY}
  ];
  const todayWord = getTodayWord();
  foods = getFoodPositionsForWord(todayWord);
  score = 0;
  elapsedSeconds = 0;
  win = false;
  endlessMode = false;
  collectedLetters = [];
  submittedWords.clear();
  wordRowsFilled = { 1: false, 2: false, 3: false, 4: false, 5: false, 6: false };
  // Clear garbage word display
  const garbageWordSpan = document.getElementById('garbageWord');
  if (garbageWordSpan) garbageWordSpan.textContent = '';
  // Clear all word collection rows
  for (let i = 1; i <= 6; i++) {
    const row = document.getElementById('wordRow' + i);
    if (row) {
      const boxes = row.getElementsByClassName('word-box');
      for (let j = 0; j < boxes.length; j++) {
        boxes[j].textContent = '';
      }
    }
  }
  // Draw initial state
  render();
}


// Listen for splash page dismissal
document.addEventListener('DOMContentLoaded', function() {
  // Speed slider logic for Endless Mode
  const endlessSpeedSlider = document.getElementById('endlessSpeedSlider');
  const endlessSpeedValue = document.getElementById('endlessSpeedValue');
  if (endlessSpeedSlider && endlessSpeedValue) {
    endlessSpeedSlider.addEventListener('input', function() {
      endlessSpeedValue.textContent = `Speed: ${endlessSpeedSlider.value}`;
    });
  }

  // Speed slider logic for Time Trial Mode
  const ttSpeedSlider = document.getElementById('ttSpeedSlider');
  const ttSpeedValue = document.getElementById('ttSpeedValue');
  if (ttSpeedSlider && ttSpeedValue) {
    ttSpeedSlider.addEventListener('input', function() {
      ttSpeedValue.textContent = `Speed: ${ttSpeedSlider.value}`;
    });
  }
  // Add close functionality for modal 'x' buttons
  const endlessCloseX = document.getElementById('endlessCloseX');
  if (endlessCloseX) {
    endlessCloseX.addEventListener('click', function(e) {
      document.getElementById('endlessModal').style.display = 'none';
      document.getElementById('splashPage').style.display = 'flex';
      e.stopPropagation();
    });
  }
  // Endless Play button logic with speed
  const endlessPlayBtn = document.getElementById('endlessPlayBtn');
  if (endlessPlayBtn) {
    endlessPlayBtn.addEventListener('click', function() {
      // Get speed from slider
      const endlessSpeedSlider = document.getElementById('endlessSpeedSlider');
      let selectedSpeed = endlessSpeedSlider ? parseInt(endlessSpeedSlider.value) : 3;
      speedIndex = selectedSpeed - 1; // SPEED_LEVELS is 0-indexed
      fps = BASE_FPS * SPEED_LEVELS[speedIndex];
      resetGame();
      endlessMode = true;
      running = true;
      requestAnimationFrame(gameLoop);
    });
  }
  const placeholderCloseX = document.getElementById('placeholderCloseX');
  if (placeholderCloseX) {
    placeholderCloseX.addEventListener('click', function(e) {
      document.getElementById('placeholderModal').style.display = 'none';
      document.getElementById('splashPage').style.display = 'flex';
      e.stopPropagation();
    });
  }
  const ttCloseX = document.getElementById('ttCloseX');
  if (ttCloseX) {
    ttCloseX.addEventListener('click', function(e) {
      document.getElementById('ttModal').style.display = 'none';
      document.getElementById('splashPage').style.display = 'flex';
      e.stopPropagation();
    });
  }
  // Game should only start when Play button is clicked in modal
  const ttPlayBtn = document.getElementById('ttPlayBtn');
  if (ttPlayBtn) {
    ttPlayBtn.addEventListener('click', function() {
      // Get speed from slider
      const ttSpeedSlider = document.getElementById('ttSpeedSlider');
      let selectedSpeed = ttSpeedSlider ? parseInt(ttSpeedSlider.value) : 3;
      speedIndex = selectedSpeed - 1; // SPEED_LEVELS is 0-indexed
      fps = BASE_FPS * SPEED_LEVELS[speedIndex];
      resetGame();
      endlessMode = false;
      running = true;
      requestAnimationFrame(gameLoop);
    });
  }

  // Allow clicking outside Time Trial modal content to close it
  const ttModal = document.getElementById('ttModal');
  if (ttModal) {
    ttModal.addEventListener('click', function(e) {
      // Only close if clicking the background, not the modal content
      if (e.target === ttModal) {
        ttModal.style.display = 'none';
        document.getElementById('splashPage').style.display = 'flex';
      }
    });
  }
});
