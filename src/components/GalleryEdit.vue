<template>
  <div class="gallery-edit">
    <h2>Редагування галереї</h2>
    <div v-if="loading" class="loader-container">
      <div class="loader"></div>
    </div>
    <div v-else>
      <div class="gallery">
        <div v-for="image in images" :key="image.id" class="image-item">
          <img :src="getImageSrc(image.id)" :alt="image.image_name" />
          <button @click="deleteImage(image.id)">Видалити</button>
        </div>
      </div>
      <div class="upload-section">
        <input type="file" @change="uploadImage" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "GalleryEdit",
  data() {
    return {
      images: [],
      loading: true, // Loading state
    };
  },
  async mounted() {
    await this.fetchImages();
  },
  methods: {
    async fetchImages() {
      this.loading = true; // Show the loader
      const response = await fetch('http://localhost:5000/api/gallery');
      if (response.ok) {
        this.images = await response.json();
      } else {
        console.error('Помилка завантаження галереї:', response.statusText);
      }
      this.loading = false; // Hide the loader
    },
    async deleteImage(id) {
      this.loading = true; // Show the loader
      const response = await fetch(`http://localhost:5000/api/delete-image/${id}`, {
        method: 'DELETE',
      });
      if (response.ok) {
        this.images = this.images.filter((image) => image.id !== id);
      } else {
        console.error('Помилка видалення зображення:', response.statusText);
      }
      this.loading = false; // Hide the loader
    },
    async uploadImage(event) {
      this.loading = true; // Show the loader
      const file = event.target.files[0];
      if (file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('http://localhost:5000/api/upload-image', {
          method: 'POST',
          body: formData,
        });
        if (response.ok) {
          await this.fetchImages();
        } else {
          console.error('Помилка завантаження зображення:', response.statusText);
        }
      }
      this.loading = false; // Hide the loader
    },
    getImageSrc(imageId) {
      return `http://localhost:5000/api/get-image/${imageId}`;
    },
  },
};
</script>

<style scoped>
.gallery-edit {
  text-align: center;
  position: relative; /* Ensure the loader is positioned relative to this container */
}

.gallery {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
}

.image-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.image-item img {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 10px;
}

.image-item button {
  background: rgba(255, 0, 0, 0.7);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.image-item button:hover {
  background-color: rgba(255, 0, 0, 0.9);
}

.upload-section {
  margin-top: 20px;
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8); /* Semi-transparent background */
}

.loader {
  width: 50px;
  height: 50px;
  border: 5px solid #000;
  border-top: 5px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
