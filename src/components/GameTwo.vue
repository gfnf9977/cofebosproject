<template>
  <div class="game-overlay">
    <div class="game-content">
      <button class="close-button" @click="close">&times;</button>
      <!-- Текст видалено -->
      <div
          class="container"
          @mousemove="updateClipPath"
          :style="{
          '--mouse-x': mouseX + 'px',
          '--mouse-y': mouseY + 'px',
          'background-image': 'url(/gametwo.jpg)'
        }"
      ></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GameTwo',
  data() {
    return {
      mouseX: 0,
      mouseY: 0,
    };
  },
  methods: {
    close() {
      this.$emit('close');
    },
    updateClipPath(event) {
      const rect = event.target.getBoundingClientRect();
      this.mouseX = event.clientX - rect.left;
      this.mouseY = event.clientY - rect.top;
    },
  },
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: sans-serif;
}

body {
  background: black;
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
  background: black; /* Фон змінено на чорний */
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  position: relative;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  width: 80%;
  height: 80%;
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

.container {
  position: relative;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  clip-path: circle(100px at var(--mouse-x) var(--mouse-y));
  transition: clip-path 0.05s ease-out;
  cursor: none; /* Приховуємо стандартний курсор */
  background-color: black; /* Чорний фон */
}
</style>