<template>
  <div v-if="isOpen" class="modal">
    <div class="modal-content">
      <h3 class="modal-title">Оплата балами</h3>
      <p class="points-info">
        Кількість балів: <strong>{{ points }}</strong>
        <img src="/cardr-removebg-preview.ico" alt="Points Icon" class="points-icon">
      </p>
      <p class="order-amount">Сума замовлення (в балах): <strong>{{ convertedTotalPrice }}</strong></p>
      <div class="button-group">
        <button @click="confirmPayment" class="confirm-btn">Підтвердити оплату</button>
        <button @click="closeModal" class="close-btn">Закрити</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PointsPaymentModal',
  props: {
    isOpen: Boolean,
    userId: Number,
    orderId: Number,
  },
  data() {
    return {
      points: null,
      convertedTotalPrice: null,
    };
  },
  watch: {
    isOpen(newVal) {
      if (newVal) {
        this.fetchUserPoints();
        this.fetchOrderTotalPrice();
      }
    },
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
    async fetchUserPoints() {
      try {
        const response = await fetch(`http://localhost:5000/api/user-points/${this.userId}`);
        if (response.ok) {
          this.points = (await response.json()).points;
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
    async fetchOrderTotalPrice() {
      try {
        const response = await fetch(`http://localhost:5000/api/orders/${this.orderId}`);
        if (response.ok) {
          this.convertedTotalPrice = (await response.json()).converted_total_price;
        } else {
          alert('Не вдалося отримати дані замовлення.');
          this.closeModal();
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    },
    async confirmPayment() {
      if (this.points < this.convertedTotalPrice) {
        alert('Недостатньо балів.');
        return;
      }
      try {
        const response = await fetch('http://localhost:5000/api/record-payment', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            order_id: this.orderId,
            user_id: this.userId,
            payment_method: 'points',
          }),
        });

        if (response.ok) {
          alert('Оплата успішна.');
          this.closeModal();
        } else {
          alert('Помилка оплати.');
        }
      } catch (error) {
        console.error('Fetch error:', error);
        alert('Помилка оплати.');
      }
    },
  },
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  animation: fadeIn 0.3s ease-in-out;
}

.modal-content {
  background: #fff;
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 90%;
  animation: slideIn 0.3s ease-in-out;
}

.modal-title {
  font-size: 22px;
  margin-bottom: 15px;
  color: #333;
}

.points-info,
.order-amount {
  font-size: 18px;
  margin: 10px 0;
}

.points-icon {
  width: 28px;
  height: 28px;
  vertical-align: middle;
  margin-left: 8px;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

button {
  padding: 12px 20px;
  font-size: 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s;
}

.confirm-btn {
  background: #28a745;
  color: white;
  box-shadow: 0px 4px 10px rgba(40, 167, 69, 0.3);
}

.confirm-btn:hover {
  background: #218838;
}

.close-btn {
  background: #dc3545;
  color: white;
  box-shadow: 0px 4px 10px rgba(220, 53, 69, 0.3);
}

.close-btn:hover {
  background: #c82333;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from { transform: translateY(-20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
