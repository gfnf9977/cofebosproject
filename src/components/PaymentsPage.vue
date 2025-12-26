<template>
  <div>
    <h2>Чеки та оплати</h2>
    <div v-if="loading" class="loader-container">
      <div class="coffee-cup">
        <img src="coffeboss.png" alt="Coffeboss" class="coffee-image" />
      </div>
    </div>
    <div v-else>
      <div v-if="filteredOrders.length > 0">
        <div v-for="order in filteredOrders" :key="order.id" class="receipt-wrapper">
          <button class="print-button" @click="printReceipt(order.id)">
            <img src="print.png" alt="Print" class="print-image" />
          </button>
          <div class="order-container">
            <div class="order-details" :ref="`order-${order.id}`">
              <h3 class="company-name">ТОВ "Кофебосс"</h3>
              <p class="address">Чернігівська область, м. Чернігів, Вулиця Вячеслава Чорновола 9, Знаходиться біля готелю "Градецький"</p>
              <hr class="dotted-line" />
              <p class="order-id">Код замовлення: {{ order.id }}</p>
              <p class="customer">Клієнт: {{ userDetails[order.user_id] || 'Unknown' }}</p>
              <p class="order-date">Замовлено: {{ formatDate(order.order_date) }}</p>
              <hr class="dotted-line" />
              <div v-if="order.bakeryItems.length > 0">
                <h4 class="section-title">Випічка</h4>
                <table class="order-table">
                  <thead>
                  <tr>
                    <th class="name-column">Назва випічки</th>
                    <th class="quantity-column">Кількість</th>
                    <th class="price-column">Ціна</th>
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
              <div v-if="order.drinkItems.length > 0">
                <h4 class="section-title">Напої</h4>
                <table class="order-table">
                  <thead>
                  <tr>
                    <th class="name-column">Назва напою</th>
                    <th class="size-column">Розмір</th>
                    <th class="quantity-column">Кількість</th>
                    <th class="price-column">Ціна</th>
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
              <hr class="dotted-line" />
              <p class="total-price">Всього до сплати: {{ order.total_price }} грн</p>
              <hr class="dotted-line" />
              <div v-if="paymentDetails[order.id]?.payments_date && paymentDetails[order.id]?.card_number">
                <p class="payment-date">Сплачено: {{ formatDate(paymentDetails[order.id]?.payments_date) }}</p>
                <p class="card-number">Номер карти: {{ formatCardNumber(paymentDetails[order.id]?.card_number) }}</p>
              </div>
              <div v-else>
                <p class="payment-method">Сплачено: {{ getPaymentMethod(order.id) }}</p>
              </div>
              <hr class="dotted-line" />
              <div v-if="generatedCodes[order.id]">
                <p class="lucky-message">Вітаємо! Цей чек щасливий! Вам надано спеціальний код, що надає право на безкоштовне замовлення. Просто зробіть оформлення та оберіть використати код:)</p>
                <p class="lucky-code">Ваш щасливий код: <strong>{{ generatedCodes[order.id] }}</strong></p>
                <button class="copy-button" @click="copyCode(generatedCodes[order.id])">Скопіювати код</button>
              </div>
              <div v-else-if="order.id % 46 === 0">
                <button class="generate-button" @click="generateCode(order.id)">Сформувати код</button>
              </div>
              <hr class="dotted-line" />
              <div class="qr-code-container">
                <img src="RUSOYOB.png" alt="Coffeboss QR" class="qr-code-image" />
                <p class="fiscal-receipt">*****ФІСКАЛЬНИЙ ЧЕК*****</p>
                <p class="order-year">{{ getOrderYear(order.order_date) }}</p>
              </div>
            </div>
          </div>
          <button class="download-button" @click="downloadReceipt(order.id)">
            <img src="download.png" alt="Download" class="download-image" />
          </button>
        </div>
      </div>
      <div v-else>
        <p>Немає замовлень.</p>
      </div>
    </div>
  </div>
</template>

<script>
import html2canvas from 'html2canvas';

