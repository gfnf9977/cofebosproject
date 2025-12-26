<template>
  <div class="menu-container">
    <!-- Loading Animation -->
    <div v-if="loading" class="loader-container">
      <div class="coffee-cup">
        <img src="/coffeboss.png" alt="Coffeboss" class="coffee-image" />
      </div>
    </div>

    <!-- Header Section -->
    <header v-else class="menu-header bg-gray-900 text-white p-8 rounded-t-2xl shadow-xl">
      <h2 class="text-4xl font-extrabold mb-6">Меню кав'ярні</h2>
      <div class="shop-select mb-8">
        <label for="shopSelect" class="block text-lg font-medium mb-4">Оберіть кав'ярню:</label>
        <select id="shopSelect" v-model="selectedShop" @change="showMenu" class="w-full p-4 border rounded-xl bg-white text-gray-900 shadow-md">
          <option value="null" disabled>Оберіть кав'ярню</option>
          <option v-for="shop in shops" :key="shop.id" :value="shop.id">
            {{ shop.Street }} {{ shop.nomer }} - {{ shop.loc_desc }}
          </option>
        </select>
      </div>
      <div v-if="selectedShop" class="user-info mb-8">
        <p class="text-2xl">Користувач: {{ username }}</p>
        <p class="text-2xl">ID користувача: {{ userID }}</p>
      </div>
    </header>

    <!-- Main Menu Section -->
    <div v-if="selectedShop" class="menu-content p-8 bg-gray-50 rounded-b-2xl shadow-xl">
      <div class="grid md:grid-cols-2 gap-12">
        <!-- Drinks Menu -->
        <div class="drinks-section">
          <h3 class="text-3xl font-bold mb-8">Напої</h3>
          <div class="menu-items space-y-8">
            <div v-for="drink in drinks" :key="drink.id" class="menu-item p-8 bg-white rounded-2xl shadow-xl transition-transform transform hover:scale-105">
              <h4 class="font-semibold text-2xl mb-6">{{ drink.name }}</h4>
              <img :src="getMenuImageUrl(drink.id)" alt="Menu Image" class="mb-6 rounded-xl"/>
              <ul class="space-y-6">
                <li v-for="size in getDrinkSizes(drink.id)" :key="size.size" class="flex items-center justify-between">
                  <span class="text-xl">{{ size.size }} - {{ size.price }} грн</span>
                  <div class="flex items-center gap-6">
                    <input type="number" v-model="size.quantity" min="1" class="w-24 p-3 border rounded-xl shadow-sm">
                    <button @click="addToCart('drink', drink, size)" class="add-button">
                      +
                    </button>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Bakery Menu -->
        <div v-if="showBakery" class="bakery-section">
          <h3 class="text-3xl font-bold mb-8">Випічка</h3>
          <div class="menu-items space-y-8">
            <div v-for="item in bakeryItems" :key="item.id" class="menu-item p-8 bg-white rounded-2xl shadow-xl transition-transform transform hover:scale-105">
              <div class="flex items-center justify-between mb-6">
                <div>
                  <h4 class="font-semibold text-2xl">{{ item.name }}</h4>
                  <p class="text-gray-700 text-xl">{{ item.price }} грн</p>
                </div>
                <img :src="getBakeryImageUrl(item.id)" alt="Bakery Image" class="rounded-xl"/>
              </div>
              <div class="flex items-center gap-6">
                <input type="number" v-model="item.quantity" min="1" class="w-24 p-3 border rounded-xl shadow-sm">
                <button @click="addToCart('bakery', item)" class="add-button">
                  +
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Shopping Cart -->
      <div v-if="cart.length > 0" class="cart-section mt-12 p-8 bg-white rounded-2xl shadow-xl">
        <div class="cart-image mb-6">
          <img src="/shopping-basket.png" alt="Shopping Basket" class="basket-image"/>
        </div>
        <h3 class="text-3xl font-bold mb-8">Ваше замовлення</h3>
        <ul class="space-y-6">
          <li v-for="(item, index) in cart" :key="index" class="flex items-center justify-between p-6 bg-gray-50 rounded-xl shadow-sm">
            <div>
              <span class="font-semibold text-2xl">{{ item.name }}</span>
              <span v-if="item.size" class="text-gray-600 ml-2">({{ item.size }})</span>
              <span class="text-gray-600 ml-2">
                {{ item.quantity }} x {{ item.price }} грн
              </span>
            </div>
            <button @click="removeFromCart(index)" class="text-red-700 hover:text-red-800 transition-colors">
              Видалити
            </button>
          </li>
        </ul>
        <div class="mt-8 flex items-center justify-between">
          <p class="font-bold text-3xl">Загальна сума: {{ totalCartPrice }} грн</p>
          <button @click="submitOrder" class="bg-green-700 text-white px-8 py-4 rounded-xl hover:bg-green-800 transition-colors">
            Оформити замовлення
          </button>
        </div>
      </div>
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
      selectedShop: null,
      showBakery: false,
      cart: [],
      loading: true, // Added loading state
      error: null,
      userID: null
    }
  },
  computed: {
    totalCartPrice() {
      return this.cart.reduce((total, item) => {
        return total + (item.price * item.quantity)
      }, 0)
    }
  },
  methods: {
    async fetchData() {
      try {
        this.loading = true
        const [drinksRes, drinkSizesRes, bakeryRes, shopsRes] = await Promise.all([
          fetch('http://localhost:5000/api/drinks'),
          fetch('http://localhost:5000/api/drink_sizes'),
          fetch('http://localhost:5000/api/bakery'),
          fetch('http://localhost:5000/api/shops')
        ])
        if (!drinksRes.ok || !drinkSizesRes.ok || !bakeryRes.ok || !shopsRes.ok) {
          throw new Error('Помилка завантаження даних')
        }
        this.drinks = await drinksRes.json()
        this.drinkSizes = await drinkSizesRes.json()
        this.bakeryItems = await bakeryRes.json()
        this.shops = await shopsRes.json()
        this.bakeryItems = this.bakeryItems.map(item => ({ ...item, quantity: 1 }))
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
          .map(size => ({ ...size, quantity: 1 }))
    },
    addToCart(type, item, size = null) {
      const existingItemIndex = this.cart.findIndex(cartItem =>
          cartItem.id === item.id &&
          cartItem.type === type &&
          (size ? cartItem.size === size.size : true)
      )
      if (existingItemIndex !== -1) {
        this.cart[existingItemIndex].quantity += size ? size.quantity : item.quantity
      } else {
        const cartItem = {
          type,
          id: item.id,
          name: item.name,
          quantity: size ? size.quantity : item.quantity,
          price: size ? size.price : item.price
        }
        if (size) {
          cartItem.size = size.size
        }
        this.cart.push(cartItem)
      }
    },
    removeFromCart(index) {
      this.cart.splice(index, 1)
    },
    async submitOrder() {
      if (!this.selectedShop || !this.cart.length) return
      try {
        const orderData = {
          user_id: this.userID,
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
    async fetchUserId() {
      try {
        const response = await fetch(`http://localhost:5000/api/user-id?username=${this.username}`)
        if (!response.ok) {
          throw new Error('Помилка отримання id користувача')
        }
        const data = await response.json()
        this.userID = data.id
        console.log('User ID:', this.userID)
      } catch (error) {
        console.error('Error:', error)
      }
    },
    getMenuImageUrl(drinkId) {
      return `http://localhost:5000/api/get-menu-image/${drinkId}`;
    },
    getBakeryImageUrl(bakeryId) {
      return `http://localhost:5000/api/get-bakery-image/${bakeryId}`;
    }
  },
  async mounted() {
    await this.fetchData()
    await this.fetchUserId()
    // Simulate loading
    setTimeout(() => {
      this.loading = false;
    }, 3000);
  }
}
</script>

<style scoped>
.menu-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

.menu-header {
  background-color: #1f2937;
  color: #ffffff;
  padding: 2rem;
  border-radius: 1.5rem 1.5rem 0 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.menu-content {
  background-color: #f9fafb;
  padding: 2rem;
  border-radius: 0 0 1.5rem 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.menu-item {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease-in-out;
}

.menu-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.1);
}

input[type="number"] {
  -moz-appearance: textfield;
  appearance: textfield;
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: border-color 0.2s ease-in-out;
}

input[type="number"]:focus {
  border-color: #6b7280;
  outline: none;
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f9fafb;
}

.coffee-cup {
  width: 200px;
  height: 200px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.coffee-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.cart-image {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.basket-image {
  width: 100px;
  height: 100px;
  object-fit: contain;
}

.cart-section {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.cart-section h3 {
  margin-bottom: 1rem;
}

.cart-section ul {
  list-style: none;
  padding: 0;
}

.cart-section li {
  background-color: #f3f4f6;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cart-section button {
  background-color: #ef4444;
  color: #ffffff;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: background-color 0.2s ease-in-out;
}

.cart-section button:hover {
  background-color: #dc2626;
}

.cart-section .total {
  font-size: 1.5rem;
  font-weight: bold;
  margin-top: 1rem;
}

.cart-section .checkout-button {
  background-color: #10b981;
  color: #ffffff;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  transition: background-color 0.2s ease-in-out;
}

.cart-section .checkout-button:hover {
  background-color: #059669;
}

.add-button {
  background-color: #10b981;
  color: #ffffff;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

.add-button:hover {
  background-color: #059669;
}
</style>