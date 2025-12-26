<template>
  <div class="staff-page">
    <h2>Працівники</h2>
    <div v-if="loading" class="loader-container">
      <div class="loader"></div>
    </div>
    <div v-else>
      <div class="search-bar">
        <label for="searchInput">Пошук за прізвищем та логіном:</label>
        <input id="searchInput" v-model="searchQuery" @input="filterUsers" placeholder="Введіть прізвище або логін" />
      </div>
      <div class="shop-selector">
        <label for="shopSelect">Оберіть кав'ярню:</label>
        <select id="shopSelect" v-model="selectedShopId" @change="filterUsersByShop">
          <option value="">Всі</option>
          <option v-for="shop in shops" :key="shop.id" :value="shop.id">
            {{ shop.Street }}, {{ shop.nomer }}
          </option>
        </select>
      </div>
      <table>
        <thead>
        <tr>
          <th>Прізвище</th>
          <th>Ім'я</th>
          <th>По батькові</th>
          <th>Логін</th>
          <th>Телефон</th>
          <th>Дата народження</th>
          <th>Адреса кав'ярні</th>
          <th>Дії</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="user in filteredUsers" :key="user.username">
          <td>{{ user.last_name }}</td>
          <td>{{ user.first_name }}</td>
          <td>{{ user.middle_name }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.phone_number }}</td>
          <td :class="{ 'highlight': isBirthdayToday(user.birth_date) }">{{ formatDate(user.birth_date) }}</td>
          <td>{{ getShopAddress(user.shop_id) }}</td>
          <td>
            <button class="action-button" @click="setUserStatus(user.id)">Звільнити</button>
            <button v-if="!user.shop_id" class="action-button" @click="openAssignShopModal(user.id)">Призначити кав'ярню</button>
          </td>
        </tr>
        </tbody>
      </table>

      <!-- Modal for assigning shop -->
      <div v-if="showAssignShopModal" class="modal">
        <div class="modal-content">
          <span class="close" @click="closeAssignShopModal">&times;</span>
          <h3>Призначити кав'ярню</h3>
          <label for="assignShopSelect">Оберіть кав'ярню:</label>
          <select id="assignShopSelect" v-model="selectedAssignShopId">
            <option v-for="shop in shops" :key="shop.id" :value="shop.id">
              {{ shop.Street }}, {{ shop.nomer }}
            </option>
          </select>
          <button class="action-button" @click="assignShopToUser">Призначити</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "StaffPage",
  data() {
    return {
      users: [], // Дані користувачів
      shops: [], // Дані кав'ярень
      selectedShopId: '', // Вибраний ID кав'ярні, по дефолту "Всі"
      showAssignShopModal: false, // Показувати модальне вікно для призначення кав'ярні
      selectedAssignShopId: null, // Вибраний ID кав'ярні для призначення
      currentUserId: null, // ID користувача, якому призначається кав'ярня
      searchQuery: '', // Пошуковий запит
      loading: true, // Loading state
    };
  },
  computed: {
    filteredUsers() {
      let filtered = this.users;

      // Filter by shop if selected
      if (this.selectedShopId) {
        filtered = filtered.filter(user => user.shop_id === this.selectedShopId);
      }

      // Filter by search query
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(user =>
            user.last_name.toLowerCase().includes(query) ||
            user.username.toLowerCase().includes(query)
        );
      }

      return filtered;
    },
  },
  async mounted() {
    try {
      const usersResponse = await fetch("http://localhost:5000/api/users");
      const shopsResponse = await fetch("http://localhost:5000/api/shops");
      if (usersResponse.ok && shopsResponse.ok) {
        this.users = await usersResponse.json();
        this.shops = await shopsResponse.json();
      } else {
        console.error("Помилка завантаження даних:", usersResponse.statusText, shopsResponse.statusText);
      }
    } catch (error) {
      console.error("Помилка підключення до API:", error);
    } finally {
      this.loading = false; // Hide the loader
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return "Невідомо";
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(date).toLocaleDateString("uk-UA", options);
    },
    getShopAddress(shopId) {
      const shop = this.shops.find(shop => shop.id === shopId);
      return shop ? `${shop.Street}, ${shop.nomer}` : "Невідомо";
    },
    async setUserStatus(userId) {
      try {
        const response = await fetch(`http://localhost:5000/api/set-user/${userId}`, {
          method: 'POST',
        });
        if (response.ok) {
          alert('Status set to user successfully');
          // Optionally, refresh the user list
          this.users = this.users.filter(user => user.id !== userId);
        } else {
          console.error('Помилка встановлення статусу:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка підключення до API:', error);
      }
    },
    filterUsersByShop() {
      // This method is called when the selected shop changes
      // You can add any additional logic here if needed
    },
    openAssignShopModal(userId) {
      this.currentUserId = userId;
      this.showAssignShopModal = true;
    },
    closeAssignShopModal() {
      this.showAssignShopModal = false;
      this.currentUserId = null;
      this.selectedAssignShopId = null;
    },
    async assignShopToUser() {
      if (!this.selectedAssignShopId) {
        alert('Будь ласка, виберіть кав\'ярню.');
        return;
      }

      try {
        const response = await fetch(`http://localhost:5000/api/update-shop/${this.currentUserId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ shop_id: this.selectedAssignShopId }),
        });

        if (response.ok) {
          alert('Кав\'ярню призначено успішно.');
          this.closeAssignShopModal();
          // Optionally, refresh the user list
          this.users = this.users.map(user =>
              user.id === this.currentUserId ? { ...user, shop_id: this.selectedAssignShopId } : user
          );
        } else {
          console.error('Помилка призначення кав\'ярні:', response.statusText);
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
    filterUsers() {
      // This method is called when the search query changes
      // You can add any additional logic here if needed
    },
  },
};
</script>

<style scoped>
.staff-page {
  padding: 20px;
  background: linear-gradient(135deg, #e6e6e6, #ffffff);
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
  text-transform: uppercase;
  letter-spacing: 1px;
}

.search-bar {
  margin-bottom: 20px;
  text-align: center;
}

.search-bar label {
  margin-right: 10px;
  font-weight: bold;
  color: #555;
}

.search-bar input {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
  width: 300px;
}

.shop-selector {
  margin-bottom: 20px;
  text-align: center;
}

.shop-selector label {
  margin-right: 10px;
  font-weight: bold;
  color: #555;
}

.shop-selector select {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
  color: #333;
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

.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0,0,0);
  background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 500px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border-radius: 10px;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.action-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.action-button:hover {
  background-color: #0056b3;
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Full viewport height */
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