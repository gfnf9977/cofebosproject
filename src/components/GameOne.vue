<template>
  <div class="game-overlay">
    <div class="game-content">
      <button class="close-button" @click="close">&times;</button>
      <h2>Злови його та отримай свої бали</h2>
      <div class="scores-container">
        <div class="total-score">
          <h2>Your Score:</h2>
          <h2 id="score">{{ score }}</h2>
        </div>
        <div class="time">
          <h2>Time left:</h2>
          <h2 id="time-left">{{ timeLeft }}</h2>
        </div>
      </div>
      <div class="grid-container">
        <div class="grid">
          <div
              v-for="index in 10"
              :key="index"
              :class="['square', { emoji: index === hitPosition }]"
              @mousedown="checkHit(index)"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GameOne',
  data() {
    return {
      score: 0,
      hitPosition: null,
      timeLeft: 60,
      timerId: null,
      countDownTimerId: null,
    };
  },
  methods: {
    close() {
      this.$emit('close');
      this.resetGame();
    },
    randomSquare() {
      this.hitPosition = Math.floor(Math.random() * 10) + 1;
    },
    checkHit(index) {
      if (index === this.hitPosition) {
        this.score++;
        this.hitPosition = null;
      }
    },
    moveEmoji() {
      this.timerId = setInterval(this.randomSquare, 500);
    },
    countDown() {
      this.timeLeft--;
      if (this.timeLeft === 0) {
        clearInterval(this.countDownTimerId);
        clearInterval(this.timerId);
        alert(`Game Over! Your final Score Is ${this.score}`);
        this.resetGame();
      }
    },
    resetGame() {
      this.score = 0;
      this.timeLeft = 60;
      this.hitPosition = null;
      clearInterval(this.timerId);
      clearInterval(this.countDownTimerId);
    },
  },
  mounted() {
    this.moveEmoji();
    this.countDownTimerId = setInterval(this.countDown, 1000);
  },
  beforeUnmount() {
    this.resetGame();
  },
};
</script>

<style scoped>
body {
  background: rgb(10, 10, 10);
  color: #fff;
  font-family: sans-serif;
}

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
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  position: relative;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  width: 80%;
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

.scores-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.total-score,
.time {
  margin: 20px;
  text-align: center;
  background: #ccc;
  padding: 20px;
  color: #000;
}

.grid-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.grid {
  width: 90%;
  height: 90%;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  background-color: rgb(36, 36, 36);
  margin-top: 2rem;
  padding: 20px;
}

.square {
  height: 100px;
  width: 100px;
  margin: 10px;
  background: rgb(61, 61, 61);
}

.square.emoji {
  background-image: url("https://i.guim.co.uk/img/media/a1b7129c950433c9919f5670c92ef83aa1c682d9/55_344_1971_1183/master/1971.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=88ba2531f114b9b58b9cb2d8e723abe1");
  background-position: center;
  background-size: cover;
}
</style>
