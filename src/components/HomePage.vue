<template>
  <div class="home-page">
    <h2>Головна</h2>
    <p class="welcome-text">Ласкаво просимо, старший адмін!!</p>
    <p class="info-text">Тут ви можете керувати всім, що стосується системи.</p>

    <div v-if="loading" class="loader-container">
      <div class="loader"></div>
    </div>
    <div v-else class="stats">
      <div class="stat-card">
        <h3>Кількість працівників</h3>
        <p>{{ adminsCount }}</p>
      </div>
      <div class="stat-card">
        <h3>Кількість закладів</h3>
        <p>{{ shopsCount }}</p>
      </div>
      <div class="stat-card">
        <h3>Кількість користувачів</h3>
        <p>{{ usersCount }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      adminsCount: 0,
      usersCount: 0,
      shopsCount: 0,
      loading: true, // Add loading state
    };
  },
  async mounted() {
    this.loading = true; // Start loading
    try {
      await Promise.all([
        this.fetchAdminsCount(),
        this.fetchUsersCount(),
        this.fetchShopsCount(),
      ]);
    } catch (error) {
      console.error('Помилка при отриманні даних:', error);
    } finally {
      this.loading = false; // Stop loading
    }
  },
  methods: {
    async fetchAdminsCount() {
      try {
        const response = await fetch('http://localhost:5000/api/admins-count');
        const data = await response.json();
        if (data.admins_count !== undefined) {
          this.adminsCount = data.admins_count;
        }
      } catch (error) {
        console.error('Помилка при отриманні кількості адмінів:', error);
      }
    },
    async fetchUsersCount() {
      try {
        const response = await fetch('http://localhost:5000/api/users-count');
        const data = await response.json();
        if (data.users_count !== undefined) {
          this.usersCount = data.users_count;
        }
      } catch (error) {
        console.error('Помилка при отриманні кількості користувачів:', error);
      }
    },
    async fetchShopsCount() {
      try {
        const response = await fetch('http://localhost:5000/api/shops-count');
        const data = await response.json();
        if (data.shops_count !== undefined) {
          this.shopsCount = data.shops_count;
        }
      } catch (error) {
        console.error('Помилка при отриманні кількості кав\'ярень:', error);
      }
    },
  },
};
</script>

<style scoped>
.home-page {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 900px;
  margin: 0 auto;
  font-family: 'Arial', sans-serif;
  text-align: center;
}

h2 {
  color: #333;
  font-size: 2.2rem;
  margin-bottom: 20px;
}

.welcome-text {
  font-size: 1.6rem;
  font-weight: bold;
  color: #4CAF50;
  margin-bottom: 15px;
}

.info-text {
  font-size: 1.3rem;
  color: #555;
  margin-bottom: 30px;
}

.stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.stat-card {
  background-color: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: calc(33.333% - 20px);
  margin-bottom: 20px;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-card h3 {
  font-size: 1.4rem;
  color: #333;
  margin-bottom: 10px;
}

.stat-card p {
  font-size: 1.8rem;
  font-weight: bold;
  color: #007bff;
}

@media (max-width: 768px) {
  .stat-card {
    width: calc(50% - 20px);
  }
}

@media (max-width: 480px) {
  .stat-card {
    width: 100%;
  }
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.loader {
  width: 50px;
  aspect-ratio: 1;
  display: grid;
  background:
      radial-gradient(closest-side at 50% 12.5%,
      #000 96%, #0000) 50% 0/20% 80% repeat-y,
      radial-gradient(closest-side at 12.5% 50%,
      #000 96%, #0000) 0 50%/80% 20% repeat-x;
  animation: l26 1s infinite steps(12);
}

.loader:before,
.loader:after {
  content: "";
  grid-area: 1/1;
  transform: rotate(30deg);
  background:
      radial-gradient(closest-side at 50% 12.5%,
      #000 96%, #0000) 50% 0/20% 80% repeat-y,
      radial-gradient(closest-side at 12.5% 50%,
      #000 96%, #0000) 0 50%/80% 20% repeat-x;
}

.loader:after {
  transform: rotate(60deg);
}

@keyframes l26 {
  100% {
    transform: rotate(1turn);
  }
}
</style>