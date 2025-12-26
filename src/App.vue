<template>
  <div id="app">
    <div v-if="!isLoggedIn">
      <UserLogin @login-success="handleLoginSuccess" />
    </div>

    <div v-else>
      <div class="button-container">
        <button @click="logout" class="logout-button">
          <img src="/exit.png" alt="Вийти" class="button-image" />
        </button>
        <button @click="toggleCalculator" class="calculator-button">
          <img src="/calculator.png" alt="Калькулятор купюр" class="button-image" />
        </button>
      </div>
      <PrimeAdminPage v-if="userStatus === 'prime-admin'" />
      <AdminPage v-if="userStatus === 'admin'" />
      <UserPage v-if="userStatus === 'user'" />
      <BanPage v-if="userStatus === 'ban'" @go-back="handleGoBack" />

      <div v-if="showCalculator" class="modal">
        <div class="modal-content">
          <span class="close" @click="toggleCalculator">&times;</span>
          <Calculator />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserLogin from './components/UserLogin.vue';
import PrimeAdminPage from './components/PrimeAdminPage.vue';
import AdminPage from './components/AdminPage.vue';
import UserPage from './components/UserPage.vue';
import BanPage from './components/BanPage.vue';
import Calculator from './components/CalculatorMon.vue';

export default {
  name: 'App',
  components: {
    UserLogin,
    PrimeAdminPage,
    AdminPage,
    UserPage,
    BanPage,
    Calculator
  },
  data() {
    return {
      isLoggedIn: false, 
      userStatus: '',    
      showCalculator: false, 
    };
  },
  created() {
    this.checkLoginStatus();
  },
  methods: {
    handleLoginSuccess(status) {
      this.isLoggedIn = true;
      this.userStatus = status;
      // Зберігаємо статус у localStorage
      localStorage.setItem('userStatus', status);
    },
    checkLoginStatus() {
      const status = localStorage.getItem('userStatus');
      if (status) {
        this.isLoggedIn = true;
        this.userStatus = status;
      }
    },
    logout() {
      this.isLoggedIn = false;
      this.userStatus = '';
      // Очищення localStorage
      localStorage.removeItem('userStatus');
    },
    toggleCalculator() {
      this.showCalculator = !this.showCalculator;
    },
    handleGoBack() {
      this.isLoggedIn = false;
      this.userStatus = '';
      localStorage.removeItem('userStatus');
    }
  }
};
</script>

<style scoped>
.button-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 20px 0;
}

.logout-button, .calculator-button {
  padding: 10px;
  background-color: transparent;
  border: none;
  cursor: pointer;
}

.button-image {
  width: 50px; 
  height: 50px; 
}

.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0, 0, 0);
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 900px;
  border-radius: 5px;
  position: relative;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
</style>