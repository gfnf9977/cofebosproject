<template>
  <div class="gif-choose-modal">
    <div class="modal-content">
      <h2>Вибір GIF</h2>
      <p>Виберіть GIF з наведених нижче:</p>
      <div class="video-container">
        <div v-for="(video, index) in videos" :key="index" class="video-wrapper">
          <div class="video-circle">
            <video :src="video.src" class="video" controls></video>
          </div>
          <button @click="selectVideo" class="select-button">Обрати</button>
        </div>
      </div>
      <button @click="closeModal" class="close-button">Закрити</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GIFChoose',
  data() {
    return {
      videos: [
        { src: '1111.mp4' },
        { src: '1112.mp4' },
        { src: '1113.mp4' },
        { src: '1114.mp4' },
        { src: '1115.mp4' },
      ],
    };
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
    selectVideo() {
      this.closeModal();
    },
  },
};
</script>

<style scoped>
.gif-choose-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  transition: opacity 0.3s ease;
}

.modal-content {
  background-color: #ffffff;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  text-align: center;
  max-width: 90%;
  width: 700px;
  transition: transform 0.3s ease;
}

.modal-content h2 {
  font-size: 28px;
  margin-bottom: 20px;
  color: #333;
}

.modal-content p {
  font-size: 18px;
  margin-bottom: 30px;
  color: #666;
}

.video-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 30px;
  margin-bottom: 30px;
}

.video-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.video-circle {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f0f0;
  transition: transform 0.4s ease;
}

.video-circle:hover {
  transform: scale(1.6);
}

.video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.select-button {
  padding: 10px 20px;
  background: linear-gradient(90deg, #28a745, #218838);
  color: #fff;
  border: none;
  border-radius: 7px;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.3s ease;
  margin-top: 12px;
}

.select-button:hover {
  background: linear-gradient(90deg, #218838, #1e7e34);
}

.close-button {
  padding: 14px 30px;
  background: linear-gradient(90deg, #007BFF, #0056b3);
  color: #fff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 18px;
  transition: background 0.3s ease;
}

.close-button:hover {
  background: linear-gradient(90deg, #0056b3, #004085);
}
</style>
