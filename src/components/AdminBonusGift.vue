<template>
  <div class="container">
    <h2>Бонусні подарунки</h2>
    <div class="orders-container">
      <div v-for="order in pointorders" :key="order.id" class="order-block">
        <h3>Код замовлення: {{ order.id }}</h3>
        <div class="order-info">
          <p v-if="order.personality"><strong>Особа:</strong> {{ order.personality }}</p>
          <p v-if="order.number"><strong>Номер телефону:</strong> {{ order.number }}</p>
          <p v-if="order.type_delivery"><strong>Тип доставки:</strong> {{ order.type_delivery }}</p>
          <p v-if="order.type_delivery === 'НоваПошта'">
            <strong>Опція доставки:</strong>
            <span v-if="order.branchNumber">Відділення {{ order.branchNumber }}</span>
            <span v-if="order.postomatNumber">Поштомат {{ order.postomatNumber }}</span>
          </p>
          <p v-else-if="order.deliveryOption"><strong>Опція доставки:</strong> {{ order.deliveryOption }}</p>
          <p v-if="order.city"><strong>Місто:</strong> {{ order.city }}</p>
          <p v-if="order.cafeAddress"><strong>Адреса кав'ярні:</strong> {{ order.cafeAddress }}</p>
          <p v-if="order.orderDetails"><strong>Товар:</strong> {{ order.orderDetails }}</p>
          <p v-if="order.created_at"><strong>Дата створення:</strong> {{ order.created_at }}</p>
          <p class="status"><strong>Статус:</strong> <span :class="order.status">{{ order.status }}</span></p>
        </div>
        <div class="status-buttons">
          <button class="delivered" @click="updateStatus(order.id, 'доставлено')">Доставлено</button>
          <button class="received" @click="updateStatus(order.id, 'отримано')">Отримано</button>
          <button class="declined" @click="updateStatus(order.id, 'відмова')">Відмова</button>
          <button class="damaged" @click="updateStatus(order.id, 'пошкоджено')">Пошкоджено</button>
          <button class="returned" @click="updateStatus(order.id, 'відправлено назад')">Відправлено назад</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminBonusGift',
  data() {
    return {
      pointorders: []
    };
  },
  mounted() {
    this.fetchPointOrders();
  },
  methods: {
    async fetchPointOrders() {
      try {
        const response = await fetch('http://localhost:5000/api/pointorders');
        if (response.ok) {
          const data = await response.json();
          this.pointorders = data;
        } else {
          console.error('Помилка завантаження бонусних подарунків:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка підключення до API:', error);
      }
    },
    async updateStatus(orderId, newStatus) {
      try {
        const response = await fetch(`http://localhost:5000/api/update-bonus-status/${orderId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ status: newStatus })
        });
        if (response.ok) {
          this.fetchPointOrders();
        } else {
          console.error('Помилка оновлення статусу бонусу:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка підключення до API:', error);
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

h2 {
  color: #222;
  font-size: 28px;
  margin-bottom: 20px;
  font-weight: bold;
}

.orders-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px;
}

.order-block {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.order-block:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.order-info p {
  color: #444;
  font-size: 16px;
  margin: 5px 0;
}

.status {
  font-weight: bold;
  font-size: 18px;
}

.status-buttons {
  margin-top: 15px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
}

.status-buttons button {
  padding: 10px 15px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
  color: white;
}

.delivered {
  background-color: #28a745;
}
.delivered:hover {
  background-color: #218838;
}

.received {
  background-color: #17a2b8;
}
.received:hover {
  background-color: #138496;
}

.declined {
  background-color: #dc3545;
}
.declined:hover {
  background-color: #c82333;
}

.damaged {
  background-color: #ff9800;
}
.damaged:hover {
  background-color: #e68900;
}

.returned {
  background-color: #6c757d;
}
.returned:hover {
  background-color: #5a6268;
}
</style>