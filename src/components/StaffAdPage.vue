<template>
  <div class="staff-page">
    <h2>Працівники</h2>
    <div class="shop-selector">
      <label for="shopSelect">Оберіть кав'ярню:</label>
      <select id="shopSelect" v-model="selectedShopId" @change="filterUsersByShop">
        <option v-for="shop in shops" :key="shop.id" :value="shop.id">
          {{ shop.Street }}, {{ shop.nomer }}
        </option>
      </select>
    </div>
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
        <th>Адреса кав'ярні</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="user in filteredUsers" :key="user.username">
        <td>{{ user.last_name }}</td>
        <td>{{ user.first_name }}</td>
        <td>{{ user.middle_name }}</td>
        <td>{{ user.phone_number }}</td>
        <td>{{ formatDate(user.birth_date) }}</td>
        <td>{{ getShopAddress(user.shop_id) }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "StaffPage",
  data() {
    return {
      users: [], // Дані користувачів
      shops: [], // Дані кав'ярень
      selectedShopId: null, // Вибраний ID кав'ярні
      currentUserId: null, // ID поточного користувача
      currentShopId: null, // ID кав'ярні поточного користувача
      isLoading: true, // Loading state
    };
  },
  computed: {
    filteredUsers() {
      if (this.selectedShopId) {
        return this.users.filter(user => user.shop_id === this.selectedShopId);
      }
      return this.users;
    },
  },
  async mounted() {
    try {
      const username = localStorage.getItem('username');
      if (username) {
        const userIdResponse = await fetch(`http://localhost:5000/api/user-id?username=${username}`);
        if (userIdResponse.ok) {
          const userIdData = await userIdResponse.json();
          this.currentUserId = userIdData.id;

          // Fetch the shop ID based on the user ID
          const shopIdResponse = await fetch(`http://localhost:5000/api/shop-id?user_id=${this.currentUserId}`);
          if (shopIdResponse.ok) {
            const shopIdData = await shopIdResponse.json();
            this.currentShopId = shopIdData.shop_id;
          } else {
            console.error('Помилка завантаження ID кав\'ярні:', shopIdResponse.statusText);
          }
        } else {
          console.error('Помилка завантаження ID користувача:', userIdResponse.statusText);
        }
      }

      const usersResponse = await fetch("http://localhost:5000/api/users");
      const shopsResponse = await fetch("http://localhost:5000/api/shops");
      if (usersResponse.ok && shopsResponse.ok) {
        this.users = await usersResponse.json();
        this.shops = await shopsResponse.json();
        // Set the default selected shop to the current user's shop
        if (this.currentShopId) {
          this.selectedShopId = this.currentShopId;
        } else if (this.shops.length > 0) {
          this.selectedShopId = this.shops[0].id;
        }
      } else {
        console.error("Помилка завантаження даних:", usersResponse.statusText, shopsResponse.statusText);
      }
    } catch (error) {
      console.error("Помилка підключення до API:", error);
    } finally {
      this.isLoading = false; // Hide the loader
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return "Невідомо";
      const options = {year: "numeric", month: "long", day: "numeric"};
      return new Date(date).toLocaleDateString("uk-UA", options);
    },
    getShopAddress(shopId) {
      const shop = this.shops.find(shop => shop.id === shopId);
      return shop ? `${shop.Street}, ${shop.nomer}` : "Невідомо";
    },
    filterUsersByShop() {
      // This method is called when the selected shop changes
      // You can add any additional logic here if needed
    },
  },
};
</script>

<style scoped>
.staff-page {
  padding: 30px;
  background: linear-gradient(135deg, #f0f0f0, #ffffff);
  border-radius: 15px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

h2 {
  color: #333;
  text-align: center;
  font-size: 28px;
  margin-bottom: 30px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

.shop-selector {
  margin-bottom: 30px;
  text-align: center;
}

.shop-selector label {
  margin-right: 15px;
  font-weight: bold;
  color: #555;
}

.shop-selector select {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  overflow: hidden;
}

th, td {
  border: 1px solid #ddd;
  padding: 15px 20px;
  text-align: left;
  font-size: 16px;
}

th {
  background: linear-gradient(135deg, #f9f9f9, #ececec);
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #444;
}

td {
  background-color: #fff;
}

tr:nth-child(even) td {
  background-color: #fafafa;
}

tr:hover td {
  background-color: #f5f5f5;
  transition: background-color 0.3s ease;
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
  .staff-page {
    padding: 20px;
  }

  h2 {
    font-size: 24px;
    margin-bottom: 20px;
  }

  .shop-selector {
    margin-bottom: 20px;
  }

  .shop-selector label {
    margin-right: 10px;
  }

  .shop-selector select {
    padding: 8px;
    font-size: 14px;
  }

  table {
    margin-top: 15px;
  }

  th, td {
    padding: 12px 15px;
    font-size: 14px;
  }
}
</style>