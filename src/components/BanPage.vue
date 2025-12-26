<template>
  <div class="ban-page">
    <div class="ban-container">
      <span class="icon">🔒</span>
      <h2>Ваш аккаунт заблоковано</h2>
      <p>
        Вибачте, але ваш аккаунт було заблоковано. <br />
        Будь ласка, зв'яжіться нашими співробітниками для отримання додаткової інформації.
      </p>
      <button @click="goBack">На головну</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "BanPage",
  methods: {
    goBack() {
      this.$emit('go-back'); // Emit the event
    },
  },
};
</script>

<style scoped>
.ban-page {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: radial-gradient(circle, #e0e0e0, #c0c0c0);
  text-align: center;
  padding: 20px;
}

.ban-container {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 100%;
  animation: fadeIn 0.5s ease-in-out;
}

.icon {
  font-size: 50px;
  color: #ff3b3b;
  margin-bottom: 10px;
  display: block;
}

h2 {
  color: #333;
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 15px;
}

p {
  color: #555;
  font-size: 16px;
  line-height: 1.5;
  margin-bottom: 25px;
}

button {
  background: linear-gradient(135deg, #ff3b3b, #d32f2f);
  color: white;
  border: none;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 6px;
  transition: 0.3s;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
}

button:hover {
  background: linear-gradient(135deg, #d32f2f, #b71c1c);
  transform: translateY(-2px);
}

/* Анімація появи */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
