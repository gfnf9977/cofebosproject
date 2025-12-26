<template>
  <div class="staff-page">
    <h2>Графік роботи</h2>
    <div v-if="loading" class="loader-container">
      <div class="loader"></div>
    </div>
    <div v-else>
      <div class="date-selector">
        <label for="dateSelect">Оберіть дату:</label>
        <input type="date" id="dateSelect" v-model="selectedDate" @change="updateCalendarView">
      </div>
      <div class="schedule-form">
        <h3>Додати графік</h3>
        <label for="userId">Працівник:</label>
        <select id="userId" v-model="newSchedule.user_id">
          <option v-for="user in filteredUsers" :key="user.id" :value="user.id">
            {{ user.last_name }} {{ user.first_name }} {{ user.middle_name }}
          </option>
        </select>
        <label for="workDate">Дата:</label>
        <input type="date" id="workDate" v-model="newSchedule.work_date">
        <label for="period">Період:</label>
        <select id="period" v-model="newSchedule.period">
          <option value="morning">6:30 - 14:00</option>
          <option value="evening">14:00 - 22:00</option>
          <option value="full_day">6:30 - 22:00</option>
        </select>
        <button @click="addSchedule">Додати</button>
      </div>
      <FullCalendar ref="calendar" :options="calendarOptions" />
    </div>
  </div>
</template>


<script>
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import timeGridPlugin from '@fullcalendar/timegrid';

