<template>
  <div class="points-games-overlay">
    <div class="points-games-content">
      <button class="close-button" @click="close">&times;</button>
      <h2>Міні-ігри</h2>
      <p>Тут ви можете грати в різні міні-ігри та заробляти бали.</p>
      <button class="game-button" @click="openGameOne">Грати в Гру 1</button>
      <button class="game-button" @click="openGameTwo">Грати в Гру 2</button>
      <button class="game-button" @click="openGameThree">Грати в Гру 3</button>
      <GameOne v-if="showGameOne" @close="closeGameOne" />
      <GameTwo v-if="showGameTwo" @close="closeGameTwo" />
      <GameThree v-if="showGameThree" @close="closeGameThree" />
    </div>
  </div>
</template>

<script>
import GameOne from './GameOne.vue';
import GameTwo from './GameTwo.vue';
import GameThree from './GameThree.vue';

export default {
  name: 'PointsGames',
  components: {GameOne, GameTwo, GameThree},
  data() {
    return {
      showGameOne: false,
      showGameTwo: false,
      showGameThree: false,
    };
  },
  methods: {
    close() {
      this.$emit('close');
    },
    openGameOne() {
      this.showGameOne = true;
    },
    closeGameOne() {
      this.showGameOne = false;
    },
    openGameTwo() {
      this.showGameTwo = true;
    },
    closeGameTwo() {
      this.showGameTwo = false;
    },
    openGameThree() {
      this.showGameThree = true;
    },
    closeGameThree() {
      this.showGameThree = false;
    },
  },
};
</script>

<style scoped>
.points-games-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(8px);
}

.points-games-content {
  background: linear-gradient(135deg, #ffffff, #e3eaf4);
  padding: 30px;
  border-radius: 16px;
  text-align: center;
  position: relative;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.25);
  width: 420px;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.close-button {
  position: absolute;
  top: 12px;
  right: 12px;
  background: none;
  border: none;
  font-size: 22px;
  color: #444;
  cursor: pointer;
  transition: color 0.3s;
}

.close-button:hover {
  color: #d9534f;
}

h2 {
  margin-top: 0;
  font-size: 26px;
  font-weight: bold;
  color: #222;
}

p {
  font-size: 18px;
  color: #555;
}

.game-button {
  margin-top: 20px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.game-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.game-button:active {
  transform: translateY(0);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}
</style>