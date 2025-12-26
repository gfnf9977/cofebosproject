<template>
  <div class="modal-backdrop">
    <div class="modal-container">
      <h2>Реєстрація</h2>
      <form @submit.prevent="register">
        <div class="form-group">
          <input v-model="registerData.username" @blur="validateField('username')" placeholder="Логін" />
          <p v-if="validationErrors.username" class="error-message">{{ validationErrors.username }}</p>
        </div>

        <div class="form-group password-container">
          <input :type="passwordType" v-model="registerData.password" @input="filterPassword" @blur="validateField('password')" placeholder="Пароль" />
          <button type="button" @click="togglePasswordVisibility" class="toggle-password">
            {{ passwordVisible ? 'Приховати' : 'Показати' }}
          </button>
          <button v-if="showGenerateButton" type="button" @click="generatePassword" class="generate-password">
            Згенерувати
          </button>
          <p v-if="validationErrors.password" class="error-message">{{ validationErrors.password }}</p>
        </div>

        <div class="form-group">
          <input v-model="registerData.last_name" @input="filterName" @blur="validateField('last_name')" placeholder="Прізвище" name="last_name" />
          <p v-if="validationErrors.last_name" class="error-message">{{ validationErrors.last_name }}</p>
        </div>

        <div class="form-group">
          <input v-model="registerData.first_name" @input="filterName" @blur="validateField('first_name')" placeholder="Ім'я" name="first_name" />
          <p v-if="validationErrors.first_name" class="error-message">{{ validationErrors.first_name }}</p>
        </div>

        <div class="form-group">
          <input v-model="registerData.middle_name" @input="filterName" @blur="validateField('middle_name')" placeholder="По-батькові" name="middle_name" />
          <p v-if="validationErrors.middle_name" class="error-message">{{ validationErrors.middle_name }}</p>
        </div>

        <div class="form-group phone-input">
          <select v-model="registerData.country_code" class="country-code">
            <option value="+380">+380 (Україна)</option>
            <option value="+1">+1 (США)</option>
            <option value="+44">+44 (Великобританія)</option>
            <option value="+33">+33 (Франція)</option>
            <option value="+48">+48 (Польща)</option>
            <option value="manual">Ввести вручну</option>
          </select>
          <input v-if="registerData.country_code === 'manual'" v-model="registerData.manual_country_code" @input="filterPhoneNumber" @blur="validateField('manual_country_code')" placeholder="Код країни" class="country-code-input" />
          <input v-model="registerData.phone_number" @input="filterPhoneNumber" @blur="validateField('phone_number')" placeholder="Номер телефону" class="phone-number" />
          <p v-if="validationErrors.phone_number" class="error-message">{{ validationErrors.phone_number }}</p>
        </div>

        <div class="form-group">
          <input v-model="registerData.birth_date" @blur="validateField('birth_date')" type="date" placeholder="Дата народження" />
          <p v-if="validationErrors.birth_date" class="error-message">{{ validationErrors.birth_date }}</p>
        </div>

        <div class="form-group checkbox-container">
          <input type="checkbox" v-model="agreeToTerms" id="agreeToTerms" />
          <label for="agreeToTerms">
            Я погоджуюсь з
            <a href="#" @click.prevent="openTermsModal">правилами надання персональних даних</a>
          </label>
          <p v-if="validationErrors.agreeToTerms" class="error-message">{{ validationErrors.agreeToTerms }}</p>
        </div>

        <div class="form-actions">
          <button type="submit" :disabled="!isFormValid">Зареєструватися</button>
          <button type="button" @click="closeModal">Закрити</button>
        </div>
        <p v-if="message">{{ message }}</p>
      </form>
    </div>
  </div>
  <TermsModal :isVisible="isTermsModalVisible" @close="closeTermsModal" />
  <LoginRegisterError
      :message="errorMessage"
      :transliteratedText="transliteratedText"
      :keyboardTransliteratedText="keyboardTransliteratedText"
      :isVisible="isErrorModalVisible"
      @close="closeErrorModal"
      @apply-selection="applySelection"
  />
</template>

<script>
import axios from 'axios';
import TermsModal from './TermsModal.vue';
import LoginRegisterError from './LoginRegisterError.vue';