export default {
  name: "ScheduleAdminPage",
  components: {
    FullCalendar
  },
  data() {
    return {
      users: [],
      shops: [],
      currentUserId: null,
      currentShopId: null,
      newSchedule: {
        user_id: null,
        work_date: '',
        period: ''
      },
      selectedDate: '',
      schedule: [],
      loading: false,
      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin, timeGridPlugin],
        initialView: 'timeGridDay', // Відображення сітки часу за день
        slotMinTime: '06:30:00', // Мінімальний час для відображення
        slotMaxTime: '22:00:00', // Максимальний час для відображення
        allDaySlot: false, // Вимкнути слот для цілодобових подій
        events: [],
        dateClick: this.handleDateClick,
        eventClick: this.handleEventClick,
        editable: true, // Дозволяє перетягування та зміну розміру подій
        eventDrop: this.handleEventDrop, // Обробник перетягування подій
        eventResize: this.handleEventResize, // Обробник зміни розміру подій
        eventContent: this.renderEventContent // Обробник відображення вмісту події
      }
    };
  },
  computed: {
    filteredUsers() {
      if (this.currentShopId) {
        return this.users.filter(user => user.shop_id === this.currentShopId);
      }
      return this.users;
    },
  },
  async mounted() {
    this.loading = true;
    try {
      const username = localStorage.getItem('username');
      if (username) {
        const userIdResponse = await fetch(`http://localhost:5000/api/user-id?username=${username}`);
        if (userIdResponse.ok) {
          const userIdData = await userIdResponse.json();
          this.currentUserId = userIdData.id;

          const shopIdResponse = await fetch(`http://localhost:5000/api/shop-id?user_id=${this.currentUserId}`);
          if (shopIdResponse.ok) {
            const shopIdData = await shopIdResponse.json();
            this.currentShopId = shopIdData.shop_id;
          } else {
            console.error('Помилка завантаження ID кав\'ярні:', shopIdResponse.statusText);
          }
        } else {
          console.error('Помилка завантаження ID користувача:', userIdResponse.statusText);
        }
      }

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
      this.loading = false;
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
    async addSchedule() {
      if (this.hasConflict()) {
        alert('Працівник вже записаний на цей час.');
        return;
      }

      try {
        const response = await fetch('http://localhost:5000/api/schedule', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: this.newSchedule.user_id,
            shop_id: this.currentShopId,
            work_date: this.newSchedule.work_date,
            period: this.newSchedule.period
          })
        });
        if (response.ok) {
          this.loadSchedule();
          this.newSchedule = { user_id: null, work_date: '', period: '' };
        } else {
          console.error('Помилка додавання графіка:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка додавання графіка:', error);
      }
    },
    async deleteSchedule(scheduleId) {
      try {
        const response = await fetch(`http://localhost:5000/api/schedule/${scheduleId}`, {
          method: 'DELETE'
        });
        if (response.ok) {
          this.loadSchedule();
        } else {
          console.error('Помилка видалення графіка:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка видалення графіка:', error);
      }
    },
    getUserPeriod(userId) {
      const scheduleItem = this.schedule.find(item => item.user_id === userId);
      return scheduleItem ? scheduleItem.period : 'Невідомо';
    },
    getUserName(userId) {
      const user = this.users.find(user => user.id === userId);
      return user ? `${user.last_name} ${user.first_name} ${user.middle_name}` : 'Невідомо';
    },
    updateCalendarEvents() {
      this.calendarOptions.events = this.schedule.map(item => ({
        id: item.id, // Explicitly set the ID
        title: this.getUserName(item.user_id),
        start: `${item.work_date}T${item.period === 'morning' ? '06:30:00' : item.period === 'evening' ? '14:00:00' : '06:30:00'}`,
        end: `${item.work_date}T${item.period === 'morning' ? '14:00:00' : item.period === 'evening' ? '22:00:00' : '22:00:00'}`,
        backgroundColor: item.period === 'morning' ? 'lightblue' : item.period === 'evening' ? 'lightgreen' : 'lightcoral',
        borderColor: item.period === 'morning' ? 'blue' : item.period === 'evening' ? 'green' : 'red',
        extendedProps: {
          scheduleId: item.id
        }
      }));
    },
    handleDateClick(arg) {
      console.log('date click! ' + arg.dateStr);
    },
    handleEventClick(arg) {
      console.log('event click! ' + arg.event.title);
      this.deleteSchedule(arg.event.extendedProps.scheduleId);
    },
    handleEventDrop(arg) {
      console.log('event drop! ' + arg.event.title);
      // Обробка перетягування події
    },
    handleEventResize(arg) {
      console.log('event resize! ' + arg.event.title);
      // Обробка зміни розміру події
    },
    hasConflict() {
      const newStart = new Date(`${this.newSchedule.work_date}T${this.newSchedule.period === 'morning' ? '06:30:00' : this.newSchedule.period === 'evening' ? '14:00:00' : '06:30:00'}`);
      const newEnd = new Date(`${this.newSchedule.work_date}T${this.newSchedule.period === 'morning' ? '14:00:00' : this.newSchedule.period === 'evening' ? '22:00:00' : '22:00:00'}`);

      return this.schedule.some(item => {
        const existingStart = new Date(`${item.work_date}T${item.period === 'morning' ? '06:30:00' : item.period === 'evening' ? '14:00:00' : '06:30:00'}`);
        const existingEnd = new Date(`${item.work_date}T${item.period === 'morning' ? '14:00:00' : item.period === 'evening' ? '22:00:00' : '22:00:00'}`);
        return item.user_id === this.newSchedule.user_id &&
            ((newStart >= existingStart && newStart < existingEnd) ||
                (newEnd > existingStart && newEnd <= existingEnd) ||
                (newStart <= existingStart && newEnd >= existingEnd));
      });
    },
    renderEventContent(arg) {
      let eventContent = document.createElement('div');
      eventContent.innerHTML = `
        <div>${arg.event.title}</div>
        <button class="delete-button">Видалити</button>
      `;

      eventContent.querySelector('.delete-button').addEventListener('click', (event) => {
        event.stopPropagation(); // Prevent event propagation
        const scheduleId = arg.event.extendedProps.scheduleId;
        this.deleteSchedule(scheduleId);
      });

      return { domNodes: [eventContent] };
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
  background: linear-gradient(135deg, #f0f0f0, #ffffff);
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

h2 {
  color: #333;
  text-align: center;
  font-size: 28px;
  margin-bottom: 20px;
  font-weight: bold;
}

.date-selector {
  margin-bottom: 20px;
  text-align: center;
}

.date-selector label {
  margin-right: 10px;
  font-weight: bold;
  color: #555;
}

.date-selector input {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.schedule-form {
  margin-bottom: 20px;
  text-align: center;
}

.schedule-form h3 {
  color: #333;
  font-size: 24px;
  margin-bottom: 20px;
}

.schedule-form label {
  margin-right: 10px;
  font-weight: bold;
  color: #555;
}

.schedule-form select, .schedule-form input {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-right: 10px;
  margin-bottom: 10px;
}

.schedule-form button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.schedule-form button:hover {
  background-color: #45a049;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px 15px;
  text-align: left;
  font-size: 16px;
}

th {
  background: linear-gradient(135deg, #f9f9f9, #eaeaea);
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
}

td {
  background-color: #fff;
}

tr:nth-child(even) td {
  background-color: #f9f9f9;
}

tr:hover td {
  background-color: #f1f1f1;
  transition: background-color 0.2s ease;
}

.delete-button {
  background-color: #ff4d4d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  padding: 5px 10px;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.delete-button:hover {
  background-color: #ff1a1a;
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.loader {
  --s: 25px;
  --g: 5px;
  width: calc(2*(1.353*var(--s) + var(--g)));
  aspect-ratio: 1;
  background:
      linear-gradient(#000 0 0) left/50% 100% no-repeat,
      conic-gradient(from -90deg at var(--s) calc(0.353*var(--s)),
      #fff 135deg, #666 0 270deg, #aaa 0);
  background-blend-mode: multiply;
  --_m:
      linear-gradient(to bottom right,
      #0000 calc(0.25*var(--s)), #000 0 calc(100% - calc(0.25*var(--s)) - 1.414*var(--g)), #0000 0),
      conic-gradient(from -90deg at right var(--g) bottom var(--g), #000 90deg, #0000 0);
  -webkit-mask: var(--_m);
  mask: var(--_m);
  background-size: 50% 50%;
  -webkit-mask-size: 50% 50%;
  mask-size: 50% 50%;
  -webkit-mask-composite: source-in;
  mask-composite: intersect;
  animation: l9 1.5s infinite;
}

@keyframes l9 {
  0%, 12.5% { background-position: 0% 0%, 0 0; }
  12.6%, 37.5% { background-position: 100% 0%, 0 0; }
  37.6%, 62.5% { background-position: 100% 100%, 0 0; }
  62.6%, 87.5% { background-position: 0% 100%, 0 0; }
  87.6%, 100% { background-position: 0% 0%, 0 0; }
}
</style>