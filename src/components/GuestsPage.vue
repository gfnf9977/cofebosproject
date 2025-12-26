<template>
  <div class="guests-page">
    <h2>Гості</h2>
    <input v-model="searchQuery" placeholder="Пошук за прізвищем або логіном" class="search-input" />
    <div v-if="loading" class="loader-container">
      <div class="loader"></div>
    </div>
    <table v-else>
      <thead>
      <tr>
        <th>Прізвище</th>
        <th>Ім'я</th>
        <th>По батькові</th>
        <th>Телефон</th>
        <th>Логін</th>
        <th>Дата народження</th>
        <th>Дії</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="guest in filteredGuests" :key="guest.id">
        <td>{{ guest.last_name }}</td>
        <td>{{ guest.first_name }}</td>
        <td>{{ guest.middle_name }}</td>
        <td>{{ guest.phone_number }}</td>
        <td>{{ guest.username }}</td>
        <td :class="{ 'highlight': isBirthdayToday(guest.birth_date) }">{{ formatDate(guest.birth_date) }}</td>
        <td>
          <button class="admin-btn" @click="setAdminStatus(guest.id)">Взяти на роботу</button>
          <button class="ban-btn" @click="setBanStatus(guest.id)">Заблокувати</button>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'GuestsPage',
  data() {
    return {
      guests: [], // Дані для гостей
      searchQuery: '', // Поле для пошуку
      loading: true // Loading state
    };
  },
  async mounted() {
    try {
      const response = await fetch('http://localhost:5000/api/guests'); // Змініть URL за потреби
      if (response.ok) {
        this.guests = await response.json();
      } else {
        console.error('Помилка завантаження даних:', response.statusText);
      }
    } catch (error) {
      console.error('Помилка підключення до API:', error);
    } finally {
      this.loading = false; // Hide the loader
    }
  },
  computed: {
    filteredGuests() {
      if (!this.searchQuery) {
        return this.guests;
      }
      return this.guests.filter(guest =>
          guest.last_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          guest.username.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return 'Невідомо';
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString('uk-UA', options);
    },
    async setAdminStatus(userId) {
      try {
        const response = await fetch(`http://localhost:5000/api/set-admin/${userId}`, {
          method: 'POST',
        });
        if (response.ok) {
          alert('Status set to admin successfully');
          // Optionally, refresh the guest list
          this.guests = this.guests.filter(guest => guest.id !== userId);
        } else {
          console.error('Помилка встановлення статусу:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка підключення до API:', error);
      }
    },
    async setBanStatus(userId) {
      try {
        const response = await fetch(`http://localhost:5000/api/set-ban/${userId}`, {
          method: 'POST',
        });
        if (response.ok) {
          alert('Status set to ban successfully');
          // Optionally, refresh the guest list
          this.guests = this.guests.filter(guest => guest.id !== userId);
        } else {
          console.error('Помилка встановлення статусу:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка підключення до API:', error);
      }
    },
    isBirthdayToday(birthDate) {
      if (!birthDate) return false;
      const today = new Date();
      const birthday = new Date(birthDate);
      return today.getMonth() === birthday.getMonth() && today.getDate() === birthday.getDate();
    },
  },
};
</script>

<style scoped>
.guests-page {
  padding: 20px;
  background: linear-gradient(135deg, #e6e6e6, #ffffff);
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 1200px;
  margin: 0 auto;
  position: relative; /* Ensure the loader is positioned relative to this container */
}

h2 {
  color: #333;
  text-align: center;
  font-size: 28px;
  margin-bottom: 20px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.search-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

th, td {
  border: 1px solid #ddd;
  padding: 15px;
  text-align: left;
  font-size: 16px;
}

th {
  background: linear-gradient(135deg, #f4f4f4, #eaeaea);
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #555;
}

td {
  background-color: #fff;
}

tr:nth-child(even) td {
  background-color: #f9f9f9;
}

tr:hover td {
  background-color: #f1f1f1;
  transition: background-color 0.2s ease;
}

.highlight {
  background-color: #ffeb3b; /* Bright yellow background */
  color: #ff0000; /* Red text color */
  font-weight: bold;
  border: 2px solid #ff0000; /* Red border */
  animation: blink 1s infinite; /* Blinking animation */
}

@keyframes blink {
  0% { background-color: #ffeb3b; }
  50% { background-color: #ffffff; }
  100% { background-color: #ffeb3b; }
}

button {
  padding: 8px 12px;
  margin: 2px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.admin-btn {
  background-color: #4caf50;
  color: white;
}

.admin-btn:hover {
  background-color: #45a049;
}

.ban-btn {
  background-color: #f44336;
  color: white;
}

.ban-btn:hover {
  background-color: #e57373;
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8); /* Semi-transparent background */
}

.loader {
  width: 50px;
  aspect-ratio: 1;
  display: grid;
  -webkit-mask: conic-gradient(from 15deg, #0000, #000);
  animation: l26 1s infinite steps(12);
  background:
      radial-gradient(closest-side at 50% 12.5%,
      #000 96%, #0000) 50% 0/20% 80% repeat-y,
      radial-gradient(closest-side at 12.5% 50%,
      #000 96%, #0000) 0 50%/80% 20% repeat-x;
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
  100% { transform: rotate(1turn); }
}
</style>