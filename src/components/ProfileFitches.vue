<template>
  <div class="wrapper">
    <!-- Loading Animation -->
    <div v-if="isLoading" class="loader-container">
      <span class="loader"></span>
    </div>

    <!-- Profile Content -->
    <div v-else class="profile-content">
      <div class="info">
        <div id="name">{{ localUsername }}</div>
        <hr class="horizon" />
        <div class="info-item">
          <label for="firstname">Ім'я:</label>
          <input
              v-if="isEditing"
              type="text"
              id="firstname"
              v-model="firstname"
          />
          <span v-else id="first">{{ firstname }}</span>
        </div>
        <div class="info-item">
          <label for="middlename">По батькові:</label>
          <input
              v-if="isEditing"
              type="text"
              id="middlename"
              v-model="middlename"
          />
          <span v-else id="middlename">{{ middlename }}</span>
        </div>
        <div class="info-item">
          <label for="lastname">Прізвище:</label>
          <input
              v-if="isEditing"
              type="text"
              id="lastname"
              v-model="lastname"
          />
          <span v-else id="last">{{ lastname }}</span>
        </div>
        <div class="info-item">
          <label for="phone">Телефон:</label>
          <input
              v-if="isEditing"
              type="text"
              id="phone"
              v-model="phone"
          />
          <span v-else id="phone">{{ phone }}</span>
        </div>
        <div class="info-item" v-if="isEditing">
          <label for="avatar">Аватар:</label>
          <input
              type="file"
              id="avatar"
              @change="uploadAvatar"
          />
        </div>
      </div>
      <div class="img-area">
        <div class="inner-area" @click="openGIFChoose">
          <img v-if="avatarUrl" :src="avatarUrl" alt="Avatar" id="photo" />
        </div>
      </div>
      <button id="btn" @click="toggleEditing">{{ isEditing ? 'Зберегти' : 'Редагувати' }}</button>
    </div>

    <!-- GIF Choose Modal -->
    <GIFChoose v-if="showGIFChoose" @close="closeGIFChoose" />
  </div>
</template>

<script>
import GIFChoose from './GIFChoose.vue';

export default {
  name: 'ProfileEdit',
  components: {
    GIFChoose
  },
  props: {
    username: String // Приймаємо username як пропс
  },
  data() {
    return {
      localUsername: this.username, // Локальна змінна, що містить значення username
      firstname: '', // Ім'я користувача
      middlename: '', // По батькові користувача
      lastname: '', // Прізвище користувача
      phone: '', // Телефон користувача
      avatarFile: null, // Файл аватара
      avatarUrl: '', // URL аватара
      isEditing: false, // Статус редагування
      isLoading: false, // Статус завантаження
      loading: true, // Added loading state
      showGIFChoose: false // Статус відображення модального вікна
    };
  },
  mounted() {
    this.fetchUserProfile();
    this.fetchAvatar();
    // Simulate loading
    setTimeout(() => {
      this.loading = false;
    }, 3000);
  },
  methods: {
    async fetchUserProfile() {
      try {
        const response = await fetch(`http://localhost:5000/api/user-profile?username=${this.localUsername}`);
        const data = await response.json();

        if (data.username) {
          this.localUsername = data.username;
          this.firstname = data.first_name;
          this.middlename = data.middle_name;
          this.lastname = data.last_name;
          this.phone = data.phone_number;
        }
      } catch (error) {
        console.error('Помилка при отриманні профілю користувача:', error);
      }
    },
    async fetchAvatar() {
      try {
        const userIdResponse = await fetch(`http://localhost:5000/api/user-id?username=${this.localUsername}`);
        const userIdData = await userIdResponse.json();
        const userId = userIdData.id;

        const avatarResponse = await fetch(`http://localhost:5000/api/get-avatar/${userId}`);
        const blob = await avatarResponse.blob();
        this.avatarUrl = URL.createObjectURL(blob);
      } catch (error) {
        console.error('Помилка при отриманні аватара:', error);
      }
    },
    async uploadAvatar(event) {
      const file = event.target.files[0];
      if (file) {
        this.isLoading = true; // Show loader
        const formData = new FormData();
        formData.append('file', file);

        const userIdResponse = await fetch(`http://localhost:5000/api/user-id?username=${this.localUsername}`);
        const userIdData = await userIdResponse.json();
        const userId = userIdData.id;

        const response = await fetch(`http://localhost:5000/api/upload-avatar/${userId}`, {
          method: 'POST',
          body: formData,
        });
        if (response.ok) {
          await this.fetchAvatar();
        } else {
          console.error('Помилка завантаження аватара:', response.statusText);
        }
        this.isLoading = false; // Hide loader
      }
    },
    async toggleEditing() {
      if (this.isEditing) {
        this.isLoading = true; // Show loader
        try {
          const response = await fetch('http://localhost:5000/api/update-profile', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              username: this.localUsername,
              first_name: this.firstname,
              middle_name: this.middlename,
              last_name: this.lastname,
              phone_number: this.phone,
            }),
          });

          const data = await response.json();
          if (!response.ok) {
            alert('Помилка при збереженні профілю: ' + data.error);
          }
        } catch (error) {
          console.error('Помилка при збереженні профілю:', error);
          alert('Сталася помилка при збереженні профілю.');
        } finally {
          this.isLoading = false; // Hide loader
        }
      }
      this.isEditing = !this.isEditing;
    },
    openGIFChoose() {
      this.showGIFChoose = true;
    },
    closeGIFChoose() {
      this.showGIFChoose = false;
    }
  }
};
</script>


