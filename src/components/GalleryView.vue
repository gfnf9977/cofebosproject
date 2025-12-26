<template>
  <div class="gallery-view">
    <h2>Галерея</h2>
    <div v-if="loading" class="loader-container">
      <div class="loader"></div>
    </div>
    <div v-else class="gallery">
      <div v-for="image in images" :key="image.id" class="image-item">
        <img :src="getImageSrc(image.id)" :alt="image.image_name" />
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: "GalleryView",
  props: {
    images: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      loading: true,
    };
  },
  methods: {
    getImageSrc(imageId) {
      return `http://localhost:5000/api/get-image/${imageId}`;
    },
  },
  mounted() {
    // Simulate data fetching
    setTimeout(() => {
      this.loading = false;
    }, 2000); // Adjust the timeout as needed
  },
};
</script>

<style scoped>
.gallery-view {
  text-align: center;
  padding: 20px;
  background-color: #f8f9fa;
}

.gallery {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 20px;
}

.image-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: transform 0.3s ease;
}

.image-item img {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.image-item img:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

h2 {
  font-size: 2.5em;
  margin-bottom: 20px;
  color: #333;
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.loader {
  --s: 25px;
  --g: 5px;
  width: calc(2*(1.353*var(--s) + var(--g)));
  aspect-ratio: 1;
  background:
      linear-gradient(#000 0 0) left/50% 100% no-repeat,
      conic-gradient(from -90deg at var(--s) calc(0.353*var(--s)),
      #fff 135deg, #666 0 270deg, #aaa 0);
  background-blend-mode: multiply;
  --_m:
      linear-gradient(to bottom right,
      #0000 calc(0.25*var(--s)), #000 0 calc(100% - calc(0.25*var(--s)) - 1.414*var(--g)), #0000 0),
      conic-gradient(from -90deg at right var(--g) bottom var(--g), #000 90deg, #0000 0);
  -webkit-mask: var(--_m);
  mask: var(--_m);
  background-size: 50% 50%;
  -webkit-mask-size: 50% 50%;
  mask-size: 50% 50%;
  -webkit-mask-composite: source-in;
  mask-composite: intersect;
  animation: l9 1.5s infinite;
}

@keyframes l9 {
  0%, 12.5% { background-position: 0% 0%, 0 0; }
  12.6%, 37.5% { background-position: 100% 0%, 0 0; }
  37.6%, 62.5% { background-position: 100% 100%, 0 0; }
  62.6%, 87.5% { background-position: 0% 100%, 0 0; }
  87.6%, 100% { background-position: 0% 0%, 0 0; }
}
</style>