<template>
  <div class="vacancies-container flow">
    <h1 class="main__heading">Вакансії</h1>

    <div v-if="loading" class="loader-container">
      <div class="coffee-cup">
        <img src="/coffeboss.png" alt="Coffeboss" class="coffee-image" />
      </div>
    </div>

    <div v-else>
      <div v-if="vacancies.length" class="cards">
        <div class="cards__inner">
          <div class="card vacancy-card" v-for="vacancy in vacancies" :key="vacancy.id">
            <h2 class="card__heading">{{ vacancy.title }}</h2>
            <p class="vacancy-description">{{ vacancy.description }}</p>
            <p class="vacancy-salary">💰 Зарплата: <strong>{{ vacancy.salary }}</strong></p>
            <button class="cta apply-button" @click="openFeedbackModal(vacancy.id)">Відгукнутися</button>
          </div>
        </div>
        <div class="overlay cards__inner"></div>
      </div>

      <div v-else class="no-vacancies">
        <p>Наразі немає доступних вакансій.</p>
      </div>

      <ResumeCreate
          v-if="showFeedbackModal"
          :userId="userId"
          :firstName="firstName"
          :middleName="middleName"
          :lastName="lastName"
          :phone="phone"
          :vacancyId="selectedVacancyId"
          @close="closeFeedbackModal"
      />
    </div>
  </div>
</template>

<script>
import ResumeCreate from './ResumeCreate.vue';

export default {
  name: 'UserVacancies',
  components: { ResumeCreate },
  data() {
    return {
      vacancies: [],
      showFeedbackModal: false,
      userId: null,
      firstName: '',
      middleName: '',
      lastName: '',
      phone: '',
      selectedVacancyId: null,
      loading: true,
    };
  },
  methods: {
    async fetchVacancies() {
      try {
        const response = await fetch('http://localhost:5000/api/vacancies');
        if (response.ok) {
          this.vacancies = await response.json();
        } else {
          console.error('Помилка завантаження вакансій:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка підключення до API:', error);
      }
    },
    openFeedbackModal(vacancyId) {
      this.selectedVacancyId = vacancyId;
      this.showFeedbackModal = true;
    },
    closeFeedbackModal() {
      this.showFeedbackModal = false;
    },
    async fetchUserDetails() {
      try {
        const username = localStorage.getItem('username');
        if (username) {
          const response = await fetch(`http://localhost:5000/api/user-profile?username=${username}`);
          if (response.ok) {
            const userData = await response.json();
            this.firstName = userData.first_name;
            this.middleName = userData.middle_name;
            this.lastName = userData.last_name;
            this.phone = userData.phone_number;
          }

          const userIdResponse = await fetch(`http://localhost:5000/api/user-id?username=${username}`);
          if (userIdResponse.ok) {
            const userIdData = await userIdResponse.json();
            this.userId = userIdData.id;
          }
        }
      } catch (error) {
        console.error('Помилка підключення до API:', error);
      }
    },
  },
  mounted() {
    setTimeout(() => {
      this.loading = false;
    }, 3000);
    this.fetchVacancies();
    this.fetchUserDetails();
  },
};
</script>

<style scoped>
.vacancies-container {
  max-width: 75rem;
  padding: 3em 1.5em;
  margin: 0 auto;
}

.main__heading {
  font-weight: 600;
  font-size: 2.25em;
  margin-bottom: 0.75em;
  text-align: center;
  color: #000000;
}

.cards {
  position: relative;
}

.cards__inner {
  display: flex;
  flex-wrap: wrap;
  gap: 2.5em;
}

.vacancy-card {
  --flow-space: 0.5em;
  --hsl: var(--hue), var(--saturation), var(--lightness);
  flex: 1 1 14rem;
  padding: 1.5em 2em;
  display: grid;
  grid-template-rows: auto auto auto 1fr;
  align-items: start;
  gap: 1.25em;
  color: #eceff1;
  background-color: #2b2b2b;
  border: 1px solid #eceff133;
  border-radius: 15px;
  transition: 400ms background ease;
  will-change: background;
}

.vacancy-card:hover {
  --lightness: 95%;
  background: hsla(var(--hsl), 0.1);
}

.vacancy-card:hover .card__heading,
.vacancy-card:hover .vacancy-description {
  color: #000000; /* Колір тексту стає чорним при наведенні */
}

.vacancy-card:nth-child(1) {
  --hue: 165;
  --saturation: 82.26%;
  --lightness: 51.37%;
}

.vacancy-card:nth-child(2) {
  --hue: 291.34;
  --saturation: 95.9%;
  --lightness: 61.76%;
}

.vacancy-card:nth-child(3) {
  --hue: 338.69;
  --saturation: 100%;
  --lightness: 48.04%;
}

.vacancy-description {
  color: #ddd;
  font-size: 14px;
  margin-top: 5px;
  transition: color 0.3s ease; /* Додано плавний перехід для кольору тексту */
}

.vacancy-salary {
  color: #007bff;
  font-weight: bold;
  margin-top: 10px;
}

.apply-button {
  display: block;
  align-self: end;
  margin: 1em 0 0.5em 0;
  text-align: center;
  text-decoration: none;
  color: black;
  border: 2px solid antiquewhite;
  padding: 1rem 5rem;
  position: relative;
  overflow: hidden;
  transition: all 1s;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
}

.apply-button:before {
  content: "Подати резюме";
  font-weight: bold;
  color: #000;
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: antiquewhite;
  transform: translateY(-100%);
  transition: all 1s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.apply-button:hover:before {
  transform: translateY(0);
}

.no-vacancies {
  text-align: center;
  color: #666;
  font-size: 18px;
  padding: 20px;
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50vh;
}

.coffee-cup {
  width: 150px;
  height: 150px;
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
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
  user-select: none;
  opacity: var(--opacity, 0);
  -webkit-mask: radial-gradient(
      25rem 25rem at var(--x) var(--y),
      #000 1%,
      transparent 50%
  );
  mask: radial-gradient(
      25rem 25rem at var(--x) var(--y),
      #000 1%,
      transparent 50%
  );
  transition: 400ms mask ease;
  will-change: mask;
}

.overlay .vacancy-card {
  background-color: hsla(var(--hsl), 0.15);
  border-color: hsla(var(--hsl), 1);
  box-shadow: 0 0 0 1px inset hsl(var(--hsl));
}

.overlay .apply-button {
  display: block;
  grid-row: -1;
  width: 100%;
  background-color: hsl(var(--hsl));
  box-shadow: 0 0 0 1px hsl(var(--hsl));
}
</style>