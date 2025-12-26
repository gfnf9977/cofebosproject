<template>
  <div class="guests-page">
    <h2>Гості</h2>
    <input
        type="text"
        v-model="searchQuery"
        placeholder="Пошук за прізвищем"
        class="search-input"
    />
    <div v-if="isLoading" class="loader-container">
      <div class="loader"></div>
    </div>
    <table v-else>
      <thead>
      <tr>
        <th>Прізвище</th>
        <th>Ім'я</th>
        <th>По батькові</th>
        <th>Телефон</th>
        <th>Дата народження</th>
        <th>Бали</th>
        <th>Додати бали</th> <!-- Add Points column header -->
      </tr>
      </thead>
      <tbody>
      <tr v-for="guest in filteredGuests" :key="guest.id">
        <td>{{ guest.last_name }}</td>
        <td>{{ guest.first_name }}</td>
        <td>{{ guest.middle_name }}</td>
        <td>{{ guest.phone_number }}</td>
        <td :class="{ 'birthday-highlight': isBirthday(guest.birth_date) }">
          {{ formatDate(guest.birth_date) }}
        </td>
        <td>{{ guest.points }}</td>
        <td>
          <input type="number" v-model="guest.newPoints" placeholder="Додати бали" />
          <button @click="addPoints(guest.id, guest.newPoints)">Додати</button>
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
      searchQuery: '', // Search input
      isLoading: true, // Loading state
    };
  },
  async mounted() {
    try {
      const response = await fetch('http://localhost:5000/api/guests'); // Змініть URL за потреби
      if (response.ok) {
        this.guests = await response.json();
        // Initialize newPoints for each guest
        this.guests.forEach(guest => {
          guest.newPoints = 0;
        });
      } else {
        console.error('Помилка завантаження даних:', response.statusText);
      }
    } catch (error) {
      console.error('Помилка підключення до API:', error);
    } finally {
      this.isLoading = false; // Hide the loader
    }
  },
  computed: {
    filteredGuests() {
      if (!this.searchQuery) {
        return this.guests;
      }
      const query = this.searchQuery.toLowerCase();
      return this.guests.filter(guest =>
          guest.last_name && guest.last_name.toLowerCase().includes(query)
      );
    },
  },
  methods: {
    formatDate(date) {
      if (!date) return 'Невідомо';
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString('uk-UA', options);
    },
    isBirthday(date) {
      if (!date) return false;
      const birthday = new Date(date);
      const today = new Date();
      return birthday.getMonth() === today.getMonth() && birthday.getDate() === today.getDate();
    },
    async addPoints(userId, points) {
      try {
        const response = await fetch(`http://localhost:5000/api/update-points/${userId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ points }),
        });
        if (response.ok) {
          const message = await response.json();
          alert(message.message);
          // Refresh the guest list to update the points
          this.mounted();
        } else {
          console.error('Помилка оновлення балів:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка підключення до API:', error);
      }
    },
  },
};
</script>


<style scoped>
.guests-page {
  padding: 20px;
  background: linear-gradient(135deg, #f0f0f0, #ffffff);
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

h2 {
  color: #333;
  text-align: center;
  font-size: 28px;
  margin-bottom: 20px;
  font-weight: bold;
  letter-spacing: 1px;
}

.search-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
  font-size: 16px;
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
  background: linear-gradient(135deg, #f9f9f9, #e6e6e6);
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

input[type="number"] {
  width: 70px;
  margin-right: 10px;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
}

button {
  padding: 8px 15px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #45a049;
}

.birthday-highlight {
  background-color: #ffeb3b; /* Highlight color for birthday */
  font-weight: bold;
  color: #d32f2f; /* Text color for better contrast */
  border: 2px solid #d32f2f; /* Border for more emphasis */
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.loader {
  --s: 25px;
  --g: 5px;
  width: calc(2*(1.353*var(--s) + var(--g)));
  aspect-ratio: 1;
  background:
      linear-gradient(#000 0 0) left/50% 100% no-repeat,
      conic-gradient(from -90deg at var(--s) calc(0.353*var(--s)),
      #fff 135deg, #666 0 270deg, #aaa 0);
  background-blend-mode: multiply;
  --_m:
      linear-gradient(to bottom right,
      #0000 calc(0.25*var(--s)), #000 0 calc(100% - calc(0.25*var(--s)) - 1.414*var(--g)), #0000 0),
      conic-gradient(from -90deg at right var(--g) bottom var(--g), #000 90deg, #0000 0);
  -webkit-mask: var(--_m);
  mask: var(--_m);
  background-size: 50% 50%;
  -webkit-mask-size: 50% 50%;
  mask-size: 50% 50%;
  -webkit-mask-composite: source-in;
  mask-composite: intersect;
  animation: l9 1.5s infinite;
}

@keyframes l9 {
  0%, 12.5% { background-position: 0% 0%, 0 0; }
  12.6%, 37.5% { background-position: 100% 0%, 0 0; }
  37.6%, 62.5% { background-position: 100% 100%, 0 0; }
  62.6%, 87.5% { background-position: 0% 100%, 0 0; }
  87.6%, 100% { background-position: 0% 0%, 0 0; }
}

@media (max-width: 768px) {
  table, thead, tbody, th, td, tr {
    display: block;
  }

  thead tr {
    display: none;
  }

  tr {
    margin-bottom: 10px;
  }

  td {
    text-align: right;
    padding-left: 50%;
    position: relative;
  }

  td::before {
    content: attr(data-label);
    position: absolute;
    left: 10px;
    width: calc(50% - 20px);
    padding-left: 10px;
    font-weight: bold;
    text-align: left;
  }
}
</style>