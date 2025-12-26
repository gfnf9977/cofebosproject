<template>
  <div v-if="isVisible" class="modal-backdrop">
    <div class="modal-container">
      <h2>Умови надання персональних даних</h2>
      <p>
        Ці умови регулюють збір, використання та захист ваших персональних даних. Продовжуючи використовувати наш сервіс, ви погоджуєтеся з цими умовами.
      </p>
      <p>
        <strong>Збір даних:</strong> Ми збираємо ваші персональні дані, такі як ім'я, прізвище, номер телефону та дата народження, для надання наших послуг.
      </p>
      <p>
        <strong>Використання даних:</strong> Ваші персональні дані використовуються для надання послуг, покращення досвіду користування та зв'язку з вами.
      </p>
      <p>
        <strong>Захист даних:</strong> Ми вживаємо заходів для захисту ваших персональних даних від несанкціонованого доступу, втрати та зловживання.
      </p>
      <p>
        <strong>Права користувача:</strong> Ви маєте право на доступ до ваших персональних даних, їх виправлення та видалення.
      </p>
      <p>
        <strong>Зміни умов:</strong> Ми можемо оновлювати ці умови час від часу. Будь ласка, перевіряйте їх регулярно.
      </p>
      <button @click="closeModal">Закрити</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TermsModal',
  props: {
    isVisible: Boolean,
  },
  methods: {
    closeModal() {
      this.$emit('close');
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
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-container {
  background: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
  width: 600px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  margin: 5px;
}

button:hover {
  background-color: #0056b3;
}
</style>
