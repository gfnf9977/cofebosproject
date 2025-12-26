<template>
  <div class="orders-container">
    <h2>Мої замовлення</h2>
    <div v-if="loading" class="loader-container">
      <div class="coffee-cup">
        <img src="coffeboss.png" alt="Coffeboss" class="coffee-image" />
      </div>
    </div>
    <div v-else>
      <div v-if="orders.length > 0">
        <div v-for="order in orders" :key="order.id" class="order-card">
          <h3>Замовлення ID: {{ order.id }}</h3>
          <p>Замовив: {{ userDetails[order.user_id] || 'Наш любий клієнт' }}</p>
          <p>Адреса кав'ярні: {{ shopAddresses[order.shop_id] || 'Unknown' }}</p>
          <p>Статус замовлення: <span :class="`status-${order.status}`">{{ getStatusDisplayText(order.status) }}</span></p>
          <p>Всього до сплати: {{ order.total_price }} грн</p>
          <p>Замовлено: {{ order.order_date }}</p>

          <div class="order-section">
            <h4>Випічка</h4>
            <div v-if="order.bakeryItems.length > 0">
              <table class="order-table">
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
                  <td>{{ bakery.price }} грн</td>
                </tr>
                </tbody>
              </table>
            </div>
            <div v-else>
              <p class="no-items">Немає випічки у цьому замовленні.</p>
            </div>
          </div>

          <div class="order-section">
            <h4>Напої</h4>
            <div v-if="order.drinkItems.length > 0">
              <table class="order-table">
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
                  <td>{{ drink.price }} грн</td>
                </tr>
                </tbody>
              </table>
            </div>
            <div v-else>
              <p class="no-items">Немає напоїв у цьому замовленні.</p>
            </div>
          </div>

          <div v-if="order.status === 'pending'" class="action-buttons">
            <button class="btn-pay" @click="openPaymentModal(order.id)">Оплатити картою</button>
            <button class="btn-points" @click="openPointsPaymentModal(order.id)">Оплатити балами</button>
            <button class="btn-lucky" @click="openLuckyReceiptModal(order.id)">Маю щасливий чек?</button>
          </div>
        </div>
      </div>
      <div v-else>
        <p class="no-orders">Немає замовлень.</p>
      </div>
      <PaymentModal :isOpen="isPaymentModalOpen" :orderId="selectedOrderId" :userId="userId" @close="closePaymentModal" />
      <PointsPaymentModal :isOpen="isPointsPaymentModalOpen" :userId="userId" :orderId="selectedOrderId" @close="closePointsPaymentModal" />
      <LuckyReceiptModal :isOpen="isLuckyReceiptModalOpen" :orderId="selectedOrderId" @close="closeLuckyReceiptModal" />
    </div>
  </div>
</template>

<script>
import PaymentModal from './PaymentModal.vue';
import PointsPaymentModal from './PointsPaymentModal.vue';
import LuckyReceiptModal from './LuckyReceiptModal.vue';