export default {
  name: 'PaymentsPage',
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
      paymentDetails: {},
      generatedCodes: {},
      loading: true, // Додано стан завантаження
    };
  },
  computed: {
    filteredOrders() {
      return this.orders.filter(order => order.status === 'finished');
    }
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
          this.fetchPaymentDetails();
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
    generateCode(orderId) {
      if (orderId % 46 === 0 && !this.generatedCodes[orderId]) {
        const code = this.generateRandomCode();
        this.saveCodeToDatabase(orderId, code);
      }
    },
    generateRandomCode(length = 10) {
      const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      let result = '';
      const charactersLength = characters.length;
      for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
      }
      return result;
    },
    async saveCodeToDatabase(orderId, code) {
      try {
        const response = await fetch('http://localhost:5000/api/generate-code', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ order_id: orderId, code: code }),
        });

        if (response.ok) {
          this.generatedCodes[orderId] = code;
        } else {
          const data = await response.json();
          if (data.error === 'Code already generated for this order') {
            alert('Code already generated for this order');
          } else {
            console.error('Failed to save code to database');
          }
        }
      } catch (error) {
        console.error('Error saving code to database:', error);
      }
    },
    async copyCode(code) {
      try {
        await navigator.clipboard.writeText(code);
        alert('Code copied to clipboard!');
      } catch (err) {
        console.error('Failed to copy code: ', err);
      }
    },
    async fetchBakeryNames() {
      const bakeryIds = [...new Set(this.filteredOrders.flatMap(order =>
          order.bakeryItems.map(item => item.bakery_id)
      ))];

      if (bakeryIds.length === 0) return;

      try {
        const response = await fetch('http://localhost:5000/api/bakery-names', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ bakery_ids: bakeryIds }),
        });

        if (response.ok) {
          this.bakeryNames = await response.json();
        }
      } catch (error) {
        console.error('Fetch bakery names error:', error);
      }
    },
    async fetchDrinkNames() {
      const drinkIds = [...new Set(this.filteredOrders.flatMap(order =>
          order.drinkItems.map(item => item.drink_id)
      ))];

      if (drinkIds.length === 0) return;

      try {
        const response = await fetch('http://localhost:5000/api/drink-names', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ drink_ids: drinkIds }),
        });

        if (response.ok) {
          this.drinkNames = await response.json();
        }
      } catch (error) {
        console.error('Fetch drink names error:', error);
      }
    },
    async fetchShopAddresses() {
      const shopIds = [...new Set(this.filteredOrders.map(order => order.shop_id))];

      if (shopIds.length === 0) return;

      try {
        const response = await fetch('http://localhost:5000/api/shop-addresses', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ shop_ids: shopIds }),
        });

        if (response.ok) {
          this.shopAddresses = await response.json();
        }
      } catch (error) {
        console.error('Fetch shop addresses error:', error);
      }
    },
    async fetchUserDetails() {
      const userIds = [...new Set(this.filteredOrders.map(order => order.user_id))];

      if (userIds.length === 0) return;

      try {
        const response = await fetch('http://localhost:5000/api/user-details', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ user_ids: userIds }),
        });

        if (response.ok) {
          this.userDetails = await response.json();
        }
      } catch (error) {
        console.error('Fetch user details error:', error);
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
            this.paymentDetails[orderId] = await response.json();
          }

          // Fetch the generated code for the order
          const codeResponse = await fetch(`http://localhost:5000/api/get-generated-code/${orderId}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          });

          if (codeResponse.ok) {
            const codeData = await codeResponse.json();
            if (codeData.code) {
              this.generatedCodes[orderId] = codeData.code;
            }
          }
        } catch (error) {
          console.error(`Fetch payment details for order ${orderId} error:`, error);
        }
      }
    },
    getPaymentMethod(orderId) {
      // Logic to determine the payment method based on orderId
      const paymentDetail = this.paymentDetails[orderId];
      if (paymentDetail && paymentDetail.card_number) {
        return 'Карткою';
      }
      return 'Оплачено з допомогою бонусних балів/готівкою чи за допомогою послуги щасливий чек';
    },
    getOrderStatus(status) {
      switch (status) {
        case 'pending':
          return 'в обробці';
        case 'paid':
          return 'оплачено';
        case 'finished':
          return 'завершено';
        default:
          return status;
      }
    },
    async downloadReceipt(orderId) {
      const element = this.$refs[`order-${orderId}`][0];
      const canvas = await html2canvas(element);
      const dataURL = canvas.toDataURL('image/png');
      const link = document.createElement('a');
      link.href = dataURL;
      link.download = `receipt_${orderId}.png`;
      link.click();
    },
    printReceipt(orderId) {
      const element = this.$refs[`order-${orderId}`][0];
      const printWindow = window.open('', '_blank');
      printWindow.document.write('<html><head><title>Print Receipt</title></head><body>');
      printWindow.document.write(element.innerHTML);
      printWindow.document.write('</body></html>');
      printWindow.document.close();
      printWindow.print();
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
      const year = date.getFullYear();
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${day}.${month}.${year} ${hours}:${minutes}`;
    },
    getOrderYear(dateString) {
      const date = new Date(dateString);
      return date.getFullYear();
    }
  },
  mounted() {
    // Імітація завантаження даних
    setTimeout(() => {
      this.loading = false;
    }, 3000);
  },
};
</script>

