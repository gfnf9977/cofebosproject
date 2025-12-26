<template>
  <div>
    <div v-if="loading" class="loader-container">
      <div class="coffee-cup">
        <img src="/coffeboss.png" alt="Coffeboss" class="coffee-image" />
      </div>
    </div>
    <div v-else>
      <div class="header">
        <p v-if="fullName">Вітаємо, {{ fullName }}!</p>
        <p class="points" @click="openPointsOptions">
          Ваші бали: {{ displayPoints }}
          <img src="/cardr-removebg-preview.ico" alt="Points Icon" class="points-icon">
        </p>
      </div>

      <div class="tabs">
        <button :class="{ active: activeTab === 'home', 'list-items': true }" @click="setActiveTab('home')">Головна</button>
        <button :class="{ active: activeTab === 'menu', 'list-items': true }" @click="setActiveTab('menu')">Меню</button>
        <button :class="{ active: activeTab === 'vacancies', 'list-items': true }" @click="setActiveTab('vacancies')">Вакансії</button>
        <button :class="{ active: activeTab === 'orders', 'list-items': true }" @click="setActiveTab('orders')">Мої замовлення</button>
        <button :class="{ active: activeTab === 'gallery', 'list-items': true }" @click="setActiveTab('gallery')">Галерея</button>
        <button :class="{ active: activeTab === 'cafes', 'list-items': true }" @click="setActiveTab('cafes')">Наші кав'ярні</button>
        <button :class="{ active: activeTab === 'profile', 'list-items': true }" @click="setActiveTab('profile')">Профіль</button>
        <button :class="{ active: activeTab === 'payments', 'list-items': true }" @click="setActiveTab('payments')">Чеки та оплати</button>
        <button :class="{ active: activeTab === 'connect', 'list-items': true }" @click="setActiveTab('connect')">Зв'язок</button>
      </div>

      <div class="tab-content">
        <div v-if="activeTab === 'home'">
          <HomeUserPage />
        </div>
        <div v-if="activeTab === 'menu'">
          <MenuUsr :username="username" />
        </div>
        <div v-if="activeTab === 'vacancies'">
          <UserVacancies />
        </div>
        <div v-if="activeTab === 'orders'">
          <OrdersPage :userId="userId" :orders="detailedOrders" />
        </div>
        <div v-if="activeTab === 'cafes'">
          <CafesPage />
        </div>
        <div v-if="activeTab === 'profile'">
          <ProfileFitches :username="username" />
        </div>
        <div v-if="activeTab === 'payments'">
          <PaymentsPage :userId="userId" :orders="detailedOrders" />
        </div>
        <div v-if="activeTab === 'gallery'">
          <GalleryShow :images="galleryImages" />
        </div>
        <div v-if="activeTab === 'connect'">
          <UserConnect />
        </div>
      </div>
    </div>

    <PointsOptions v-if="showPointsOptions" @close="closePointsOptions" :userId="userId" :username="username" :points="points" />
  </div>
</template>

<script>
import HomeUserPage from './HomeUserPage.vue';
import ProfileFitches from './ProfileFitches.vue';
import CafesPage from './CafesPage.vue';
import MenuUsr from './MenuUsr.vue';
import OrdersPage from './OrdersPage.vue';
import PaymentsPage from './PaymentsPage.vue';
import UserVacancies from './UserVacancies.vue';
import GalleryShow from './GalleryShow.vue';
import UserConnect from './UserConnect.vue';
import PointsOptions from './PointsOptions.vue'; // Імпорт нового компонента

export default {
  name: 'UserPage',
  components: {
    HomeUserPage,
    ProfileFitches,
    CafesPage,
    MenuUsr,
    OrdersPage,
    PaymentsPage,
    UserVacancies,
    GalleryShow,
    UserConnect,
    PointsOptions, // Реєстрація нового компонента
  },
  data() {
    return {
      activeTab: 'home',
      username: '',
      fullName: '',
      userId: null,
      points: null,
      detailedOrders: [],
      galleryImages: [],
      loading: true,
      showPointsOptions: false, // Added state for PointsOptions
    };
  },
  computed: {
    displayPoints() {
      return this.points !== null ? this.points : '0 балів';
    },
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

          const userIdResponse = await fetch(`http://localhost:5000/api/user-id?username=${username}`);
          if (userIdResponse.ok) {
            const userIdData = await userIdResponse.json();
            this.userId = userIdData.id;

            const pointsResponse = await fetch(`http://localhost:5000/api/user-points/${this.userId}`);
            if (pointsResponse.ok) {
              const pointsData = await pointsResponse.json();
              this.points = pointsData.points;
            } else {
              console.error('Помилка завантаження балів:', pointsResponse.statusText);
            }

            const ordersResponse = await fetch(`http://localhost:5000/api/orders-idsort/${this.userId}`);
            if (ordersResponse.ok) {
              this.orders = await ordersResponse.json();
              await this.fetchOrderDetails();
            } else {
              console.error('Помилка завантаження замовлень:', ordersResponse.statusText);
            }

            const galleryResponse = await fetch('http://localhost:5000/api/gallery');
            if (galleryResponse.ok) {
              this.galleryImages = await galleryResponse.json();
            } else {
              console.error('Помилка завантаження галереї:', galleryResponse.statusText);
            }
          } else {
            console.error('Помилка завантаження ID користувача:', userIdResponse.statusText);
          }
        } else {
          console.error('Помилка завантаження даних користувача:', response.statusText);
        }
      } else {
        console.error('Username not found in localStorage');
      }
    } catch (error) {
      console.error('Помилка підключення до API:', error);
    } finally {
      // Simulate loading
      setTimeout(() => {
        this.loading = false;
      }, 3000);
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
    openPointsOptions() {
      this.showPointsOptions = true;
    },
    closePointsOptions() {
      this.showPointsOptions = false;
    },
  },
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header p {
  color: #333;
  font-size: 18px;
  margin: 0;
}

.points {
  display: flex;
  align-items: center;
  margin-right: 20px;
  cursor: pointer;
}

.points-icon {
  width: 30px;
  height: 30px;
  margin-left: 5px;
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
  position: relative;
  text-transform: uppercase;
}

button.active {
  background-color: #007bff;
  color: white;
}

button:hover {
  background-color: #ddd;
}

button.list-items:before {
  content: "";
  position: absolute;
  bottom: 12px;
  left: 12px;
  width: 12px;
  height: 12px;
  border: 3px solid black;
  border-width: 0 0 3px 3px;
  opacity: 0;
  transition: all 0.6s;
}

button.list-items:hover:before {
  opacity: 1;
  bottom: -8px;
  left: -8px;
}

button.list-items:after {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  width: 12px;
  height: 12px;
  border: 3px solid black;
  border-width: 3px 3px 0 0;
  opacity: 0;
  transition: all 0.6s;
}

button.list-items:hover:after {
  opacity: 1;
  top: -8px;
  right: -8px;
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
