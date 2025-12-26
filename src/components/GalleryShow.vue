<template>
  <div class="gallery">
    <div v-if="loading" class="loader-container">
      <div class="coffee-cup">
        <img src="coffeboss.png" alt="Coffeboss" class="coffee-image" />
      </div>
    </div>
    <div v-else class="gallery-content">
      <div class="image-container">
        <span v-for="(image, index) in images" :key="image.id" :style="`--i: ${index + 1}`">
          <img :src="getImageSrc(image.id)" :alt="image.image_name" />
        </span>
      </div>
      <div class="btn-container">
        <div class="arrow left" @click="rotateGallery(45)">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
            <path d="M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z"/>
          </svg>
        </div>
        <div class="arrow right" @click="rotateGallery(-45)">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
            <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GalleryShow',
  props: {
    images: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      loading: true,
      rotationAngle: 0,
    };
  },
  methods: {
    getImageSrc(imageId) {
      return `http://localhost:5000/api/get-image/${imageId}`;
    },
    rotateGallery(angle) {
      this.rotationAngle += angle;
      const imageContainer = this.$el.querySelector('.image-container');
      imageContainer.style.transform = `perspective(1000px) rotateY(${this.rotationAngle}deg)`;
    },
  },
  mounted() {
    setTimeout(() => {
      this.loading = false;
    }, 3000);
  },
};
</script>

<style scoped>
.gallery {
  text-align: center;
  margin-top: 20px;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f3f4f7, #e0e7ff);
  border-radius: 12px;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  animation: fadeIn 2s ease-out;
}

h2 {
  color: #3a3a3a;
  margin-bottom: 30px;
  font-size: 2.5em;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  animation: slideIn 1.5s ease-in-out;
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.coffee-cup {
  width: 220px;
  height: 220px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  background-color: #ffffff;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  animation: cupShake 1s infinite alternate;
}

.coffee-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes cupShake {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(5deg);
  }
}

.gallery-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: fadeIn 2s ease-in-out;
}

.image-container {
  position: relative;
  width: 300px;
  height: 300px;
  margin-top: 50px;
  transform-style: preserve-3d;
  transform: perspective(1000px) rotateY(0deg);
  transition: transform 0.7s;
}

.image-container span {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  transform: rotateY(calc(var(--i) * 45deg)) translateZ(400px);
}

.image-container span img {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.image-container span img:hover {
  transform: scale(1.1);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.25);
}

.btn-container {
  position: relative;
  width: 80%;
  margin-top: 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.arrow {
  cursor: pointer;
  padding: 10px;
  background-color: crimson;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
}

.arrow svg {
  fill: white;
  width: 24px;
  height: 24px;
}

.arrow:hover {
  background-color: darkred;
}

.left {
  margin-right: auto;
}

.right {
  margin-left: auto;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideIn {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(0);
  }
}
</style>