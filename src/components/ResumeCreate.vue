<template>
  <div class="modal-backdrop">
    <div class="modal">
      <h3>Відгукнутися на вакансію</h3>
      <form @submit.prevent="submitFeedback">
        <div>
          <label for="lastName">Прізвище:</label>
          <input type="text" id="lastName" v-model="feedback.lastName" required>
        </div>
        <div>
          <label for="firstName">Ім'я:</label>
          <input type="text" id="firstName" v-model="feedback.firstName" required>
        </div>
        <div>
          <label for="middleName">По батькові:</label>
          <input type="text" id="middleName" v-model="feedback.middleName" required>
        </div>
        <div>
          <label for="phone">Телефон:</label>
          <input type="tel" id="phone" v-model="feedback.phone" required>
        </div>
        <div>
          <label for="contactMethod">Спосіб зв'язку:</label>
          <div class="custom-select" @click="toggleDropdown">
            <div class="selected-option">
              <img v-if="selectedIcon" :src="selectedIcon" alt="">
              <span>{{ selectedLabel }}</span>
            </div>
            <div class="dropdown-content" v-if="isDropdownOpen">
              <div class="dropdown-item" @click="selectOption('viber')">
                <img src="viber.png" alt="Viber">
                <span>Viber</span>
              </div>
              <div class="dropdown-item" @click="selectOption('telegram')">
                <img src="telegram.png" alt="Telegram">
                <span>Telegram</span>
              </div>
              <div class="dropdown-item" @click="selectOption('whatsapp')">
                <img src="whatsapp.png" alt="WhatsApp">
                <span>WhatsApp</span>
              </div>
              <div class="dropdown-item" @click="selectOption('instagram')">
                <img src="instagram.png" alt="Instagram">
                <span>Instagram</span>
              </div>
              <div class="dropdown-item" @click="selectOption('email')">
                <img src="gmail.png" alt="E-mail">
                <span>E-mail</span>
              </div>
            </div>
          </div>
        </div>
        <div v-if="feedback.contactMethod">
          <label :for="feedback.contactMethod">{{ contactMethodLabel }}:</label>
          <input :type="contactMethodType" :id="feedback.contactMethod" v-model="feedback.contactDetail" :readonly="isContactDetailReadOnly" required>
        </div>
        <div>
          <label for="residence">Чи мешкаєте в Чернігові?</label>
          <select id="residence" v-model="feedback.residence" required>
            <option value="">Оберіть відповідь</option>
            <option value="yes">Так</option>
            <option value="no">Ні</option>
          </select>
        </div>
        <div>
          <label for="experience">Попередній досвід:</label>
          <textarea id="experience" v-model="feedback.experience" required></textarea>
        </div>
        <div>
          <label for="about">Коротко про себе:</label>
          <textarea id="about" v-model="feedback.about" required></textarea>
        </div>
        <div>
          <label for="whyCoffeBoss">Чому саме CoffeBoss?</label>
          <textarea id="whyCoffeBoss" v-model="feedback.whyCoffeBoss" required></textarea>
        </div>
        <button type="submit">Надіслати</button>
        <button type="button" @click="closeModal">Закрити</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResumeCreate',
  props: {
    userId: {
      type: Number,
      required: true,
    },
    firstName: {
      type: String,
      required: true,
    },
    middleName: {
      type: String,
      required: true,
    },
    lastName: {
      type: String,
      required: true,
    },
    phone: {
      type: String,
      required: true,
    },
    vacancyId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      feedback: {
        userId: this.userId,
        vacancyId: this.vacancyId,
        firstName: this.firstName,
        middleName: this.middleName,
        lastName: this.lastName,
        phone: this.phone,
        contactMethod: '',
        contactDetail: '',
        residence: '',
        experience: '',
        about: '',
        whyCoffeBoss: '',
      },
      isDropdownOpen: false,
      selectedIcon: '',
      selectedLabel: 'Оберіть спосіб зв\'язку',
    };
  },
  computed: {
    contactMethodLabel() {
      const labels = {
        viber: 'Viber',
        telegram: 'Telegram',
        whatsapp: 'WhatsApp',
        instagram: 'Instagram',
        email: 'E-mail',
      };
      return `${labels[this.feedback.contactMethod]} (${this.feedback.contactDetail})`;
    },
    contactMethodType() {
      return this.feedback.contactMethod === 'email' ? 'email' : 'text';
    },
    isContactDetailReadOnly() {
      return this.feedback.contactMethod !== 'email' && this.feedback.contactMethod !== 'instagram';
    },
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
    updateContactDetail() {
      if (this.feedback.contactMethod !== 'email' && this.feedback.contactMethod !== 'instagram') {
        this.feedback.contactDetail = this.feedback.phone;
      } else {
        this.feedback.contactDetail = '';
      }
    },
    async submitFeedback() {
      try {
        const response = await fetch('http://localhost:5000/api/feedback', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.feedback),
        });
        if (response.ok) {
          alert('Feedback submitted successfully');
          this.closeModal();
        } else {
          console.error('Помилка відправлення відгуку:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка підключення до API:', error);
      }
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    selectOption(method) {
      this.feedback.contactMethod = method;
      this.selectedIcon = `${method}.png`;
      this.selectedLabel = method.charAt(0).toUpperCase() + method.slice(1);
      this.updateContactDetail();
      this.isDropdownOpen = false;
    },
  },
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  padding: 24px 32px;
  border-radius: 16px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  text-align: center;
  max-width: 600px;
  width: 90%;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

h3 {
  margin-bottom: 16px;
  font-size: 1.8em;
  color: #2c3e50;
  font-weight: 700;
}

form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

label {
  margin-bottom: 8px;
  font-weight: 600;
  color: #34495e;
}

input,
select,
textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #bdc3c7;
  border-radius: 8px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  font-size: 1em;
  transition: border-color 0.3s, box-shadow 0.3s;
}

input:focus,
select:focus,
textarea:focus {
  border-color: #3498db;
  box-shadow: 0 0 6px rgba(52, 152, 219, 0.4);
  outline: none;
}

button {
  padding: 14px 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.1em;
  font-weight: 600;
  transition: background-color 0.3s, transform 0.2s;
}

button:hover {
  background-color: #2980b9;
  transform: scale(1.03);
}

button[type="button"] {
  background-color: #95a5a6;
}

button[type="button"]:hover {
  background-color: #7f8c8d;
}

.custom-select {
  position: relative;
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #bdc3c7;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1em;
  color: #34495e;
  background-color: #ecf0f1;
}

.custom-select:focus {
  border-color: #3498db;
}

.selected-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.selected-option img {
  width: 24px;
  height: 24px;
  margin-right: 10px;
}

.dropdown-content {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #bdc3c7;
  border-radius: 8px;
  z-index: 100;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  animation: fadeInDropdown 0.3s ease-out;
}

@keyframes fadeInDropdown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.dropdown-item img {
  width: 24px;
  height: 24px;
  margin-right: 10px;
}

.dropdown-item:hover {
  background-color: #ecf0f1;
}
</style>
