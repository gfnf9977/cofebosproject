<template>
  <div v-if="isVisible" class="error-modal-backdrop">
    <div class="error-modal-container">
      <p class="error-message">{{ message }}</p>
      <div class="transliterated-container" @click="selectOption('transliterated')" :class="{ selected: selectedOption === 'transliterated' }">
        <p>Транслітерований варіант:</p>
        <input type="text" :value="transliteratedText" readonly />
      </div>
      <div class="transliterated-container" @click="selectOption('keyboardTransliterated')" :class="{ selected: selectedOption === 'keyboardTransliterated' }">
        <p>Переклад по клавіатурі:</p>
        <input type="text" :value="keyboardTransliteratedText" readonly />
      </div>
      <div class="button-group">
        <button class="apply-btn" @click="applySelection" :disabled="!selectedOption">Застосувати</button>
        <button class="close-btn" @click="closeModal">Закрити</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginRegisterError',
  props: {
    message: { type: String, required: true },
    transliteratedText: { type: String, required: true },
    keyboardTransliteratedText: { type: String, required: true },
    isVisible: { type: Boolean, required: true },
  },
  data() {
    return { selectedOption: '' };
  },
  methods: {
    selectOption(option) {
      this.selectedOption = option;
    },
    closeModal() {
      this.$emit('close');
    },
    applySelection() {
      if (this.selectedOption) {
        this.$emit('apply-selection', this.selectedOption);
        this.closeModal();
      }
    },
  },
};
</script>

<style scoped>
.error-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  animation: fadeIn 0.3s ease-in-out;
}

.error-modal-container {
  background: white;
  padding: 24px;
  border-radius: 12px;
  text-align: center;
  width: 320px;
  box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
  animation: slideIn 0.3s ease-in-out;
}

.error-message {
  color: #d32f2f;
  font-size: 1.1em;
  font-weight: bold;
  margin-bottom: 16px;
}

.transliterated-container {
  margin-bottom: 16px;
  padding: 10px;
  border: 2px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s ease-in-out;
}

.transliterated-container p {
  font-weight: 500;
  margin-bottom: 6px;
}

.transliterated-container input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: #f7f7f7;
}

.transliterated-container:hover {
  background-color: #f0f0f0;
}

.selected {
  border-color: #007bff;
  background-color: #e6f0ff;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 16px;
}

button {
  padding: 10px 18px;
  border: none;
  border-radius: 6px;
  font-size: 0.95em;
  font-weight: bold;
  cursor: pointer;
  transition: 0.2s ease-in-out;
}

.apply-btn {
  background-color: #007bff;
  color: white;
}

.apply-btn:disabled {
  background-color: #b0c4de;
  cursor: not-allowed;
}

.apply-btn:hover:not(:disabled) {
  background-color: #0056b3;
}

.close-btn {
  background-color: #6c757d;
  color: white;
}

.close-btn:hover {
  background-color: #5a6268;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from { transform: translateY(-20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
