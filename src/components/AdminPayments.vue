<template>
  <div class="admin-payments">
    <h2>Чеки та оплати</h2>
    <div v-if="loading" class="loader-container">
      <div class="loader"></div>
    </div>
    <div v-else>
      <div v-if="filteredOrders.length > 0">
        <div v-for="order in filteredOrders" :key="order.id" class="order-details">
          <h3>Код замовлення: {{ order.id }}</h3>
          <p>Замовник: {{ userDetails[order.user_id] || 'Unknown' }}</p>
          <p>Адреса кав'ярні: {{ shopAddresses[order.shop_id] || 'Unknown' }}</p>
          <p>Вартість: {{ order.total_price }} грн</p>
          <p>Замовлено: {{ order.order_date }}</p>

          <!-- Conditional rendering for payment details -->
          <div v-if="paymentDetails[order.id] && paymentDetails[order.id].payments_date && paymentDetails[order.id].card_number">
            <p>Оплачено: {{ paymentDetails[order.id].payments_date }}</p>
            <p>Номер карти: {{ formatCardNumber(paymentDetails[order.id].card_number) }}</p>
          </div>
          <div v-else>
            <p>Метод оплати: {{ getPaymentMethod(order) }}</p>
          </div>

          <h4>Випічка</h4>
          <div v-if="order.bakeryItems.length > 0">
            <table>
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
            <p>Немає випічки у цьому замовленні.</p>
          </div>

          <h4>Напої</h4>
          <div v-if="order.drinkItems.length > 0">
            <table>
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
            <p>Немає напоїв у цьому замовленні.</p>
          </div>
        </div>
      </div>
      <div v-else>
        <p>Немає замовлень зі статусом 'finished'.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminPayments',
  props: {
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
      paymentDetails: {},
      loading: true, // Add loading state
    };
  },
  computed: {
    filteredOrders() {
      return this.orders && this.orders.length > 0 ? this.orders.filter(order => order.status === 'finished') : [];
    }
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
    formatCardNumber(cardNumber) {
      if (!cardNumber) return 'N/A';
      const last4Digits = cardNumber.slice(-4);
      const maskedPart = 'xxxx xxxx xxxx';
      return `${maskedPart} ${last4Digits}`;
    },
    getPaymentMethod(order) {
      const paymentDetails = this.paymentDetails[order.id];
      if (!paymentDetails || (!paymentDetails.payments_date && !paymentDetails.card_number)) {
        return 'Оплачено бонусними картками, готівкою чи через послугу щасливий чек';
      }
      return '';
    },
    async fetchData() {
      this.loading = true; // Start loading
      await Promise.all([
        this.fetchBakeryNames(),
        this.fetchDrinkNames(),
        this.fetchShopAddresses(),
        this.fetchUserDetails(),
        this.fetchPaymentDetails(),
      ]);
      this.loading = false; // Stop loading
    },
    async fetchBakeryNames() {
      const bakeryIds = [...new Set(this.filteredOrders.flatMap(order => {
        return order.bakeryItems.map(item => item.bakery_id);
      }))];

      if (bakeryIds.length === 0) return;

      const requestBody = { bakery_ids: bakeryIds };

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
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
    async fetchDrinkNames() {
      const drinkIds = [...new Set(this.filteredOrders.flatMap(order => {
        return order.drinkItems.map(item => item.drink_id);
      }))];

      if (drinkIds.length === 0) return;

      const requestBody = { drink_ids: drinkIds };

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
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
    async fetchShopAddresses() {
      const shopIds = [...new Set(this.filteredOrders.map(order => order.shop_id))];

      if (shopIds.length === 0) return;

      const requestBody = { shop_ids: shopIds };

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
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
    async fetchUserDetails() {
      const userIds = [...new Set(this.filteredOrders.map(order => order.user_id))];

      if (userIds.length === 0) return;

      const requestBody = { user_ids: userIds };

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
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
    async fetchPaymentDetails() {
      const orderIds = this.filteredOrders.map(order => order.id);

      if (orderIds.length === 0) return;

      for (const orderId of orderIds) {
        try {
          const response = await fetch(`http://localhost:5000/api/payments/${orderId}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          });

          if (response.ok) {
            const data = await response.json();
            this.paymentDetails[orderId] = data;
          }
        } catch (error) {
          console.error('Fetch error:', error);
        }
      }
    },
  },
};
</script>

<style scoped>
.admin-payments {
  font-family: 'Arial', sans-serif;
  padding: 20px;
  background-color: #f4f4f4;
}

h2 {
  color: #333;
  font-size: 24px;
  margin-bottom: 20px;
}

.order-details {
  margin-bottom: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h3 {
  margin-top: 0;
  color: #444;
  font-size: 20px;
}

h4 {
  margin-top: 15px;
  color: #555;
  font-size: 18px;
}

p {
  color: #666;
  font-size: 16px;
  margin: 5px 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 10px 0;
  font-size: 14px;
}

th, td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
  font-weight: bold;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1f1f1;
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