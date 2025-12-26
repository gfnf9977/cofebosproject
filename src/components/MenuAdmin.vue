<template>
  <div class="menu-container">
    <!-- Header Section -->
    <header class="menu-header">
      <h2 class="text-4xl font-bold mb-10 text-center text-gray-800">Меню кав'ярні</h2>
      <div class="shop-info mb-6">
        <label for="shopInfo" class="block text-sm font-medium mb-2 text-gray-700">Кав'ярня:</label>
        <input
            id="shopInfo"
            v-model="shopInfo"
            class="w-full p-4 border border-gray-300 rounded-lg shadow-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            readonly
        >
      </div>
      <div class="user-select mb-6">
        <label for="userSelect" class="block text-sm font-medium mb-2 text-gray-700">Оберіть користувача:</label>
        <input
            v-model="searchQuery"
            placeholder="Пошук за прізвищем"
            class="w-full p-4 border border-gray-300 rounded-lg shadow-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
        />
        <div class="chat-list">
          <div v-for="user in filteredUsers" :key="user.id" class="chat-item" @click="selectUser(user.id)">
            <strong>{{ user.last_name }} {{ user.first_name }} {{ user.middle_name }}</strong>
          </div>
        </div>
      </div>
      <div v-if="selectedShop" class="user-info mb-6">
        <p class="text-xl font-semibold text-gray-800">Користувач: {{ selectedUserName }}</p>
        <p class="text-gray-600">ID користувача: {{ selectedUser }}</p>
      </div>
    </header>

    <!-- Main Menu Section -->
    <div v-if="selectedShop" class="menu-content">
      <div class="grid md:grid-cols-2 gap-10">
        <!-- Drinks Menu -->
        <div class="drinks-section">
          <h3 class="text-3xl font-semibold mb-8 text-gray-800">Напої</h3>
          <div class="menu-items">
            <div
                v-for="drink in drinks"
                :key="drink.id"
                class="menu-item p-8 border border-gray-200 rounded-2xl mb-8 bg-white shadow-lg transition-transform transform hover:scale-105 hover:shadow-xl"
            >
              <h4 class="font-medium text-2xl mb-6 text-gray-800">{{ drink.name }}</h4>
              <img :src="getMenuImageUrl(drink.id)" alt="Menu Image" class="mb-6 rounded-lg shadow-md w-full h-48 object-cover"/>
              <ul class="space-y-6">
                <li
                    v-for="size in getDrinkSizes(drink.id)"
                    :key="size.size"
                    class="flex items-center justify-between"
                >
                  <span class="text-xl text-gray-800">{{ size.size }} - {{ size.price }} грн</span>
                  <div class="flex items-center gap-6">
                    <input
                        type="number"
                        v-model="size.quantity"
                        min="1"
                        class="w-24 p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                    <button
                        @click="addToCart('drink', drink, size)"
                        class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      Додати
                    </button>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Bakery Menu -->
        <div v-if="showBakery" class="bakery-section">
          <h3 class="text-3xl font-semibold mb-8 text-gray-800">Випічка</h3>
          <div class="menu-items">
            <div
                v-for="item in bakeryItems"
                :key="item.id"
                class="menu-item p-8 border border-gray-200 rounded-2xl mb-8 bg-white shadow-lg transition-transform transform hover:scale-105 hover:shadow-xl"
            >
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="font-medium text-2xl text-gray-800">{{ item.name }}</h4>
                  <p class="text-gray-600 text-xl">{{ item.price }} грн</p>
                </div>
                <div class="flex items-center gap-6">
                  <img :src="getBakeryImageUrl(item.id)" alt="Bakery Image" class="mb-6 rounded-lg shadow-md w-full h-48 object-cover"/>
                  <input
                      type="number"
                      v-model="item.quantity"
                      min="1"
                      class="w-24 p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                  <button
                      @click="addToCart('bakery', item)"
                      class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Додати
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Shopping Cart -->
      <div v-if="cart.length > 0" class="cart-section mt-16 p-10 border border-gray-200 rounded-2xl bg-gray-50 shadow-lg">
        <h3 class="text-3xl font-semibold mb-8 text-gray-800">Ваше замовлення</h3>
        <ul class="space-y-6">
          <li
              v-for="(item, index) in cart"
              :key="index"
              class="flex items-center justify-between p-6 bg-white rounded-2xl shadow-lg"
          >
            <div>
              <span class="font-medium text-xl text-gray-800">{{ item.name }}</span>
              <span v-if="item.size" class="text-gray-600 ml-2">({{ item.size }})</span>
              <span class="text-gray-600 ml-2">
                {{ item.quantity }} x {{ item.price }} грн
              </span>
            </div>
            <button
                @click="removeFromCart(index)"
                class="text-red-600 hover:text-red-700 transition-colors"
            >
              Видалити
            </button>
          </li>
        </ul>
        <div class="mt-8 flex items-center justify-between">
          <p class="font-semibold text-2xl text-gray-800">Загальна сума: {{ totalCartPrice }} грн</p>
          <button
              @click="submitOrder"
              class="bg-green-600 text-white px-8 py-4 rounded-lg hover:bg-green-700 transition-colors"
          >
            Оформити замовлення
          </button>
        </div>
      </div>
    </div>
    <div v-if="loading" class="loader-container">
      <div class="loader"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MenuUsr',
  props: {
    userId: {
      type: Number,
      required: true
    },
    username: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      drinks: [],
      drinkSizes: [],
      bakeryItems: [],
      shops: [],
      users: [],
      selectedShop: null,
      selectedUser: null,
      showBakery: false,
      cart: [],
      loading: false,
      error: null,
      currentUserId: null,
      currentShopId: null,
      shopInfo: '',
      searchQuery: ''
    }
  },
  computed: {
    totalCartPrice() {
      return this.cart.reduce((total, item) => {
        return total + (item.price * item.quantity)
      }, 0)
    },
    selectedUserName() {
      const user = this.users.find(u => u.id === this.selectedUser);
      return user ? `${user.last_name} ${user.first_name} ${user.middle_name}` : '';
    },
    filteredUsers() {
      return this.users
          .filter(user => user.id !== this.userId && user.status === 'user')
          .filter(user => {
            const lastName = user.last_name.toLowerCase();
            return lastName.includes(this.searchQuery.toLowerCase());
          });
    }
  },
  methods: {
    async fetchData() {
      try {
        this.loading = true
        const [drinksRes, drinkSizesRes, bakeryRes, shopsRes, usersRes] = await Promise.all([
          fetch('http://localhost:5000/api/drinks'),
          fetch('http://localhost:5000/api/drink_sizes'),
          fetch('http://localhost:5000/api/bakery'),
          fetch('http://localhost:5000/api/shops'),
          fetch('http://localhost:5000/api/get_all_users')
        ])

        if (!drinksRes.ok || !drinkSizesRes.ok || !bakeryRes.ok || !shopsRes.ok || !usersRes.ok) {
          throw new Error('Помилка завантаження даних')
        }

        this.drinks = await drinksRes.json()
        this.drinkSizes = await drinkSizesRes.json()
        this.bakeryItems = await bakeryRes.json()
        this.shops = await shopsRes.json()
        this.users = await usersRes.json()

        this.bakeryItems = this.bakeryItems.map(item => ({
          ...item,
          quantity: 1
        }))
      } catch (error) {
        this.error = 'Помилка завантаження даних'
        console.error('Error:', error)
      } finally {
        this.loading = false
      }
    },

    showMenu() {
      const selectedShop = this.shops.find(shop => shop.id === this.selectedShop)
      if (selectedShop) {
        this.showBakery = Boolean(selectedShop.has_bakery)
      }
    },

    getDrinkSizes(drinkId) {
      return this.drinkSizes
          .filter(size => size.drink_id === drinkId)
          .map(size => ({
            ...size,
            quantity: 1
          }))
    },

    addToCart(type, item, size = null) {
      const existingItemIndex = this.cart.findIndex(cartItem =>
          cartItem.id === item.id &&
          cartItem.type === type &&
          (size ? cartItem.size === size.size : true)
      );

      if (existingItemIndex !== -1) {
        this.cart[existingItemIndex].quantity += size ? size.quantity : item.quantity;
      } else {
        const cartItem = {
          type,
          id: item.id,
          name: item.name,
          quantity: size ? size.quantity : item.quantity,
          price: size ? size.price : item.price
        };

        if (size) {
          cartItem.size = size.size;
        }

        this.cart.push(cartItem);
      }
    },

    removeFromCart(index) {
      this.cart.splice(index, 1)
    },

    async submitOrder() {
      if (!this.selectedShop || !this.selectedUser || !this.cart.length) return

      try {
        const orderData = {
          user_id: this.selectedUser,
          shop_id: this.selectedShop,
          drinks: this.cart
              .filter(item => item.type === 'drink')
              .map(item => ({
                drink_id: item.id,
                size: item.size,
                quantity: item.quantity
              })),
          bakery_items: this.cart
              .filter(item => item.type === 'bakery')
              .map(item => ({
                bakery_id: item.id,
                quantity: item.quantity
              })),
          total_price: this.totalCartPrice
        }

        const response = await fetch('http://localhost:5000/api/orders', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(orderData)
        })

        if (!response.ok) {
          throw new Error('Помилка створення замовлення')
        }

        const data = await response.json()
        console.log('Order created:', data)

        this.cart = []
        alert('Замовлення успішно створено!')
      } catch (error) {
        console.error('Error:', error)
        alert('Помилка при створенні замовлення')
      }
    },

    getMenuImageUrl(drinkId) {
      return `http://localhost:5000/api/get-menu-image/${drinkId}`;
    },

    getBakeryImageUrl(bakeryId) {
      return `http://localhost:5000/api/get-bakery-image/${bakeryId}`;
    },

    selectUser(userId) {
      this.selectedUser = userId;
    }
  },
  async mounted() {
    await this.fetchData();
    try {
      const userIdResponse = await fetch(`http://localhost:5000/api/user-id?username=${this.username}`);
      if (userIdResponse.ok) {
        const userIdData = await userIdResponse.json();
        this.currentUserId = userIdData.id;

        const shopIdResponse = await fetch(`http://localhost:5000/api/shop-id?user_id=${this.currentUserId}`);
        if (shopIdResponse.ok) {
          const shopIdData = await shopIdResponse.json();
          this.currentShopId = shopIdData.shop_id;
          this.selectedShop = this.currentShopId;
          const selectedShop = this.shops.find(shop => shop.id === this.selectedShop);
          if (selectedShop) {
            this.shopInfo = `${selectedShop.Street}, ${selectedShop.nomer} - ${selectedShop.loc_desc}`;
            this.showBakery = Boolean(selectedShop.has_bakery);
          }
        } else {
          console.error('Помилка завантаження ID кав\'ярні:', shopIdResponse.statusText);
        }
      } else {
        console.error('Помилка завантаження ID користувача:', userIdResponse.statusText);
      }
    } catch (error) {
      console.error("Помилка підключення до API:", error);
    }
  }
}
</script>

