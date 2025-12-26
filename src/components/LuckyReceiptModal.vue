<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="modal">
      <h3>Вітаємо!</h3>
      <p>Вам випав щасливий чек, це дає змогу розрахуватися за замовлення безкоштовно.</p>
      <p>Будь ласка, введіть код щасливого чека:</p>
      <input v-model="luckyReceiptCode" placeholder="Введіть код" />
      <button @click="confirmPayment">Підтвердити оплату</button>
      <button @click="closeModal">Закрити</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LuckyReceiptModal',
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    orderId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      luckyReceiptCode: '',
    };
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
    async confirmPayment() {
      try {
        const response = await fetch('http://localhost:5000/api/verify-lucky-code', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            order_id: this.orderId,
            code: this.luckyReceiptCode,
          }),
        });

        const responseData = await response.json();

        if (response.ok) {
          alert('Payment confirmed successfully');
          this.closeModal();
        } else {
          console.error('Verification failed:', responseData);
          alert(responseData.error || 'Failed to confirm payment');
        }
      } catch (error) {
        console.error('Fetch error:', error);
        alert('Failed to confirm payment');
      }
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  animation: fadeIn 0.3s ease-in-out;
}

.modal {
  background: #ffffff;
  padding: 30px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
}

h3 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #333;
}

p {
  font-size: 1rem;
  color: #555;
}

input {
  margin: 15px 0;
  padding: 12px;
  width: 100%;
  box-sizing: border-box;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

input:focus {
  border-color: #007bff;
  outline: none;
}

button {
  margin: 12px;
  padding: 12px 25px;
  background: linear-gradient(90deg, #007bff, #0056b3);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.2s ease;
}

button:hover {
  background: linear-gradient(90deg, #0056b3, #003f7f);
  transform: translateY(-2px);
}

button:active {
  transform: translateY(2px);
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>
