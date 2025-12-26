<template>
  <div class="staff-page">
    <h2>Графік роботи</h2>
    <div v-if="loading" class="loader-container">
      <div class="loader"></div>
    </div>
    <div v-else>
      <div class="shop-selector">
        <label for="shopSelect">Оберіть кав'ярню:</label>
        <select id="shopSelect" v-model="selectedShopId" @change="filterUsersByShop">
          <option value="">Оберіть кав'ярню</option>
          <option v-for="shop in shops" :key="shop.id" :value="shop.id">
            {{ shop.Street }}, {{ shop.nomer }}
          </option>
        </select>
      </div>
      <div class="date-selector" v-if="selectedShopId">
        <label for="dateSelect">Оберіть дату:</label>
        <input type="date" id="dateSelect" v-model="selectedDate" @change="updateCalendarView">
      </div>
      <FullCalendar v-if="selectedShopId" ref="calendar" :options="calendarOptions" />
    </div>
  </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import timeGridPlugin from '@fullcalendar/timegrid';

export default {
  name: "PrimeScheduleAdminPage",
  components: {
    FullCalendar
  },
  data() {
    return {
      users: [],
      shops: [],
      selectedShopId: '',
      selectedDate: '',
      schedule: [],
      loading: true, // Add loading state
      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin, timeGridPlugin],
        initialView: 'timeGridDay',
        slotMinTime: '06:30:00',
        slotMaxTime: '22:00:00',
        allDaySlot: false,
        events: [],
        editable: false, // Disable editing
        initialDate: new Date().toISOString().split('T')[0], // Set initial date to today
      }
    };
  },
  computed: {
    filteredUsers() {
      if (this.selectedShopId) {
        return this.users.filter(user => user.shop_id === this.selectedShopId);
      }
      return this.users;
    },
  },
  async mounted() {
    this.loading = true; // Start loading
    try {
      const usersResponse = await fetch("http://localhost:5000/api/users");
      const shopsResponse = await fetch("http://localhost:5000/api/shops");
      if (usersResponse.ok && shopsResponse.ok) {
        this.users = await usersResponse.json();
        this.shops = await shopsResponse.json();
      } else {
        console.error("Помилка завантаження даних:", usersResponse.statusText, shopsResponse.statusText);
      }

      this.loadSchedule();
    } catch (error) {
      console.error("Помилка підключення до API:", error);
    } finally {
      this.loading = false; // Stop loading
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return "Невідомо";
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(date).toLocaleDateString("uk-UA", options);
    },
    getShopAddress(shopId) {
      const shop = this.shops.find(shop => shop.id === shopId);
      return shop ? `${shop.Street}, ${shop.nomer}` : "Невідомо";
    },
    async loadSchedule() {
      try {
        const response = await fetch("http://localhost:5000/api/schedule");
        if (response.ok) {
          this.schedule = await response.json();
          this.updateCalendarEvents();
        } else {
          console.error('Помилка завантаження графіка:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка завантаження графіка:', error);
      }
    },
    getUserName(userId) {
      const user = this.users.filter(user => user.shop_id === this.selectedShopId).find(user => user.id === userId);
      return user ? `${user.last_name} ${user.first_name} ${user.middle_name}` : 'Невідомо';
    },
    updateCalendarEvents() {
      this.calendarOptions.events = this.schedule.map(item => ({
        id: item.id,
        title: this.getUserName(item.user_id),
        start: `${item.work_date}T${item.period === 'morning' ? '06:30:00' : item.period === 'evening' ? '14:00:00' : '06:30:00'}`,
        end: `${item.work_date}T${item.period === 'morning' ? '14:00:00' : item.period === 'evening' ? '22:00:00' : '22:00:00'}`,
        backgroundColor: item.period === 'morning' ? 'lightblue' : item.period === 'evening' ? 'lightgreen' : 'lightcoral',
        borderColor: item.period === 'morning' ? 'blue' : item.period === 'evening' ? 'green' : 'red',
      }));
    },
    filterUsersByShop() {
      this.loadSchedule();
    },
    updateCalendarView() {
      if (this.selectedDate) {
        this.calendarOptions.initialDate = this.selectedDate;
        this.calendarOptions.initialView = 'timeGridDay';
        // Force re-render of the calendar
        this.$refs.calendar.getApi().gotoDate(this.selectedDate);
      }
    }
  },
};
</script>

<style scoped>
.staff-page {
  padding: 20px;
  background: linear-gradient(135deg, #e6e6e6, #ffffff);
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 900px;
  margin: 0 auto;
  font-family: 'Arial', sans-serif;
}

h2 {
  color: #444;
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: bold;
}

.shop-selector {
  margin-bottom: 20px;
  text-align: center;
}

.shop-selector label {
  margin-right: 10px;
  font-weight: bold;
}

.shop-selector select {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.date-selector {
  margin-bottom: 20px;
  text-align: center;
}

.date-selector label {
  margin-right: 10px;
  font-weight: bold;
}

.date-selector input {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.loader {
  width: 50px;
  aspect-ratio: 1;
  display: grid;
  background:
      radial-gradient(closest-side at 50% 12.5%,
      #000 96%, #0000) 50% 0/20% 80% repeat-y,
      radial-gradient(closest-side at 12.5% 50%,
      #000 96%, #0000) 0 50%/80% 20% repeat-x;
  animation: l26 1s infinite steps(12);
}

.loader:before,
.loader:after {
  content: "";
  grid-area: 1/1;
  transform: rotate(30deg);
  background:
      radial-gradient(closest-side at 50% 12.5%,
      #000 96%, #0000) 50% 0/20% 80% repeat-y,
      radial-gradient(closest-side at 12.5% 50%,
      #000 96%, #0000) 0 50%/80% 20% repeat-x;
}

.loader:after {
  transform: rotate(60deg);
}

@keyframes l26 {
  100% {
    transform: rotate(1turn);
  }
}
</style>