export default {
  name: 'UserRegister',
  components: {
    TermsModal,
    LoginRegisterError,
  },
  data() {
    return {
      registerData: {
        username: '',
        password: '',
        last_name: '',
        first_name: '',
        middle_name: '',
        country_code: '+380',
        manual_country_code: '',
        phone_number: '',
        birth_date: '',
      },
      passwordVisible: false,
      message: '',
      agreeToTerms: false,
      isTermsModalVisible: false,
      isErrorModalVisible: false,
      errorMessage: '',
      transliteratedText: '',
      keyboardTransliteratedText: '',
      validationErrors: {
        username: '',
        password: '',
        last_name: '',
        first_name: '',
        middle_name: '',
        phone_number: '',
        birth_date: '',
        agreeToTerms: '',
        manual_country_code: '',
      },
      showGenerateButton: false,
    };
  },
  computed: {
    passwordType() {
      return this.passwordVisible ? 'text' : 'password';
    },
    isFormValid() {
      return (
          this.registerData.username &&
          this.registerData.password &&
          this.registerData.last_name &&
          this.registerData.first_name &&
          this.registerData.middle_name &&
          this.registerData.phone_number &&
          this.registerData.birth_date &&
          this.agreeToTerms &&
          (this.registerData.country_code !== 'manual' || this.registerData.manual_country_code)
      );
    }
  },
  methods: {
    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible;
    },
    filterPhoneNumber(event) {
      this.registerData.phone_number = event.target.value.replace(/\D/g, '');
    },
    filterName(event) {
      if (event.target.name === 'username') return;
      let value = event.target.value;
      value = value.replace(/[^a-zA-Zа-яА-ЯіІїЇєЄ\s]/g, '');
      value = value.charAt(0).toUpperCase() + value.slice(1).toLowerCase();
      event.target.value = value;
      this.registerData[event.target.name] = value;
    },
    filterPassword(event) {
      let value = event.target.value;
      value = value.replace(/[^a-zA-Z0-9]/g, ''); // Allow only English letters and numbers
      event.target.value = value;
      this.registerData.password = value;
    },
    validateField(field) {
      if (!this.registerData[field]) {
        this.validationErrors[field] = 'Це поле не може бути порожнім';
      } else if (field === 'username') {
        const usernameRegex = /^[a-zA-Z0-9!@#$%^&*()_+-=[\]{};':"|,.<>/?]+$/;
        if (!usernameRegex.test(this.registerData[field])) {
          this.validationErrors[field] = 'Логін має містити лише англійські літери, цифри та спеціальні символи';
          this.errorMessage = this.validationErrors[field];
          this.transliteratedText = this.transliterate(this.registerData[field]);
          this.keyboardTransliteratedText = this.keyboardTransliterate(this.registerData[field]);
          this.isErrorModalVisible = true;
        } else {
          this.validationErrors[field] = '';
        }
      } else if (field === 'password') {
        const passwordRegex = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
        if (!passwordRegex.test(this.registerData[field])) {
          this.validationErrors[field] = 'Пароль має містити не менше 8 символів, включаючи принаймні одну велику літеру та одну цифру';
          this.showGenerateButton = true;
        } else {
          this.validationErrors[field] = '';
          this.showGenerateButton = false;
        }
      } else if (field === 'birth_date') {
        const birthDate = new Date(this.registerData[field]);
        const minDate = new Date('1900-01-01');
        const maxDate = new Date('2020-12-31');
        if (birthDate < minDate || birthDate > maxDate) {
          this.validationErrors[field] = 'Некоректна дата народження';
        } else {
          this.validationErrors[field] = '';
        }
      } else if (field === 'manual_country_code') {
        const manualCountryCodeRegex = /^\+\d+$/;
        if (!manualCountryCodeRegex.test(this.registerData[field])) {
          this.validationErrors[field] = 'Некоректний код країни';
        } else {
          this.validationErrors[field] = '';
        }
      } else {
        this.validationErrors[field] = '';
      }
    },
    generatePassword() {
      const length = 12;
      const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
      let result = '';
      for (let i = 0; i < length; i++) {
        result += charset.charAt(Math.floor(Math.random() * charset.length));
      }
      this.registerData.password = result;
      this.validateField('password');
    },
    transliterate(text) {
      const transliterationMap = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'є': 'ye',
        'ж': 'zh',
        'з': 'z',
        'и': 'i',
        'і': 'i',
        'ї': 'yi',
        'й': 'y',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'kh',
        'ц': 'ts',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'shch',
        'ю': 'yu',
        'я': 'ya',
        'А': 'A',
        'Б': 'B',
        'В': 'V',
        'Г': 'G',
        'Д': 'D',
        'Е': 'E',
        'Є': 'Ye',
        'Ж': 'Zh',
        'З': 'Z',
        'И': 'I',
        'І': 'I',
        'Ї': 'Yi',
        'Й': 'Y',
        'К': 'K',
        'Л': 'L',
        'М': 'M',
        'Н': 'N',
        'О': 'O',
        'П': 'P',
        'Р': 'R',
        'С': 'S',
        'Т': 'T',
        'У': 'U',
        'Ф': 'F',
        'Х': 'Kh',
        'Ц': 'Ts',
        'Ч': 'Ch',
        'Ш': 'Sh',
        'Щ': 'Shch',
        'Ю': 'Yu',
        'Я': 'Ya',
      };
      return text.split('').map(char => transliterationMap[char] || char).join('');
    },
    keyboardTransliterate(text) {
      const keyboardMap = {
        'а': 'f',
        'б': '<',
        'в': 'd',
        'г': 'u',
        'д': 'l',
        'е': 't',
        'є': '',
        'ж': ';',
        'з': 'p',
        'и': 'b',
        'і': 's',
        'ї': ']',
        'й': 'q',
        'к': 'r',
        'л': 'k',
        'м': 'v',
        'н': 'y',
        'о': 'j',
        'п': 'g',
        'р': 'h',
        'с': 'c',
        'т': 'n',
        'у': 'e',
        'ф': 'a',
        'х': '[',
        'ц': 'w',
        'ч': 'x',
        'ш': 'i',
        'щ': 'o',
        'ю': '.',
        'я': 'z',
        'А': 'F',
        'Б': '<',
        'В': 'D',
        'Г': 'U',
        'Д': 'L',
        'Е': 'T',
        'Є': '',
        'Ж': ';',
        'З': 'P',
        'И': 'B',
        'І': 'S',
        'Ї': ']',
        'Й': 'Q',
        'К': 'R',
        'Л': 'K',
        'М': 'V',
        'Н': 'Y',
        'О': 'J',
        'П': 'G',
        'Р': 'H',
        'С': 'C',
        'Т': 'N',
        'У': 'E',
        'Ф': 'A',
        'Х': '[',
        'Ц': 'W',
        'Ч': 'X',
        'Ш': 'I',
        'Щ': 'O',
        'Ю': '.',
        'Я': 'Z',
      };
      return text.split('').map(char => keyboardMap[char] || char).join('');
    },
    applySelection(option) {
      if (option === 'transliterated') {
        this.registerData.username = this.transliteratedText;
      } else if (option === 'keyboardTransliterated') {
        this.registerData.username = this.keyboardTransliteratedText;
      }
      // Clear the validation error for the username field
      this.validationErrors.username = '';
    },
    async register() {
      // Перевірка всіх полів перед відправкою
      for (const field in this.registerData) {
        if (!this.registerData[field] && field !== 'manual_country_code') {
          this.validationErrors[field] = 'Це поле не може бути порожнім';
          return;
        }
      }

      // Додаткова перевірка для дати народження
      const birthDate = new Date(this.registerData.birth_date);
      const minDate = new Date('1900-01-01');
      const maxDate = new Date('2020-12-31');
      if (birthDate < minDate || birthDate > maxDate) {
        this.validationErrors.birth_date = 'Некоректна дата народження';
        return;
      }

      // Перевірка, чи користувач погодився з правилами
      if (!this.agreeToTerms) {
        this.validationErrors.agreeToTerms = 'Ви повинні погодитися з правилами надання персональних даних';
        return;
      }

      // Перевірка коду країни, якщо введено вручну
      if (this.registerData.country_code === 'manual' && !this.registerData.manual_country_code) {
        this.validationErrors.manual_country_code = 'Це поле не може бути порожнім';
        return;
      }

      try {
        this.registerData.phone_number = (this.registerData.country_code === 'manual' ? this.registerData.manual_country_code : this.registerData.country_code) + this.registerData.phone_number;
        const response = await axios.post('http://localhost:5000/api/register', this.registerData);
        this.message = response.data.message;
        this.$emit('close');
      } catch (error) {
        console.error('Помилка при реєстрації:', error);
        this.message = error.response?.data?.error || 'Сталася помилка при реєстрації.';
      }
    },
    closeModal() {
      this.$emit('close');
    },
    openTermsModal() {
      this.isTermsModalVisible = true;
    },
    closeTermsModal() {
      this.isTermsModalVisible = false;
    },
    closeErrorModal() {
      this.isErrorModalVisible = false;
      this.errorMessage = '';
      this.transliteratedText = '';
      this.keyboardTransliteratedText = '';
    }
  }
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-container {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  width: 95%;
  max-width: 800px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

h2 {
  margin-bottom: 20px;
  font-size: 1.5em;
  color: #343a40;
}

form {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 600px;
  align-items: center;
}

.form-group {
  margin-bottom: 15px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

input, select {
  width: 100%;
  max-width: 400px;
  padding: 12px;
  margin: 5px 0;
  border: 1px solid #ced4da;
  border-radius: 5px;
  font-size: 1em;
  background-color: #e9ecef;
  color: #495057;
}

.password-container {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 400px;
}

.toggle-password, .generate-password {
  background: none;
  border: none;
  cursor: pointer;
  margin-left: 10px;
  color: #6c757d;
  font-size: 1em;
}

.generate-password {
  text-decoration: underline;
}

button {
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  background-color: #343a40;
  color: white;
  cursor: pointer;
  font-size: 1em;
  margin: 5px;
  transition: background-color 0.3s;
  width: 100%;
  max-width: 400px;
}

button:hover {
  background-color: #23272b;
}

button:disabled {
  background-color: #adb5bd;
  cursor: not-allowed;
}

.phone-input {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 400px;
}

.country-code {
  width: 25%;
}

.phone-number {
  width: 70%;
  margin-left: 10px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  margin: 10px 0;
  width: 100%;
  max-width: 400px;
}

.checkbox-container label {
  margin-left: 10px;
  color: #495057;
}

.checkbox-container a {
  color: #6c757d;
  text-decoration: underline;
  cursor: pointer;
}

.error-message {
  color: #dc3545;
  font-size: 0.9em;
  margin-top: -10px;
  margin-bottom: 10px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
  width: 100%;
  max-width: 400px;
}
</style>