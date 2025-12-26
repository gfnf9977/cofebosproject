<template>
  <div>
    <div class="header">
      <p v-if="fullName">Вітаємо, {{ fullName }}!</p>
    </div>

    <div class="tabs">
      <button :class="{ active: activeTab === 'home' }" @click="setActiveTab('home')">Головна</button>
      <button :class="{ active: activeTab === 'menu' }" @click="setActiveTab('menu')">Меню</button>
      <button :class="{ active: activeTab === 'vacancies' }" @click="setActiveTab('vacancies')">Кандидати на роботу</button>
      <button :class="{ active: activeTab === 'staff' }" @click="setActiveTab('staff')">Працівники</button>
      <button :class="{ active: activeTab === 'schedule' }" @click="setActiveTab('schedule')">Графік роботи</button>
      <button :class="{ active: activeTab === 'guests' }" @click="setActiveTab('guests')">Гості</button>
      <button :class="{ active: activeTab === 'orders' }" @click="setActiveTab('orders')">Замовлення</button>
      <button :class="{ active: activeTab === 'income' }" @click="setActiveTab('income')">Дохід</button>
      <button :class="{ active: activeTab === 'statistics' }" @click="setActiveTab('statistics')">Статистика</button>
      <button :class="{ active: activeTab === 'gallery' }" @click="setActiveTab('gallery')">Галерея</button>
      <button :class="{ active: activeTab === 'chat' }" @click="setActiveTab('chat')">Чат</button>
      <button :class="{ active: activeTab === 'profile' }" @click="setActiveTab('profile')">Профіль</button>
      <button :class="{ active: activeTab === 'bonusGifts' }" @click="setActiveTab('bonusGifts')">Бонусні подарунки</button>
    </div>

    <div class="tab-content">
      <div v-if="activeTab === 'home'">
        <HomeAdminPage />
      </div>
      <div v-if="activeTab === 'menu'">
        <MenuAdmin :userId="userID" :username="username" />
      </div>
      <div v-if="activeTab === 'vacancies'">
        <AdminVacancies :shopId="shopID" />
      </div>
      <div v-if="activeTab === 'staff'">
        <StaffAdminPage />
      </div>
      <div v-if="activeTab === 'schedule'">
        <ScheduleAdminPage />
      </div>
      <div v-if="activeTab === 'guests'">
        <GuestsAdminPage />
      </div>
      <div v-if="activeTab === 'orders'">
        <OrdersAdmin :userId="userID" :shopId="shopID" :orders="detailedOrders" />
      </div>
      <div v-if="activeTab === 'income'">
        <h2>Дохід</h2>
        <p>Зміст доходу...</p>
      </div>
      <div v-if="activeTab === 'statistics'">
        <h2>Статистика</h2>
        <p>Зміст статистики...</p>
      </div>
      <div v-if="activeTab === 'profile'">
        <ProfileAdmin :username="username" />
      </div>
      <div v-if="activeTab === 'gallery'">
        <GalleryView :images="galleryImages" />
      </div>
      <div v-if="activeTab === 'chat'">
        <AdminConnect />
      </div>
      <div v-if="activeTab === 'bonusGifts'">
        <AdminBonusGift />
      </div>
    </div>
  </div>
</template>

<script>
import HomeAdminPage from './HomeAdminPage.vue';
import ProfileAdmin from './ProfileFitches.vue';
import StaffAdminPage from './StaffAdPage.vue';
import GuestsAdminPage from './GuestsAdPage.vue';
import MenuAdmin from './MenuAdmin.vue';
import OrdersAdmin from './OrdersAdmin.vue';
import AdminVacancies from './AdminVacancies.vue';
import ScheduleAdminPage from './ScheduleAdminPage.vue';
import GalleryView from './GalleryView.vue';
import AdminConnect from './AdminConnect.vue';
import AdminBonusGift from './AdminBonusGift.vue';

export default {
  name: 'AdminPage',
  components: {
    HomeAdminPage,
    ProfileAdmin,
    StaffAdminPage,
    GuestsAdminPage,
    MenuAdmin,
    OrdersAdmin,
    AdminVacancies,
    ScheduleAdminPage,
    GalleryView,
    AdminConnect,
    AdminBonusGift,
  },
  data() {
    return {
      activeTab: 'home',
      username: '',
      fullName: '',
      userID: null,
      shopID: null,
      orders: [],
      detailedOrders: [],
      galleryImages: [],
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
          this.userID = userIdData.id;

          // Fetch the shop ID based on the user ID
          const shopIdResponse = await fetch(`http://localhost:5000/api/shop-id?user_id=${this.userID}`);
          if (shopIdResponse.ok) {
            const shopIdData = await shopIdResponse.json();
            this.shopID = shopIdData.shop_id;
          } else {
            console.error('Помилка завантаження ID кав\'ярні:', shopIdResponse.statusText);
          }
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

        // Fetch the gallery data
        const galleryResponse = await fetch('http://localhost:5000/api/gallery');
        if (galleryResponse.ok) {
          this.galleryImages = await galleryResponse.json();
        } else {
          console.error('Помилка завантаження галереї:', galleryResponse.statusText);
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
}

.header p {
  color: #333;
  font-size: 18px;
  margin: 0;
}

.tabs {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
  background-color: #f0f0f0;
  border-radius: 8px;
  padding: 10px;
}

button {
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  background-color: transparent;
  border-radius: 5px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

button.active {
  background-color: #007bff;
  color: white;
}

button:hover {
  background-color: #ddd;
}

.tab-content {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
}

h2 {
  color: #333;
  margin-bottom: 15px;
}

p {
  color: #666;
}
</style>