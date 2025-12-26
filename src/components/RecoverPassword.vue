<template>
  <div class="recover-password-content">
    <input v-model="username" placeholder="Введіть логін користувача" />
    <div class="phone-container">
      <input v-model="phoneNumber" placeholder="Введіть номер телефону" />
    </div>
    <p v-if="validationErrors.phoneNumber" class="error-message">{{ validationErrors.phoneNumber }}</p>
    <button @click="verifyCredentials">Перевірити</button>

    <div v-if="isVerified">
      <div class="password-container">
        <input :type="newPasswordType" v-model="newPassword" @blur="validateField('newPassword')" placeholder="Введіть новий пароль" />
        <button @click="toggleNewPasswordVisibility" class="toggle-password">
          <span v-if="newPasswordVisible" class="icon">👁️</span>
          <span v-else class="icon">🙈</span>
        </button>
      </div>
      <p v-if="validationErrors.newPassword" class="error-message">{{ validationErrors.newPassword }}</p>
      <div class="password-container">
        <input :type="confirmNewPasswordType" v-model="confirmNewPassword" @blur="validateField('confirmNewPassword')" placeholder="Підтвердіть новий пароль" />
        <button @click="toggleConfirmNewPasswordVisibility" class="toggle-password">
          <span v-if="confirmNewPasswordVisible" class="icon">👁️</span>
          <span v-else class="icon">🙈</span>
        </button>
      </div>
      <p v-if="validationErrors.confirmNewPassword" class="error-message">{{ validationErrors.confirmNewPassword }}</p>
      <button @click="changePassword">Змінити пароль</button>
    </div>
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RecoverPassword',
  data() {
    return {
      username: '',
      phoneNumber: '',
      newPassword: '',
      confirmNewPassword: '',
      newPasswordVisible: false,
      confirmNewPasswordVisible: false,
      message: '',
      validationErrors: {
        phoneNumber: '',
        newPassword: '',
        confirmNewPassword: '',
      },
      isVerified: false,
    };
  },
  computed: {
    newPasswordType() {
      return this.newPasswordVisible ? 'text' : 'password';
    },
    confirmNewPasswordType() {
      return this.confirmNewPasswordVisible ? 'text' : 'password';
    },
  },
  methods: {
    toggleNewPasswordVisibility() {
      this.newPasswordVisible = !this.newPasswordVisible;
    },
    toggleConfirmNewPasswordVisibility() {
      this.confirmNewPasswordVisible = !this.confirmNewPasswordVisible;
    },
    validateField(field) {
      if (field === 'newPassword') {
        const passwordRegex = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
        if (!passwordRegex.test(this.newPassword)) {
          this.validationErrors.newPassword = 'Пароль має містити не менше 8 символів, включаючи принаймні одну велику літеру та одну цифру';
        } else {
          this.validationErrors.newPassword = '';
        }
      } else if (field === 'confirmNewPassword') {
        if (this.newPassword !== this.confirmNewPassword) {
          this.validationErrors.confirmNewPassword = 'Новий пароль і його підтвердження не співпадають';
        } else {
          this.validationErrors.confirmNewPassword = '';
        }
      }
    },
    async verifyCredentials() {
      try {
        const response = await axios.post('http://localhost:5000/api/login___check', {
          username: this.username,
          phone_number: this.phoneNumber,
        });

        if (response.data.exists) {
          this.isVerified = true;
          this.message = '';
        } else {
          this.isVerified = false;
          this.message = response.data.message;
        }
      } catch (error) {
        console.error('Помилка при перевірці логіну та номера телефону:', error);
        this.message = 'Сталася помилка при перевірці логіну та номера телефону.';
      }
    },
    async changePassword() {
      // Validate that the new password and confirmation match
      if (this.newPassword !== this.confirmNewPassword) {
        this.validationErrors.confirmNewPassword = 'Новий пароль і його підтвердження не співпадають';
        return;
      }

      try {
        const response = await axios.post('http://localhost:5000/api/recover___password', {
          username: this.username,
          newPassword: this.newPassword,
        });

        if (response.data.success) {
          this.message = 'Пароль успішно змінено.';
        } else {
          this.message = response.data.message;
        }
      } catch (error) {
        console.error('Помилка при зміні пароля:', error);
        this.message = 'Сталася помилка при зміні пароля.';
      }
    },
  },
};
</script>

<style scoped>
.recover-password-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.phone-container, .password-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  position: relative;
}

input {
  width: calc(100% - 40px);
  padding: 12px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 10px;
  font-size: 1em;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #666;
}

.toggle-password {
  background: none;
  border: none;
  cursor: pointer;
  margin-left: 10px;
  font-size: 1.2em;
  color: #666;
  transition: color 0.3s;
}

.toggle-password:hover {
  color: #333;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  margin-top: 10px;
}

button:hover {
  background-color: #0056b3;
}

.message {
  margin-top: 15px;
  color: red;
  font-size: 0.9em;
}

.error-message {
  color: #dc3545;
  font-size: 0.9em;
  margin-top: -10px;
  margin-bottom: 10px;
}
</style>