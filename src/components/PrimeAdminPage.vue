<template>
  <div>
    <div class="header">
      <p v-if="fullName">Вітаємо, {{ fullName }}!</p>
    </div>
    <div class="tabs">
      <button :class="{ active: activeTab === 'home' }" @click="setActiveTab('home')">Головна</button>
      <button :class="{ active: activeTab === 'menu' }" @click="setActiveTab('menu')">Меню</button>
      <button :class="{ active: activeTab === 'vacancies' }" @click="setActiveTab('vacancies')">Вакансії</button>
      <button :class="{ active: activeTab === 'staff' }" @click="setActiveTab('staff')">Працівники</button>
      <button :class="{ active: activeTab === 'schedule' }" @click="setActiveTab('schedule')">Графік роботи</button>
      <button :class="{ active: activeTab === 'guests' }" @click="setActiveTab('guests')">Гості</button>
      <button :class="{ active: activeTab === 'payments' }" @click="setActiveTab('payments')">Оплати</button>
      <button :class="{ active: activeTab === 'orders' }" @click="setActiveTab('orders')">Замовлення</button>
      <button :class="{ active: activeTab === 'stores' }" @click="setActiveTab('stores')">Заклади</button>
      <button :class="{ active: activeTab === 'gallery' }" @click="setActiveTab('gallery')">Галерея</button>
      <button :class="{ active: activeTab === 'profile' }" @click="setActiveTab('profile')">Профіль</button>
      <button :class="{ active: activeTab === 'chats' }" @click="setActiveTab('chats')">Чати</button>
      <button :class="{ active: activeTab === 'bonusGifts' }" @click="setActiveTab('bonusGifts')">Бонусні подарунки</button>
    </div>
    <div class="tab-content">
      <div v-if="activeTab === 'home'">
        <HomePage />
      </div>
      <div v-if="activeTab === 'menu'">
        <MenuGrand />
      </div>
      <div v-if="activeTab === 'vacancies'">
        <PrimeVacancies />
      </div>
      <div v-if="activeTab === 'staff'">
        <StaffPage />
      </div>
      <div v-if="activeTab === 'schedule'">
        <PrimeScheduleAdminPage />
      </div>
      <div v-if="activeTab === 'guests'">
        <GuestsPage />
      </div>
      <div v-if="activeTab === 'payments'">
        <AdminPayments :orders="detailedOrders" />
      </div>
      <div v-if="activeTab === 'orders'">
        <OrdersPrime :userId="userId" :orders="detailedOrders" />
      </div>
      <div v-if="activeTab === 'stores'">
        <StoresPage />
      </div>
      <div v-if="activeTab === 'gallery'">
        <GalleryEdit />
      </div>
      <div v-if="activeTab === 'profile'">
        <ProfileFitches :username="username" />
      </div>
      <div v-if="activeTab === 'chats'">
        <PrimeConnect />
      </div>
      <div v-if="activeTab === 'bonusGifts'">
        <PrimeBonusGift />
      </div>
    </div>
  </div>
</template>

<script>
import HomePage from './HomePage.vue';
import ProfileFitches from './ProfileFitches.vue';
import StaffPage from './StaffPage.vue';
import GuestsPage from './GuestsPage.vue';
import StoresPage from './StoresPage.vue';
import MenuGrand from './MenuGrand.vue';
import OrdersPrime from './OrdersPrime.vue';
import AdminPayments from './AdminPayments.vue';
import PrimeVacancies from './PrimeVacancies.vue';
import PrimeScheduleAdminPage from './PrimeScheduleAdminPage.vue';
import GalleryEdit from './GalleryEdit.vue';
import PrimeConnect from './PrimeConnect.vue';
import PrimeBonusGift from './PrimeBonusGift.vue';

export default {
  name: 'PrimeAdminPage',
  components: {
    HomePage,
    ProfileFitches,
    StaffPage,
    GuestsPage,
    StoresPage,
    MenuGrand,
    OrdersPrime,
    AdminPayments,
    PrimeVacancies,
    PrimeScheduleAdminPage,
    GalleryEdit,
    PrimeConnect,
    PrimeBonusGift,
  },
  data() {
    return {
      activeTab: 'home',
      username: '',
      fullName: '',
      userId: null,
      orders: [],
      detailedOrders: [],
    };
  },
  async mounted() {
    try {
      const username = localStorage.getItem('username');
      if (username) {
        this.username = username;
        const response = await fetch(`http://localhost:5000/api/user-profile?username=${username}`);
        if (response.ok) {
          const userData = await response.json();
          this.fullName = `${userData.last_name} ${userData.first_name} ${userData.middle_name}`;
        } else {
          console.error('Помилка завантаження даних користувача:', response.statusText);
        }
        const userIdResponse = await fetch(`http://localhost:5000/api/user-id?username=${username}`);
        if (userIdResponse.ok) {
          const userIdData = await userIdResponse.json();
          this.userId = userIdData.id;
        } else {
          console.error('Помилка завантаження ID користувача:', userIdResponse.statusText);
        }
        // Fetch the orders data
        const ordersResponse = await fetch('http://localhost:5000/api/orders');
        if (ordersResponse.ok) {
          this.orders = await ordersResponse.json();
          await this.fetchOrderDetails();
        } else {
          console.error('Помилка завантаження замовлень:', ordersResponse.statusText);
        }
      }
    } catch (error) {
      console.error('Помилка підключення до API:', error);
    }
  },
  methods: {
    setActiveTab(tab) {
      this.activeTab = tab;
    },
    async fetchOrderDetails() {
      for (const order of this.orders) {
        const bakeryResponse = await fetch(`http://localhost:5000/api/order-bakery/${order.id}`);
        const bakeryItems = bakeryResponse.ok ? await bakeryResponse.json() : [];
        const drinksResponse = await fetch(`http://localhost:5000/api/order-drinks/${order.id}`);
        const drinkItems = drinksResponse.ok ? await drinksResponse.json() : [];
        this.detailedOrders.push({
          ...order,
          bakeryItems,
          drinkItems,
        });
      }
    },
  },
};
</script>

<style scoped>
.header {
  text-align: center;
  margin-bottom: 20px;
  background-color: #4CAF50;
  color: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.header p {
  font-size: 24px;
  margin: 0;
}
.tabs {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  background-color: #ffffff;
  border-radius: 5px;
  margin: 5px;
  transition: background-color 0.3s ease, color 0.3s ease, transform 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
button.active {
  background-color: #007bff;
  color: white;
  transform: scale(1.05);
}
button:hover {
  background-color: #e9ecef;
}
.tab-content {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
h2 {
  color: #007bff;
  margin-bottom: 15px;
}
p {
  color: #666;
}
</style>