<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600;700&display=swap");

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Poppins", sans-serif;
}

body {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ecf0f3;
  min-height: 100vh;
}

.wrapper,
.wrapper .img-area {
  background: #ecf0f3;
  box-shadow: -3px -3px 7px #fff, 3px 3px 5px #ceced1;
}

.wrapper {
  position: relative;
  width: 100%;
  padding: 30px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 15px;
}

.profile-content {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;
  width: 100%;
}

.wrapper .img-area {
  height: 300px;
  width: 300px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 20px;
}

.img-area .inner-area {
  height: calc(100% - 25px);
  width: calc(100% - 25px);
  border-radius: 50%;
}

.inner-area img {
  height: 100%;
  width: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.wrapper #name {
  font-size: 23px;
  font-weight: 500;
  color: #31344b;
  margin: 10px 0 5px 0;
}

.wrapper #btn {
  position: relative;
  width: 150px;
  border: none;
  outline: none;
  padding: 5px;
  color: #31344b;
  font-size: 13px;
  font-weight: 450;
  border-radius: 5px;
  cursor: pointer;
  z-index: 4;
  margin: 10px 0 15px 0;
  background-color: #ecf0f3;
  box-shadow: -3px -3px 7px #fff, 3px 3px 5px #ceced1;
}

.wrapper .horizon {
  width: 100%;
  height: 2px;
  border-width: 0;
  background: #e4e4e4;
  margin: 10px 0 5px 0;
}

.wrapper .info {
  color: #44476a;
  font-size: 14px;
  font-weight: 500;
  color: #31344b;
  text-align: left;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.info .info-item {
  margin-bottom: 20px;
}

.info-item label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.info-item input[type="text"], .info-item input[type="file"] {
  width: 100%;
  padding: 10px;
  margin: 5px 0 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s;
}

.info-item input[type="text"]:focus, .info-item input[type="file"]:focus {
  border-color: #007BFF;
  outline: none;
}

.loader {
  position: relative;
  width: 164px;
  height: 164px;
  perspective: 300px;
}
.loader::before  {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  left: 0;
  top: 0;
  background-image:
      radial-gradient(circle 15px, #FF3D00 100%, transparent 0),
      radial-gradient(circle 15px, #FF3D00 100%, transparent 0),
      linear-gradient(#FF3D00 100px, transparent 0),
      linear-gradient(#FF3D00 100px, transparent 0);
  background-repeat: no-repeat;
  background-size: 30px 30px, 30px 30px, 40% 2px, 40% 2px;
  background-position: left center, right center, left center, right center;
  animation: rotateY 1s linear infinite;
}
.loader::after  {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  left: 0;
  top: 0;
  background-image:
      radial-gradient(circle 15px, #fff 100%, transparent 0),
      radial-gradient(circle 15px, #fff 100%, transparent 0),
      linear-gradient(#fff 100px, transparent 0),
      linear-gradient(#fff 100px, transparent 0);
  background-repeat: no-repeat;
  background-size: 30px 30px, 30px 30px, 2px 40% , 2px 40%;
  background-position: top center, bottom center, top center, bottom center;
  animation: rotateX 1s linear infinite;
}

@keyframes rotateY {
  0%{ transform: rotateY(0deg)}
  100% { transform: rotateY(-180deg)}
}
@keyframes rotateX {
  0%, 25% { transform: rotateX(0deg)}
  75%,  100% { transform: rotateX(-180deg)}
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.coffee-cup {
  width: 200px;
  height: 200px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
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
</style>