<template>
  <div>
    <h2>Замовлення</h2>
    <div v-if="loading" class="loader-container">
      <div class="loader"></div>
    </div>
    <div v-else>
      <div v-if="filteredOrders.length > 0">
        <div v-for="order in filteredOrders" :key="order.id" class="order-details">
          <h3>Код замовлення: {{ order.id }}</h3>
          <p>Клієнт: {{ userDetails[order.user_id] || 'Unknown' }}</p>
          <p>Адреса кав'ярні: {{ shopAddresses[order.shop_id] || 'Unknown' }}</p>
          <p>Статус: {{ translateStatus(order.status) }}</p>
          <p>Вартість: {{ order.total_price }} грн</p>
          <p>Замовлено: {{ order.order_date }}</p>

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

          <div class="status-update">
            <label for="status">Змінити статус:</label>
            <select id="status" v-model="order.status" @change="updateOrderStatus(order.id, order.status)">
              <option value="pending">Pending</option>
              <option value="paid">Paid</option>
              <option value="finished">Finished</option>
            </select>
          </div>
        </div>
      </div>
      <div v-else>
        <p>Немає замовлень для цієї кав'ярні.</p>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'OrdersAdmin',
  props: {
    userId: {
      type: Number,
      required: true,
    },
    shopId: {
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
      loading: false,
    };
  },
  computed: {
    filteredOrders() {
      return this.orders.filter(order => order.shop_id === this.shopId);
    },
  },
  watch: {
    orders: {
      immediate: true,
      async handler(newOrders) {
        if (newOrders && newOrders.length > 0) {
          this.loading = true;
          await Promise.all([
            this.fetchBakeryNames(),
            this.fetchDrinkNames(),
            this.fetchShopAddresses(),
            this.fetchUserDetails(),
          ]);
          this.loading = false;
        }
      }
    }
  },
  methods: {
    translateStatus(status) {
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
          body: JSON.stringify({ status: newStatus }),
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
};
</script>

<style scoped>
h2 {
  color: #333;
}

p {
  color: #666;
}

.order-details {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

h3 {
  margin-top: 0;
}

h4 {
  margin-top: 15px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

.status-update {
  margin-top: 20px;
}

.status-update label {
  margin-right: 10px;
}

.status-update select {
  padding: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
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