export default {
  name: 'OrdersPage',
  components: {
    PaymentModal,
    PointsPaymentModal,
    LuckyReceiptModal,
  },
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
      isPaymentModalOpen: false,
      isPointsPaymentModalOpen: false,
      isLuckyReceiptModalOpen: false,
      selectedOrderId: null,
      loading: true,
    };
  },
  watch: {
    orders: {
      immediate: true,
      handler(newOrders) {
        if (newOrders && newOrders.length > 0) {
          this.fetchBakeryNames();
          this.fetchDrinkNames();
          this.fetchShopAddresses();
          this.fetchUserDetails();
        }
      }
    }
  },
  methods: {
    openPaymentModal(orderId) {
      this.selectedOrderId = orderId;
      this.isPaymentModalOpen = true;
    },
    closePaymentModal() {
      this.isPaymentModalOpen = false;
      this.selectedOrderId = null;
    },
    openPointsPaymentModal(orderId) {
      this.selectedOrderId = orderId;
      this.isPointsPaymentModalOpen = true;
    },
    closePointsPaymentModal() {
      this.isPointsPaymentModalOpen = false;
    },
    openLuckyReceiptModal(orderId) {
      this.selectedOrderId = orderId;
      this.isLuckyReceiptModalOpen = true;
    },
    closeLuckyReceiptModal() {
      this.isLuckyReceiptModalOpen = false;
    },
    getStatusDisplayText(status) {
      const statusMap = {
        pending: 'в обробці',
        paid: 'оплачено',
        finished: 'завершено',
      };
      return statusMap[status] || status;
    },
    async fetchBakeryNames() {
      const bakeryIds = [...new Set(this.orders.flatMap(order => {
        return order.bakeryItems.map(item => item.bakery_id);
      }))];

      if (bakeryIds.length === 0) {
        return;
      }

      const requestBody = {bakery_ids: bakeryIds};

      try {
        const response = await fetch('http://localhost:5000/api/bakery-names', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });

        if (response.ok) {
          const data = await response.json();
          this.bakeryNames = data;
        } else {
          const errorText = await response.text();
          console.error('Error response:', errorText);
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
    async fetchDrinkNames() {
      const drinkIds = [...new Set(this.orders.flatMap(order => {
        return order.drinkItems.map(item => item.drink_id);
      }))];

      if (drinkIds.length === 0) {
        return;
      }

      const requestBody = {drink_ids: drinkIds};

      try {
        const response = await fetch('http://localhost:5000/api/drink-names', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });

        if (response.ok) {
          const data = await response.json();
          this.drinkNames = data;
        } else {
          const errorText = await response.text();
          console.error('Error response:', errorText);
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
    async fetchShopAddresses() {
      const shopIds = [...new Set(this.orders.map(order => order.shop_id))];

      if (shopIds.length === 0) {
        return;
      }

      const requestBody = {shop_ids: shopIds};

      try {
        const response = await fetch('http://localhost:5000/api/shop-addresses', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });

        if (response.ok) {
          const data = await response.json();
          this.shopAddresses = data;
        } else {
          const errorText = await response.text();
          console.error('Error response:', errorText);
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
    async fetchUserDetails() {
      const userIds = [...new Set(this.orders.map(order => order.user_id))];

      if (userIds.length === 0) {
        return;
      }

      const requestBody = {user_ids: userIds};

      try {
        const response = await fetch('http://localhost:5000/api/user-details', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });

        if (response.ok) {
          const data = await response.json();
          this.userDetails = data;
        } else {
          const errorText = await response.text();
          console.error('Error response:', errorText);
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
    async updateOrderStatus(orderId, newStatus) {
      try {
        const response = await fetch(`http://localhost:5000/api/update-order-status/${orderId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({status: newStatus}),
        });

        if (response.ok) {
          alert('Order status updated successfully');
        } else {
          const errorText = await response.text();
          console.error('Error response:', errorText);
          alert('Failed to update order status');
        }
      } catch (error) {
        console.error('Fetch error:', error);
        alert('Failed to update order status');
      }
    },
  },
  mounted() {
    setTimeout(() => {
      this.loading = false;
    }, 3000);
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

.orders-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Roboto', sans-serif;
}

h2 {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 20px;
  text-align: center;
}

.order-card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.order-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

h3 {
  font-size: 22px;
  color: #34495e;
  margin-bottom: 10px;
}

p {
  font-size: 16px;
  color: #666;
  margin: 5px 0;
}

.status-pending {
  color: #e67e22;
}

.status-paid {
  color: #27ae60;
}

.status-finished {
  color: #95a5a6;
}

.order-section {
  margin-top: 20px;
}

h4 {
  font-size: 18px;
  color: #34495e;
  margin-bottom: 10px;
}

.order-table {
  width: 100%;
  border-collapse: collapse;
  margin: 10px 0;
}

.order-table th, .order-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

.order-table th {
  background-color: #f8f9fa;
  font-weight: 500;
}

.no-items {
  color: #95a5a6;
  font-style: italic;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.btn-pay {
  background-color: #3498db;
  color: white;
}

.btn-pay:hover {
  background-color: #2980b9;
}

.btn-points {
  background-color: #9b59b6;
  color: white;
}

.btn-points:hover {
  background-color: #8e44ad;
}

.btn-lucky {
  background-color: #2ecc71;
  color: white;
}

.btn-lucky:hover {
  background-color: #27ae60;
}

.no-orders {
  text-align: center;
  color: #95a5a6;
  font-style: italic;
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
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
</style>