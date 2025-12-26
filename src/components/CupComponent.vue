<template>
  <div>
    <div class="image-container">
      <img src="/play.png" class="btn" @click="openTrailer" />
    </div>
    <button class="order-button" @click="openModal">Замовити</button>
    <div class="trailer-container" :class="{ active: !isTrailerVisible }">
      <video src="/112288.MP4" controls ref="video"></video>
      <p class="close-icon" @click="closeTrailer">X</p>
    </div>
    <CupPay ref="cupPay" @close="closeModal" :userId="userId" />
  </div>
</template>

<script>
import CupPay from './CupPay.vue';

export default {
  name: 'CupComponent',
  components: {
    CupPay,
  },
  props: {
    userId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      isTrailerVisible: false,
    };
  },
  methods: {
    openTrailer() {
      this.isTrailerVisible = true;
      this.$refs.video.play();
    },
    closeTrailer() {
      this.isTrailerVisible = false;
      this.$refs.video.pause();
      this.$refs.video.currentTime = 0;
    },
    openModal() {
      this.$refs.cupPay.openModal();
    },
    closeModal() {
      this.$refs.cupPay.isModalOpen = false;
    },
  },
};
</script>

<style scoped>
.image-container {
  position: relative;
  height: 200px;
  background-position: top;
  background-repeat: no-repeat;
  background-size: cover;
}

.image-container img {
  position: absolute;
  bottom: 20px;
  right: 50px;
  width: 100px;
  cursor: pointer;
  animation-name: bounce;
  animation-duration: 1s;
  animation-timing-function: ease-in;
  animation-iteration-count: infinite;
}

@keyframes bounce {
  0% {
    transform: translateY(0);
    animation-timing-function: ease-out;
  }
  50% {
    transform: translateY(-20px);
    animation-timing-function: ease-in;
  }
  100% {
    transform: translateY(0);
    animation-timing-function: ease-out;
  }
}

.trailer-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #000;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 1;
  transition: opacity 0.7s;
}

.trailer-container.active {
  visibility: hidden;
  opacity: 0;
}

.trailer-container video {
  position: relative;
  max-width: 900px;
  outline: none;
}

.close-icon {
  position: absolute;
  top: 30px;
  right: 30px;
  color: #f26415;
  font-size: 40px;
  cursor: pointer;
  font-family: sans-serif;
  padding: 10px;
  border-radius: 100%;
}

@media (max-width: 991px) {
  .trailer-container video {
    max-width: 90%;
  }
}

.order-button {
  display: block;
  margin-top: 20px;
  margin-left: 20px;
  padding: 10px 20px;
  background: #f26415;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>