<style scoped>
.menu-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa, #e6e9f0);
  border-radius: 20px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

.menu-header {
  text-align: center;
  margin-bottom: 40px;
}

.menu-header h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #333;
}

.shop-info, .user-select, .user-info {
  margin-bottom: 20px;
}

.shop-info label, .user-select label, .user-info p {
  font-size: 1rem;
  font-weight: 500;
  color: #555;
}

.shop-info input, .user-select input {
  font-size: 1rem;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chat-list {
  width: 100%;
  max-width: 600px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
  overflow-y: auto;
  max-height: 300px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chat-item {
  padding: 12px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.3s;
}

.chat-item:hover {
  background-color: #f0f0f0;
}

.chat-item strong {
  font-weight: 600;
  color: #333;
}

.menu-content {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.menu-item {
  transition: all 0.3s ease-in-out;
}

.menu-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

input[type="number"] {
  -moz-appearance: textfield;
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.menu-item img {
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.menu-item button {
  background-color: #007bff;
  color: #fff;
  padding: 10px 20px;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.menu-item button:hover {
  background-color: #0056b3;
}

.cart-section {
  margin-top: 40px;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.cart-section h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
}

.cart-section ul {
  list-style: none;
  padding: 0;
}

.cart-section li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}

.cart-section li div {
  display: flex;
  align-items: center;
}

.cart-section li button {
  color: #ff4d4f;
  font-weight: 600;
  transition: color 0.3s;
}

.cart-section li button:hover {
  color: #d93025;
}

.cart-section .total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.cart-section .total p {
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
}

.cart-section .total button {
  background-color: #28a745;
  color: #fff;
  padding: 10px 20px;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.cart-section .total button:hover {
  background-color: #218838;
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
</style>