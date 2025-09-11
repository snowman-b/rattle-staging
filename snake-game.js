// Respawn snake after loss (wall/self collision)
function respawnSnakeAfterLoss() {
  setTimeout(() => {
    direction = {x: 1, y: 0};
    directionQueue = [];
    snake = [
      {x: 3, y: GRID_HEIGHT - 3},
      {x: 2, y: GRID_HEIGHT - 3},
      {x: 1, y: GRID_HEIGHT - 3}
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
  // Show the invalid word as a single string with strikethrough at a random location
  const garbageWordSpan = document.getElementById('garbageWord');
  const container = document.getElementById('garbageCanContainer');
  if (garbageWordSpan && container) {
    garbageWordSpan.textContent = word.toUpperCase();
    // Calculate random position within container
    // Container: 240px wide, 40px tall, 10px padding
    // Word width: estimate 33px * word.length
    const wordWidth = 33 * word.length;
  const maxLeft = Math.max(0, container.clientWidth - wordWidth - 10);
  const maxTop = Math.max(0, container.clientHeight - 33 - 10);
  // Snap to 100px increments for maximum visible variation
  const left = Math.round((Math.random() * maxLeft) / 100) * 100 + 5;
  const top = Math.round((Math.random() * maxTop) / 100) * 100 + 5;
  garbageWordSpan.style.left = left + 'px';
  garbageWordSpan.style.top = top + 'px';
    // Random tilt between -20 and +20 degrees
    const tilt = (Math.random() * 40 - 20).toFixed(2);
    garbageWordSpan.style.transform = `rotate(${tilt}deg)`;
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
  // Evenly space letters across a horizontal row (row 10)
  const row = 10;
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
  let positions = [];
  for (let i = 0; i < letters.length; i++) {
    positions.push({
      x: spacing * (i + 1),
      y: row,
      letter: letters[i].toUpperCase()
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
  // Draw border flush with grid
  ctx.save();
  // Wall coordinates and cell height (declare once)
  const wallLeftX = 3;
  const wallX = canvas.width - 3;
  const cellHeight = (canvas.height - 6) / GRID_HEIGHT;
  // Left wall: top sixteen segments black, rest red, bottommost segment black except top 5px red
  ctx.strokeStyle = '#222';
  ctx.lineWidth = 6;
  ctx.beginPath();
  ctx.moveTo(wallLeftX, 3 - 5);
  ctx.lineTo(wallLeftX, 3 + cellHeight * 16);
  ctx.stroke();
  // Red portal: from sixteen segments to one above bottom, 30px thick with 2px black border
  const redPortalThickness = 30;
  const redPortalBorder = 2;
  // Draw red portal
  ctx.strokeStyle = '#c80000';
  ctx.lineWidth = redPortalThickness;
  ctx.beginPath();
  ctx.moveTo(wallLeftX, 3 + cellHeight * 16);
  ctx.lineTo(wallLeftX, 3 + cellHeight * (GRID_HEIGHT - 1));
  ctx.stroke();
  // Red: top 5px of bottommost segment, 30px thick
  ctx.strokeStyle = '#c80000';
  ctx.lineWidth = redPortalThickness;
  ctx.beginPath();
  ctx.moveTo(wallLeftX, 3 + cellHeight * (GRID_HEIGHT - 1));
  ctx.lineTo(wallLeftX, 3 + cellHeight * (GRID_HEIGHT - 1) + 5);
  ctx.stroke();
  // Draw black border around red portal
  ctx.strokeStyle = '#222';
  ctx.lineWidth = redPortalBorder;
  // Left edge of portal
  ctx.beginPath();
  ctx.moveTo(wallLeftX - redPortalThickness / 2, 3 + cellHeight * 16);
  ctx.lineTo(wallLeftX - redPortalThickness / 2, 3 + cellHeight * (GRID_HEIGHT - 1) + 5);
  ctx.stroke();
  // Right edge of portal
  ctx.beginPath();
  ctx.moveTo(wallLeftX + redPortalThickness / 2, 3 + cellHeight * 16);
  ctx.lineTo(wallLeftX + redPortalThickness / 2, 3 + cellHeight * (GRID_HEIGHT - 1) + 5);
  ctx.stroke();
  // Top edge of portal
  ctx.beginPath();
  ctx.moveTo(wallLeftX - redPortalThickness / 2, 3 + cellHeight * 16);
  ctx.lineTo(wallLeftX + redPortalThickness / 2, 3 + cellHeight * 16);
  ctx.stroke();
  // Bottom edge of portal
  ctx.beginPath();
  ctx.moveTo(wallLeftX - redPortalThickness / 2, 3 + cellHeight * (GRID_HEIGHT - 1) + 5);
  ctx.lineTo(wallLeftX + redPortalThickness / 2, 3 + cellHeight * (GRID_HEIGHT - 1) + 5);
  ctx.stroke();
  // Restore line width for other walls
  ctx.lineWidth = 6;
  // Black: rest of bottommost segment
  ctx.strokeStyle = '#222';
  ctx.beginPath();
  ctx.moveTo(wallLeftX, 3 + cellHeight * (GRID_HEIGHT - 1) + 5);
  ctx.lineTo(wallLeftX, canvas.height - 3 + 5);
  ctx.stroke();
  // Top and bottom walls (black)
  ctx.strokeStyle = '#222';
  ctx.beginPath();
  // Top wall
  ctx.moveTo(3, 3);
  ctx.lineTo(canvas.width - 3, 3);
  // Bottom wall
  ctx.moveTo(3, canvas.height - 3);
  ctx.lineTo(canvas.width - 3, canvas.height - 3);
  ctx.stroke();
  // Right wall: top half plus 6 segments in black, bottommost segment in black, section between in green
  // Black: from top to (half + 6 segments), extended 5px at top
  ctx.strokeStyle = '#222';
  ctx.lineWidth = 6;
  ctx.beginPath();
  ctx.moveTo(wallX, 3 - 5);
  ctx.lineTo(wallX, 3 + cellHeight * (GRID_HEIGHT / 2 + 6));
  ctx.stroke();
  // Green portal: from (half + 6 segments) to one above bottom, 30px thick with 2px black border
  const portalThickness = 30;
  const portalBorder = 2;
  // Draw green portal
  ctx.strokeStyle = '#00c800';
  ctx.lineWidth = portalThickness;
  ctx.beginPath();
  ctx.moveTo(wallX, 3 + cellHeight * (GRID_HEIGHT / 2 + 6));
  ctx.lineTo(wallX, 3 + cellHeight * (GRID_HEIGHT - 1));
  ctx.stroke();
  // Light green top 5px of bottommost segment (portal color), 30px thick
  ctx.strokeStyle = '#00c800';
  ctx.lineWidth = portalThickness;
  ctx.beginPath();
  ctx.moveTo(wallX, 3 + cellHeight * (GRID_HEIGHT - 1));
  ctx.lineTo(wallX, 3 + cellHeight * (GRID_HEIGHT - 1) + 5);
  ctx.stroke();
  // Draw black border around portal
  ctx.strokeStyle = '#222';
  ctx.lineWidth = portalBorder;
  // Left edge of portal
  ctx.beginPath();
  ctx.moveTo(wallX - portalThickness / 2, 3 + cellHeight * (GRID_HEIGHT / 2 + 6));
  ctx.lineTo(wallX - portalThickness / 2, 3 + cellHeight * (GRID_HEIGHT - 1) + 5);
  ctx.stroke();
  // Right edge of portal
  ctx.beginPath();
  ctx.moveTo(wallX + portalThickness / 2, 3 + cellHeight * (GRID_HEIGHT / 2 + 6));
  ctx.lineTo(wallX + portalThickness / 2, 3 + cellHeight * (GRID_HEIGHT - 1) + 5);
  ctx.stroke();
  // Top edge of portal
  ctx.beginPath();
  ctx.moveTo(wallX - portalThickness / 2, 3 + cellHeight * (GRID_HEIGHT / 2 + 6));
  ctx.lineTo(wallX + portalThickness / 2, 3 + cellHeight * (GRID_HEIGHT / 2 + 6));
  ctx.stroke();
  // Bottom edge of portal
  ctx.beginPath();
  ctx.moveTo(wallX - portalThickness / 2, 3 + cellHeight * (GRID_HEIGHT - 1) + 5);
  ctx.lineTo(wallX + portalThickness / 2, 3 + cellHeight * (GRID_HEIGHT - 1) + 5);
  ctx.stroke();
  // Restore line width for other walls
  ctx.lineWidth = 6;
  // Black rest of bottommost segment
  ctx.strokeStyle = '#222';
  ctx.beginPath();
  ctx.moveTo(wallX, 3 + cellHeight * (GRID_HEIGHT - 1) + 5);
  ctx.lineTo(wallX, canvas.height - 3 + 5);
  ctx.stroke();
  // Draw portals
  // Green portal (right)
  ctx.save();
  ctx.fillStyle = '#00c800'; // Green
  let portalYStart = (GRID_HEIGHT - 4) * CELL_SIZE;
  let portalHeight = 3 * CELL_SIZE;
  ctx.fillRect(MARGIN_LEFT + ARENA_WIDTH - 8, MARGIN_TOP + portalYStart, 8, portalHeight);
  ctx.restore();
  // Red portal (left)
  ctx.save();
  ctx.fillStyle = '#c80000'; // Red
  ctx.fillRect(MARGIN_LEFT, MARGIN_TOP + portalYStart, 8, portalHeight);
  ctx.restore();
  ctx.restore();
}

function drawSnake() {
  ctx.save();
  for (let i = 0; i < snake.length; i++) {
  ctx.fillStyle = '#00c800'; // Match portal green
  ctx.fillRect(snake[i].x * CELL_SIZE, snake[i].y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
  // Draw only the true outer perimeter of the snake in black
  if (snake.length > 0) {
    ctx.save();
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    for (let i = 0; i < snake.length; i++) {
      const seg = snake[i];
      const x = seg.x * CELL_SIZE;
      const y = seg.y * CELL_SIZE;
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
        ctx.lineTo(x + CELL_SIZE, y);
        ctx.stroke();
      }
      // Bottom edge
      const botIdx = snake.findIndex(s => s.x === seg.x && s.y === seg.y + 1);
      if (botIdx === -1 || !isSequential(botIdx)) {
        ctx.beginPath();
        ctx.moveTo(x, y + CELL_SIZE);
        ctx.lineTo(x + CELL_SIZE, y + CELL_SIZE);
        ctx.stroke();
      }
      // Left edge
      const leftIdx = snake.findIndex(s => s.x === seg.x - 1 && s.y === seg.y);
      if (leftIdx === -1 || !isSequential(leftIdx)) {
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x, y + CELL_SIZE);
        ctx.stroke();
      }
      // Right edge
      const rightIdx = snake.findIndex(s => s.x === seg.x + 1 && s.y === seg.y);
      if (rightIdx === -1 || !isSequential(rightIdx)) {
        ctx.beginPath();
        ctx.moveTo(x + CELL_SIZE, y);
        ctx.lineTo(x + CELL_SIZE, y + CELL_SIZE);
        ctx.stroke();
      }
    }
    ctx.restore();
  }
    // Draw collected letters: newest always in second segment, older letters shift toward tail
    if (i > 0 && i <= collectedLetters.length) {
      ctx.save();
      ctx.font = '20px Avenir Next, Arial, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = '#000';
      // Place newest letter in second segment, older letters shift toward tail
      let letterIndex = collectedLetters.length - i;
      if (letterIndex >= 0) {
        ctx.fillText(collectedLetters[letterIndex], snake[i].x * CELL_SIZE + CELL_SIZE/2, snake[i].y * CELL_SIZE + CELL_SIZE/2 + 2);
      }
      ctx.restore();
    }
  }
  ctx.restore();
}

function drawFoods() {
  ctx.save();
  ctx.font = '20px Avenir Next, Arial, sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  for (let food of foods) {
    ctx.fillStyle = '#000';
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
  // Portal logic: green portal (right) to red portal (left)
  let portalYStart = GRID_HEIGHT - 4;
  let portalYEnd = GRID_HEIGHT - 1;
  let onGreenPortal = (snake[0].x === GRID_WIDTH - 1 && snake[0].y >= portalYStart && snake[0].y < portalYEnd && direction.x === 1);
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
  snake = [
    {x: 3, y: GRID_HEIGHT - 3},
    {x: 2, y: GRID_HEIGHT - 3},
    {x: 1, y: GRID_HEIGHT - 3}
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

initializeSnakeAtSpawn();

// Listen for splash page dismissal
document.addEventListener('DOMContentLoaded', function() {
  // Add close functionality for modal 'x' buttons
  const endlessCloseX = document.getElementById('endlessCloseX');
  if (endlessCloseX) {
    endlessCloseX.addEventListener('click', function(e) {
      document.getElementById('endlessModal').style.display = 'none';
      document.getElementById('splashPage').style.display = 'flex';
      e.stopPropagation();
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
      resetGame();
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
