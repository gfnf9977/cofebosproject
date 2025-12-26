<template>
  <div class="orders-container">
    <h2 class="orders-title">Замовлення</h2>
    <div v-if="loading" class="loader-container">
      <div class="loader"></div>
    </div>
    <div v-else>
      <div v-if="orders.length > 0">
        <div v-for="order in orders" :key="order.id" class="order-details">
          <h3 class="order-id">Код замовлення: {{ order.id }}</h3>
          <div class="order-info">
            <p><strong>Замовник:</strong> {{ userDetails[order.user_id] || 'Unknown' }}</p>
            <p><strong>Адреса кав'ярні:</strong> {{ shopAddresses[order.shop_id] || 'Unknown' }}</p>
            <p><strong>Статус замовлення:</strong> {{ getOrderStatus(order.status) }}</p>
            <p><strong>Вартість:</strong> {{ order.total_price }} грн</p>
            <p><strong>Замовлено:</strong> {{ order.order_date }}</p>
          </div>

          <h4 class="section-title">Випічка</h4>
          <div v-if="order.bakeryItems.length > 0">
            <table class="items-table">
              <thead>
              <tr>
                <th>Назва випічки</th>
                <th>Кількість</th>
                <th>Ціна</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="bakery in order.bakeryItems" :key="bakery.bakery_id">
                <td>{{ bakeryNames[bakery.bakery_id] || 'Unknown' }}</td>
                <td>{{ bakery.quantity }}</td>
                <td>{{ bakery.price }}</td>
              </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            <p class="no-items">Немає випічки у цьому замовленні.</p>
          </div>

          <h4 class="section-title">Напої</h4>
          <div v-if="order.drinkItems.length > 0">
            <table class="items-table">
              <thead>
              <tr>
                <th>Назва напою</th>
                <th>Розмір</th>
                <th>Кількість</th>
                <th>Ціна</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="drink in order.drinkItems" :key="drink.drink_id">
                <td>{{ drinkNames[drink.drink_id] || 'Unknown' }}</td>
                <td>{{ drink.size }}</td>
                <td>{{ drink.quantity }}</td>
                <td>{{ drink.price }}</td>
              </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            <p class="no-items">Немає напоїв у цьому замовленні.</p>
          </div>
        </div>
      </div>
      <div v-else>
        <p class="no-orders">Немає замовлень.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrdersPrime',
  props: {
    userId: {
      type: Number,
      required: true,
    },
    orders: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      bakeryNames: {},
      drinkNames: {},
      shopAddresses: {},
      userDetails: {},
      loading: true, // Add loading state
    };
  },
  watch: {
    orders: {
      immediate: true,
      handler(newOrders) {
        if (newOrders && newOrders.length > 0) {
          this.fetchData();
        } else {
          this.loading = false; // No orders, stop loading
        }
      }
    }
  },
  methods: {
    getOrderStatus(status) {
      const statusMap = {
        pending: 'в обробці',
        paid: 'оплачено',
        finished: 'завершено',
      };
      return statusMap[status] || status;
    },
    async fetchData() {
      this.loading = true; // Start loading
      await Promise.all([
        this.fetchBakeryNames(),
        this.fetchDrinkNames(),
        this.fetchShopAddresses(),
        this.fetchUserDetails(),
      ]);
      this.loading = false; // Stop loading
    },
    async fetchBakeryNames() {
      const bakeryIds = [...new Set(this.orders.flatMap(order => {
        return order.bakeryItems.map(item => item.bakery_id);
      }))];

      if (bakeryIds.length === 0) return;

      const requestBody = { bakery_ids: bakeryIds };

      try {
        const response = await fetch('http://localhost:5000/api/bakery-names', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(requestBody),
        });

        if (response.ok) {
          const data = await response.json();
          this.bakeryNames = data;
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
    async fetchDrinkNames() {
      const drinkIds = [...new Set(this.orders.flatMap(order => {
        return order.drinkItems.map(item => item.drink_id);
      }))];

      if (drinkIds.length === 0) return;

      const requestBody = { drink_ids: drinkIds };

      try {
        const response = await fetch('http://localhost:5000/api/drink-names', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(requestBody),
        });

        if (response.ok) {
          const data = await response.json();
          this.drinkNames = data;
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
    async fetchShopAddresses() {
      const shopIds = [...new Set(this.orders.map(order => order.shop_id))];

      if (shopIds.length === 0) return;

      const requestBody = { shop_ids: shopIds };

      try {
        const response = await fetch('http://localhost:5000/api/shop-addresses', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(requestBody),
        });

        if (response.ok) {
          const data = await response.json();
          this.shopAddresses = data;
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
    async fetchUserDetails() {
      const userIds = [...new Set(this.orders.map(order => order.user_id))];

      if (userIds.length === 0) return;

      const requestBody = { user_ids: userIds };

      try {
        const response = await fetch('http://localhost:5000/api/user-details', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(requestBody),
        });

        if (response.ok) {
          const data = await response.json();
          this.userDetails = data;
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
  },
};
</script>

<style scoped>
.orders-container {
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.orders-title {
  color: #444;
  margin-bottom: 20px;
}

.order-details {
  margin-bottom: 20px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.order-id {
  margin-top: 0;
  color: #333;
}

.order-info p {
  margin: 5px 0;
  color: #666;
}

.section-title {
  margin-top: 15px;
  color: #333;
}

.items-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.items-table th,
.items-table td {
  border: 1px solid #e0e0e0;
  padding: 10px;
  text-align: left;
}

.items-table th {
  background-color: #f9f9f9;
  color: #333;
}

.no-items {
  color: #999;
  margin-top: 10px;
}

.no-orders {
  color: #999;
  text-align: center;
  margin-top: 20px;
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