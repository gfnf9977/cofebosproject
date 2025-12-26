<template>
  <div class="home-page">
    <h2>Головна</h2>
    <p class="welcome-text">Ласкаво просимо, {{ username }}!</p>
    <p class="info-text">Тут ви можете переглянути ваші завдання та інформацію про вашу роботу.</p>

    <div class="tasks">
      <h3>Ваші завдання на сьогодні</h3>
      <ul>
        <li>Приготувати каву для клієнтів</li>
        <li>Підтримувати чистоту в закладі</li>
        <li>Обслуговувати клієнтів</li>
      </ul>
    </div>

    <div class="actions">
      <button class="action-btn">Переглянути графік роботи</button>
      <button class="action-btn">Переглянути меню</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      username: '', // Змінна для зберігання імені користувача
    };
  },
  mounted() {
    // Отримуємо ім'я користувача після завантаження компонента
    const username = localStorage.getItem('username');
    if (username) {
      this.username = username;
    }
  },
};
</script>

<style scoped>
.home-page {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 900px;
  margin: 0 auto;
}

h2 {
  color: #333;
  font-size: 2rem;
  margin-bottom: 15px;
}

.welcome-text {
  font-size: 1.5rem;
  font-weight: bold;
  color: #4CAF50;
  margin-bottom: 10px;
}

.info-text {
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 30px;
}

.tasks {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.tasks h3 {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 10px;
}

.tasks ul {
  list-style-type: none;
  padding: 0;
}

.tasks li {
  font-size: 1rem;
  color: #555;
  margin-bottom: 5px;
}

.actions {
  display: flex;
  justify-content: space-around;
}

.action-btn {
  background-color: #007bff;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.action-btn:hover {
  background-color: #0056b3;
}
</style>