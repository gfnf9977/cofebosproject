<template>
  <div class="game-overlay">
    <div class="game-content">
      <button class="close-button" @click="close">&times;</button>
      <h2>Обери рівень</h2>
      <div id="difficultyMenu" v-if="!gameActive">
        <button @click="startGame('easy')">Ізі</button>
        <button @click="startGame('medium')">Стандарт</button>
        <button @click="startGame('hard')">Жостік</button>
      </div>
      <canvas id="gameCanvas" v-show="gameActive"></canvas>
      <div class="mobile-controls" v-show="gameActive">
        <button @click="movePlayer('left')">&#9664;</button>
        <button @click="movePlayer('right')">&#9654;</button>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'GameComponent',
  data() {
    return {
      gameActive: false,
      player: {
        x: 0,
        y: 0,
        width: 90,
        height: 90,
        speed: 25,
      },
      bullets: [],
      enemies: [],
      initialEnemySpeed: 3,
      levels: {
        easy: { enemySpeed: 2.7 },
        medium: { enemySpeed: 3.8 },
        hard: { enemySpeed: 5.8 },
      },
      startTime: null,
      elapsedTime: null,
    };
  },
  methods: {
    close() {
      this.$emit('close');
    },
    startGame(difficulty) {
      this.initialEnemySpeed = this.levels[difficulty].enemySpeed;
      this.gameActive = true;
      this.resetGame();
      this.startTime = Date.now();
      this.draw();
    },
    resetGame() {
      const canvas = document.getElementById('gameCanvas');
      this.player.x = canvas.width / 2 - 45;
      this.player.y = canvas.height - 120;
      this.bullets = [];
      this.enemies = [];
    },
    draw() {
      if (!this.gameActive) return;

      const canvas = document.getElementById('gameCanvas');
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const backgroundImage = new Image();
      backgroundImage.src = 'map.png'; // Replace with your background image path
      ctx.drawImage(backgroundImage, 0, 0, canvas.width, canvas.height);

      this.drawPlayer(ctx);
      this.drawBullets(ctx);
      this.drawEnemies(ctx);
      this.updateBullets();
      this.spawnEnemy();
      this.updateEnemies();
      this.checkCollisions();

      requestAnimationFrame(this.draw);
    },
    drawPlayer(ctx) {
      const playerImage = new Image();
      playerImage.src = '14785.png'; // Replace with your player image path
      ctx.drawImage(playerImage, this.player.x, this.player.y, this.player.width, this.player.height);
    },
    drawBullets(ctx) {
      const bulletImage = new Image();
      bulletImage.src = 'cup.png'; // Replace with your bullet image path
      this.bullets.forEach(bullet => {
        ctx.drawImage(bulletImage, bullet.x, bullet.y, bullet.width, bullet.height);
      });
    },
    updateBullets() {
      this.bullets.forEach(bullet => {
        bullet.y -= 15;
      });
      this.bullets = this.bullets.filter(bullet => bullet.y > 0);
    },
    spawnEnemy() {
      if (Math.random() < 0.05) {
        const enemy = {
          x: Math.random() * (window.innerWidth - 70),
          y: -70,
          width: 70,
          height: 70,
          speed: this.initialEnemySpeed,
        };
        this.enemies.push(enemy);
      }
    },
    drawEnemies(ctx) {
      const enemyImage = new Image();
      enemyImage.src = 'cup.png'; // Replace with your enemy image path
      this.enemies.forEach(enemy => {
        ctx.drawImage(enemyImage, enemy.x, enemy.y, enemy.width, enemy.height);
      });
    },
    resizeCanvas() {
      const canvas = document.getElementById('gameCanvas');
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    },
    updateEnemies() {
      this.enemies.forEach(enemy => {
        enemy.y += enemy.speed;
      });
    },
    checkCollisions() {
      this.bullets.forEach((bullet, bulletIndex) => {
        this.enemies.forEach((enemy, enemyIndex) => {
          if (
              bullet.x < enemy.x + enemy.width &&
              bullet.x + bullet.width > enemy.x &&
              bullet.y < enemy.y + enemy.height &&
              bullet.y + bullet.height > enemy.y
          ) {
            this.bullets.splice(bulletIndex, 1);
            this.enemies.splice(enemyIndex, 1);
          }
        });
      });

      this.enemies.forEach(enemy => {
        if (
            this.player.x < enemy.x + enemy.width &&
            this.player.x + this.player.width > enemy.x &&
            this.player.y < enemy.y + enemy.height &&
            this.player.y + this.player.height > enemy.y
        ) {
          this.gameOver();
        }
      });
    },
    gameOver() {
      this.gameActive = false;
      this.elapsedTime = Math.floor((Date.now() - this.startTime) / 1000);
      alert(`Game Over! You survived for ${this.elapsedTime} seconds.`);
    },
    movePlayer(direction) {
      const canvas = document.getElementById('gameCanvas');
      if (direction === 'left' && this.player.x > 0) {
        this.player.x -= this.player.speed;
      } else if (direction === 'right' && this.player.x < canvas.width - this.player.width) {
        this.player.x += this.player.speed;
      }
    },
  },

  mounted() {
    const canvas = document.getElementById('gameCanvas');
    this.resizeCanvas();

    window.addEventListener('keydown', event => {
      if (!this.gameActive) return;

      if (event.key === 'ArrowLeft' && this.player.x > 0) {
        this.player.x -= this.player.speed;
      } else if (event.key === 'ArrowRight' && this.player.x < canvas.width - this.player.width) {
        this.player.x += this.player.speed;
      } else if (event.key === ' ') {
        this.bullets.push({ x: this.player.x + this.player.width / 2 - 25 / 2, y: this.player.y });
      } else if (event.key === 'r') {
        this.resetGame();
      }
    });

    window.addEventListener('resize', this.resizeCanvas);
  },
};
</script>
<style scoped>
.game-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.game-content {
  background: linear-gradient(135deg, #ffffff, #f1f1f1);
  padding: 0; /* Remove padding */
  border-radius: 0; /* Remove border radius */
  text-align: center;
  position: relative;
  box-shadow: none; /* Remove box shadow */
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  display: flex; /* Add Flexbox */
  flex-direction: column; /* Stack children vertically */
  justify-content: center; /* Center vertically */
  align-items: center; /* Center horizontally */
}

canvas {
  display: block;
  width: 100%;
  height: 100%;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 20px;
  color: #555;
  cursor: pointer;
  transition: color 0.3s;
}

.close-button:hover {
  color: #d9534f;
}

h2 {
  margin-top: 0;
  font-size: 24px;
  font-weight: bold;
}

#difficultyMenu {
  display: flex; /* Add Flexbox */
  flex-direction: column; /* Stack buttons vertically */
  align-items: center; /* Center buttons horizontally */
}

#difficultyMenu button {
  font-size: 24px;
  padding: 15px 30px;
  margin: 10px;
  cursor: pointer;
  border: none;
  border-radius: 10px;
  background-color: #8e44ad;
  color: white;
  box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

#difficultyMenu button:hover {
  background-color: #6c3483;
  transform: scale(1.05);
  box-shadow: 0px 12px 20px rgba(0, 0, 0, 0.4);
}

.mobile-controls {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
}

.mobile-controls button {
  font-size: 24px;
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #8e44ad;
  color: white;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.mobile-controls button:hover {
  background-color: #6c3483;
  transform: scale(1.1);
  box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.4);
}
</style>