<style scoped>
h2 {
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.receipt-wrapper {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  margin-bottom: 40px; /* Increased spacing */
}

.order-container {
  flex: 1;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 400px; /* Set a fixed width for the container */
}

.order-details {
  width: 100%;
  text-align: left;
}

.company-name, .address {
  font-size: 1.2em;
  font-weight: bold;
  text-align: center;
  margin-bottom: 10px;
}

.order-id, .customer, .order-date {
  font-size: 1em;
  margin: 5px 0;
}

.section-title {
  font-size: 1.2em;
  font-weight: bold;
  margin-top: 20px;
}

.order-table {
  width: 100%;
  border-collapse: collapse;
  margin: 10px 0;
}

.order-table th, .order-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.order-table th {
  background-color: #f2f2f2;
}

.order-table .name-column {
  width: 40%; /* Adjust the width of the name column */
}

.order-table .quantity-column {
  width: 20%; /* Adjust the width of the quantity column */
}

.order-table .price-column {
  width: 20%; /* Adjust the width of the price column */
}

.order-table .size-column {
  width: 20%; /* Adjust the width of the size column */
}

.total-price {
  text-align: right;
  font-weight: bold;
  font-size: 1.2em;
  margin-top: 20px;
}

.payment-date, .card-number, .payment-method {
  font-size: 1em;
  margin: 5px 0;
}

.lucky-message {
  color: #4CAF50;
  font-weight: bold;
  text-align: center;
  font-size: 1.2em;
  margin-top: 20px;
}

.lucky-code {
  text-align: center;
  font-size: 1em;
  margin-top: 10px;
}

.copy-button, .generate-button {
  margin-top: 10px;
  padding: 5px 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.copy-button:hover, .generate-button:hover {
  background-color: #45a049;
}

.dotted-line {
  border: none;
  border-top: 1px dotted #ddd;
  margin: 20px 0;
}

.qr-code-container {
  text-align: center;
  margin-top: 20px;
}

.qr-code-image {
  width: 150px;
  height: 150px;
  object-fit: contain;
}

.fiscal-receipt {
  font-weight: bold;
  margin-top: 10px;
  font-size: 1.2em;
}

.order-year {
  font-size: 1em;
  margin-top: 5px;
}

.download-button {
  margin-left: 20px;
  padding: 0;
  background: none;
  border: none;
  cursor: pointer;
}

.download-image {
  width: 100px;
  height: 100px;
  object-fit: contain;
}

.print-button {
  margin-right: 20px;
  padding: 0;
  background: none;
  border: none;
  cursor: pointer;
}

.print-image {
  width: 100px;
  height: 100px;
  object-fit: contain;
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