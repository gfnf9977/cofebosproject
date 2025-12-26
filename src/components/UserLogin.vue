<template>
  <div class="ring-container">
    <div class="ring">
      <i style="--clr:#00ff0a;"></i>
      <i style="--clr:#ff0057;"></i>
      <i style="--clr:#fffd44;"></i>
      <div class="login-box">
        <h2>Авторизація</h2>
        <div class="inputBx">
          <input v-model="username" placeholder="Введіть логін користувача" />
        </div>
        <div class="inputBx password-container">
          <input :type="passwordType" v-model="password" placeholder="Введіть пароль" />
          <button @click="togglePasswordVisibility" class="toggle-password">
            <span v-if="passwordVisible" class="icon">👁️</span>
            <span v-else class="icon">🙈</span>
          </button>
        </div>
        <div class="inputBx">
          <button class="login-button" @click="login">Увійти</button>
        </div>
        <p v-if="message" class="message">{{ message }}</p>
        <div class="links">
          <a @click="showRegisterModal = true"> ----Зареєструватися в мережі---- </a>

          <a @click="showPasswordRegenerateModal = true">Забули пароль чи хочете його змінити?</a>
        </div>
      </div>
    </div>
    <UserRegister v-if="showRegisterModal" @close="showRegisterModal = false" />
    <PasswordRegenerate v-if="showPasswordRegenerateModal" @close="showPasswordRegenerateModal = false" />
  </div>
</template>

<script>
import axios from 'axios';
import UserRegister from './UserRegister.vue';
import PasswordRegenerate from './PasswordRegenerate.vue';

export default {
  name: 'UserLogin',
  components: { UserRegister, PasswordRegenerate },
  data() {
    return {
      username: '',
      password: '',
      message: '',
      showRegisterModal: false,
      showPasswordRegenerateModal: false,
      passwordVisible: false,
    };
  },
  computed: {
    passwordType() {
      return this.passwordVisible ? 'text' : 'password';
    },
  },
  methods: {
    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible;
    },
    async login() {
      try {
        const response = await axios.post('http://localhost:5000/api/check-login', {
          username: this.username,
          password: this.password,
        });

        if (response.data.exists !== false) {
          localStorage.setItem('userStatus', response.data.status);
          localStorage.setItem('username', this.username);
          this.$emit('login-success', response.data.status);
        } else {
          this.message = response.data.message;
        }
      } catch (error) {
        console.error('Помилка при авторизації:', error);
        this.message = 'Сталася помилка при авторизації.';
      }
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Quicksand:wght@300&display=swap");
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Quicksand", sans-serif;
}
.ring-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #111;
}
.ring {
  position: relative;
  width: 500px;
  height: 500px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.ring i {
  position: absolute;
  inset: 0;
  border: 2px solid #fff;
  transition: 0.5s;
}
.ring i:nth-child(1) {
  border-radius: 38% 62% 63% 37% / 41% 44% 56% 59%;
  animation: animate 6s linear infinite;
}
.ring i:nth-child(2) {
  border-radius: 41% 44% 56% 59%/38% 62% 63% 37%;
  animation: animate 4s linear infinite;
}
.ring i:nth-child(3) {
  border-radius: 41% 44% 56% 59%/38% 62% 63% 37%;
  animation: animate2 10s linear infinite;
}
.ring:hover i {
  border: 6px solid var(--clr);
  filter: drop-shadow(0 0 20px var(--clr));
}
@keyframes animate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
@keyframes animate2 {
  0% {
    transform: rotate(360deg);
  }
  100% {
    transform: rotate(0deg);
  }
}
.login-box {
  position: absolute;
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  text-align: center;
  color: white;
}
.inputBx input {
  width: 100%;
  padding: 12px 20px;
  background: transparent;
  border: 2px solid #fff;
  border-radius: 40px;
  font-size: 1em;
  color: #fff;
  outline: none;
}
.inputBx input::placeholder {
  color: rgba(255, 255, 255, 0.75);
}
.login-button {
  width: 100%;
  padding: 12px;
  background: linear-gradient(45deg, #ff357a, #fff172);
  border: none;
  border-radius: 40px;
  font-size: 1.1em;
  cursor: pointer;
}
.message {
  color: red;
  font-size: 0.9em;
}
.links a {
  color: #fff;
  text-decoration: none;
  cursor: pointer;
  transition: color 0.3s;
}
.links a:hover {
  color: #ff357a;
}
.toggle-password {
  background: none;
  border: none;
  cursor: pointer;
  color: #fff;
  font-size: 1.2em;
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
}
</style>
