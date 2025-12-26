<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="card-form-container">
      <div class="card">
        <form class="card-form" @submit.prevent="confirmPayment">
          <div class="input-group">
            <label for="cardNumber">Номер картки</label>
            <input
                type="text"
                id="cardNumber"
                v-model="cardNumber"
                class="form-control"
                required
                placeholder="XXXX XXXX XXXX XXXX"
                pattern="\d{4} \d{4} \d{4} \d{4}"
                maxlength="19"
                @input="formatCardNumber"
            />
          </div>
          <div class="flex-row">
            <div class="input-group half">
              <label for="expirationDate">Термін дії</label>
              <input
                  type="text"
                  id="expirationDate"
                  v-model="expirationDate"
                  class="form-control"
                  required
                  placeholder="MM/YY"
                  pattern="\d{2}/\d{2}"
                  maxlength="5"
                  @input="formatExpirationDate"
              />
            </div>
            <div class="input-group half">
              <label for="cvv">CVV</label>
              <input
                  type="text"
                  id="cvv"
                  v-model="cvv"
                  class="form-control"
                  required
                  placeholder="XXX"
                  pattern="\d{3}"
                  maxlength="3"
              />
            </div>
          </div>
          <button type="submit" class="btn-primary">Підтвердити оплату</button>
          <button type="button" @click="closeModal" class="btn-secondary">Закрити</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PaymentModal',
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    orderId: {
      type: Number,
      required: true,
    },
    userId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      cardNumber: '',
      expirationDate: '',
      cvv: '',
    };
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
    formatCardNumber() {
      this.cardNumber = this.cardNumber.replace(/\D/g, '').match(/.{1,4}/g)?.join(' ') || '';
    },
    formatExpirationDate() {
      this.expirationDate = this.expirationDate.replace(/\D/g, '').replace(/(\d{2})(?=\d)/, '$1/');
    },
    async confirmPayment() {
      try {
        const response = await fetch('http://localhost:5000/api/record-payment', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            order_id: this.orderId,
            user_id: this.userId,
            card_number: this.cardNumber.replace(/\s+/g, ''),
            expiration_date: this.expirationDate,
            cvv: this.cvv,
          }),
        });

        if (response.ok) {
          alert('Payment recorded successfully');
          this.closeModal();
        } else {
          const errorText = await response.text();
          console.error('Error response:', errorText);
          alert('Failed to record payment');
        }
      } catch (error) {
        console.error('Fetch error:', error);
        alert('Failed to record payment');
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
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-form-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  background: #ffffff;
  border-radius: 15px;
  padding: 20px;
  width: 350px;
  height: 270px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  color: #333333;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.input-group label {
  font-weight: bold;
  font-size: 12px;
  color: #333333;
}

.input-group input {
  padding: 10px;
  border: 1px solid #cccccc;
  border-radius: 5px;
  font-size: 16px;
  outline: none;
  background: #f9f9f9;
  color: #333333;
}

.input-group input::placeholder {
  color: #999999;
}

.flex-row {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.half {
  width: 48%;
}

button {
  padding: 10px;
  background-color: #333333;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #555555;
}

.btn-secondary {
  background-color: #6c757d;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>
