<template>
  <div class="password-regenerate-modal">
    <div class="modal-content">
      <h2>Відновлення пароля</h2>
      <div class="tabs">
        <button
            :class="{ active: activeTab === 'change' }"
            @click="activeTab = 'change'"
        >
          Змінити пароль
        </button>
        <button
            :class="{ active: activeTab === 'recover' }"
            @click="activeTab = 'recover'"
        >
          Відновити пароль
        </button>
      </div>
      <div v-if="activeTab === 'change'" class="tab-content">
        <ChangePassword />
      </div>
      <div v-if="activeTab === 'recover'" class="tab-content">
        <RecoverPassword />
      </div>
      <button @click="close">Закрити</button>
      <p v-if="message" class="message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import ChangePassword from './ChangePassword.vue';
import RecoverPassword from './RecoverPassword.vue';

export default {
  name: 'PasswordRegenerate',
  components: {
    ChangePassword,
    RecoverPassword,
  },
  data() {
    return {
      activeTab: 'change',
      message: '',
    };
  },
  methods: {
    close() {
      this.$emit('close');
    },
  },
};
</script>

<style scoped>
.password-regenerate-modal {
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

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.tabs {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.tabs button {
  flex: 1;
  padding: 10px;
  border: none;
  border-bottom: 2px solid transparent;
  background: none;
  cursor: pointer;
  font-size: 1em;
  transition: border-color 0.3s;
}

.tabs button.active {
  border-bottom: 2px solid #007bff;
  color: #007bff;
}

.tab-content {
  display: flex;
  flex-direction: column;
  align-items: center;
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
</style>
