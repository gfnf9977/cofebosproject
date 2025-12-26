<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <h2>Замовлення</h2>
      <form @submit.prevent="submitOrder">
        <div class="form-group">
          <label for="contactName">Контактна особа:</label>
          <input type="text" id="contactName" v-model="contactName" required />
        </div>
        <div class="form-group">
          <label for="contactPhone">Контактний номер телефону:</label>
          <input type="tel" id="contactPhone" v-model="contactPhone" required />
        </div>
        <div class="form-group">
          <label for="deliveryMethod">Спосіб доставки:</label>
          <div class="custom-select" @click="toggleDropdown">
            <div class="selected-option">
              <img v-if="deliveryMethod === 'НоваПошта'" src="/novapost.png" alt="НоваПошта" class="option-image" />
              <img v-if="deliveryMethod === 'Кав\'ярня'" src="/coffeboss.png" alt="Кав'ярня" class="option-image" />
              {{ deliveryMethod || 'Оберіть спосіб доставки' }}
            </div>
            <div class="dropdown-options" v-if="isDropdownOpen">
              <div class="dropdown-option" @click="selectDeliveryMethod('НоваПошта')">
                <img src="/novapost.png" alt="НоваПошта" class="option-image" />
                НоваПошта
              </div>
              <div class="dropdown-option" @click="selectDeliveryMethod('Кав\'ярня')">
                <img src="/coffeboss.png" alt="Кав'ярня" class="option-image" />
                Кав'ярня
              </div>
            </div>
          </div>
        </div>
        <div class="form-group" v-if="deliveryMethod === 'НоваПошта'">
          <label for="deliveryOption">Тип доставки:</label>
          <button type="button" class="nova-poshta-btn" @click="openNovaPoshtaModal">Вибрати тип доставки</button>
          <span v-if="deliveryOption" class="delivery-option">{{ deliveryOption }}</span>
        </div>
        <div class="form-group" v-if="deliveryMethod === 'Кав\'ярня'">
          <label for="cafeAddress">Адреса кофебоса:</label>
          <select id="cafeAddress" v-model="cafeAddress" required>
            <option value="">Оберіть адресу кав'ярні</option>
            <option v-for="store in stores" :key="store.id" :value="`${store.Street}, ${store.nomer}`">
              {{ store.Street }}, {{ store.nomer }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="orderDetails">Замовлення:</label>
          <textarea id="orderDetails" v-model="orderDetails" readonly></textarea>
        </div>
        <button type="submit" class="submit-btn" :disabled="!hasEnoughPoints">Сплатити 30 балів</button>
      </form>
      <button class="close-btn" @click="closeModal">Закрити</button>
    </div>

    <div class="nova-poshta-modal" v-if="isNovaPoshtaModalOpen">
      <div class="nova-poshta-content">
        <h3>Виберіть тип доставки</h3>
        <div class="form-group">
          <label>
            <input type="radio" v-model="deliveryOption" value="Поштомат" @change="updateDeliveryFields" />
            Поштомат
          </label>
          <label>
            <input type="radio" v-model="deliveryOption" value="Відділення" @change="updateDeliveryFields" />
            Відділення
          </label>
          <label>
            <input type="radio" v-model="deliveryOption" value="Адресна доставка" @change="updateDeliveryFields" />
            Адресна доставка
          </label>
        </div>
        <div class="form-group">
          <label for="city">Населений пункт:</label>
          <input type="text" id="city" v-model="city" required />
        </div>
        <div class="form-group" v-if="deliveryOption === 'Відділення' && city === 'Чернігів'">
          <label for="branchNumber">Номер відділення:</label>
          <select id="branchNumber" v-model="branchNumber" required>
            <option v-for="num in branchNumbers" :key="num" :value="num">{{ num }}</option>
          </select>
        </div>
        <div class="form-group" v-if="deliveryOption === 'Відділення' && city !== 'Чернігів'">
          <label for="branchNumber">Номер відділення:</label>
          <input type="text" id="branchNumber" v-model="branchNumber" maxlength="3" pattern="\d{3}" required />
        </div>
        <div class="form-group" v-if="deliveryOption === 'Поштомат'">
          <label for="postomatNumber">Номер поштомату:</label>
          <input type="text" id="postomatNumber" v-model="postomatNumber" maxlength="7" pattern="\d{7}" required />
        </div>
        <div class="form-group" v-if="deliveryOption === 'Адресна доставка'">
          <label for="address">Адреса:</label>
          <input type="text" id="address" v-model="address" required />
        </div>
        <button class="confirm-btn" @click="closeNovaPoshtaModal">Підтвердити</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ShopperPay',
  props: {
    orderItem: {
      type: String,
      required: true,
    },
    userId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      contactName: '',
      contactPhone: '',
      deliveryMethod: '',
      deliveryOption: '',
      cafeAddress: '',
      city: 'Чернігів',
      branchNumber: '',
      postomatNumber: '',
      address: '',
      orderDetails: this.orderItem,
      isNovaPoshtaModalOpen: false,
      branchNumbers: [
        ...Array.from({ length: 31 }, (_, i) => i + 1).filter(num => ![8, 11, 17, 23].includes(num)),
        '10129',
        '953',
        '50710',
        '50708',
        '50436',
        '50709',
        '10130',
        '51158',
        '50435',
        '50707',
        '10128',
        '50351'
      ],
      stores: [],
      userPoints: 0, // Initialize user points
      isDropdownOpen: false,
    };
  },
  async mounted() {
    try {
      const response = await fetch('http://localhost:5000/api/shops'); // Змініть URL за потреби
      if (response.ok) {
        this.stores = await response.json();
      } else {
        console.error('Помилка завантаження даних:', response.statusText);
      }

      // Fetch user points
      const pointsResponse = await fetch(`http://localhost:5000/api/user-points/${this.userId}`);
      if (pointsResponse.ok) {
        const data = await pointsResponse.json();
        this.userPoints = data.points;
      } else {
        console.error('Помилка завантаження балів:', pointsResponse.statusText);
      }
    } catch (error) {
      console.error('Помилка підключення до API:', error);
    }
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
    async submitOrder() {
      if (!this.hasEnoughPoints) {
        alert('Недостатньо балів для замовлення');
        return;
      }

      const orderData = {
        personality: this.contactName,
        number: this.contactPhone,
        type_delivery: this.deliveryMethod,
        deliveryOption: this.deliveryOption,
        city: this.city,
        branchNumber: this.branchNumber,
        postomatNumber: this.postomatNumber,
        address: this.address,
        cafeAddress: this.cafeAddress,
        orderDetails: this.orderDetails,
      };

      try {
        await this.updateUserPoints();

        const response = await fetch('http://localhost:5000/api/pointorder', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(orderData),
        });

        if (response.ok) {
          alert('Замовлення успішно створено!');
          this.closeModal();
        } else {
          const errorData = await response.json();
          alert(`Помилка: ${errorData.error}`);

          // If order submission fails, try to refund points
          await this.refundUserPoints();
        }
      } catch (error) {
        console.error('Помилка при відправці замовлення:', error);
        alert('Сталася помилка при відправці замовлення.');

        // If any error occurs, try to refund points
        await this.refundUserPoints();
      }
    },
    async updateUserPoints() {
      const pointsToDeduct = 30; // Number of points to deduct
      try {
        const response = await fetch(`http://localhost:5000/api/update-user-points/${this.userId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({points: pointsToDeduct}),
        });

        if (response.ok) {
          console.log('Points updated successfully');
          this.userPoints -= pointsToDeduct; // Update local points
        } else {
          const errorData = await response.json();
          console.error(`Error updating points: ${errorData.error}`);
        }
      } catch (error) {
        console.error('Error updating points:', error);
      }
    },
    async refundUserPoints() {
      const pointsToRefund = 30; // Number of points to refund
      try {
        const response = await fetch(`http://localhost:5000/api/update-user-points/${this.userId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({points: -pointsToRefund}),
        });

        if (response.ok) {
          console.log('Points refunded successfully');
          this.userPoints += pointsToRefund; // Update local points
        } else {
          const errorData = await response.json();
          console.error(`Error refunding points: ${errorData.error}`);
        }
      } catch (error) {
        console.error('Error refunding points:', error);
      }
    },
    updateDeliveryOptions() {
      if (this.deliveryMethod !== 'НоваПошта') {
        this.deliveryOption = '';
      }
    },
    openNovaPoshtaModal() {
      this.isNovaPoshtaModalOpen = true;
    },
    closeNovaPoshtaModal() {
      this.isNovaPoshtaModalOpen = false;
    },
    updateDeliveryFields() {
      this.branchNumber = '';
      this.postomatNumber = '';
      this.address = '';
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    selectDeliveryMethod(method) {
      this.deliveryMethod = method;
      this.isDropdownOpen = false;
    },
  },
  computed: {
    hasEnoughPoints() {
      return this.userPoints >= 30;
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
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background: #fff;
  padding: 30px;
  border-radius: 15px;
  text-align: center;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  animation: slideIn 0.3s ease;
}

.modal-content h2 {
  margin-bottom: 20px;
  font-size: 28px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #555;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 14px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #007BFF;
  outline: none;
}

.form-group textarea {
  height: 120px;
  resize: vertical;
}

.nova-poshta-btn {
  padding: 12px 24px;
  background-color: #007BFF;
  color: #fff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 16px;
}

.nova-poshta-btn:hover {
  background-color: #0056b3;
}

.delivery-option {
  display: inline-block;
  margin-left: 10px;
  font-size: 16px;
  color: #007BFF;
}

.submit-btn,
.close-btn,
.confirm-btn {
  padding: 14px 28px;
  background-color: #007BFF;
  color: #fff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 16px;
  margin-top: 10px;
}

.submit-btn:hover,
.close-btn:hover,
.confirm-btn:hover {
  background-color: #0056b3;
}

.close-btn {
  background-color: #6c757d;
  margin-left: 10px;
}

.close-btn:hover {
  background-color: #5a6268;
}

.nova-poshta-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001;
  animation: fadeIn 0.3s ease;
}

.nova-poshta-content {
  background: #fff;
  padding: 30px;
  border-radius: 15px;
  text-align: center;
  max-width: 450px;
  width: 100%;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  animation: slideIn 0.3s ease;
}

.nova-poshta-content h3 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.nova-poshta-content .form-group label {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-size: 16px;
  color: #555;
}

.nova-poshta-content .form-group input[type="radio"] {
  margin-right: 10px;
}

.custom-select {
  position: relative;
  display: inline-block;
  width: 100%;
  cursor: pointer;
}

.selected-option {
  display: flex;
  align-items: center;
  padding: 14px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #fff;
  font-size: 16px;
  color: #555;
}

.option-image {
  width: 28px;
  height: 28px;
  margin-right: 10px;
}

.dropdown-options {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #fff;
  z-index: 1002;
}

.dropdown-option {
  display: flex;
  align-items: center;
  padding: 14px;
  border-bottom: 1px solid #ddd;
  cursor: pointer;
  font-size: 16px;
  color: #555;
}

.dropdown-option:last-child {
  border-bottom: none;
}

.dropdown-option:hover {
  background-color: #f0f0f0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    transform: translateY(-20px);
  }
  to {
    transform: translateY(0);
  }
}
</style>