<template>
  <div class="container">
    <h2>Вакансії</h2>
    <div v-if="loading" class="loader-container">
      <div class="loader"></div>
    </div>
    <div v-else>
      <form @submit.prevent="createVacancy" class="form">
        <div class="form-group">
          <label for="title">Посада:</label>
          <select id="title" v-model="newVacancy.title" required>
            <option value="" disabled>Оберіть посаду</option>
            <option value="Бариста">Бариста</option>
            <option value="Інженер обслуговування обладнання">Інженер обслуговування обладнання</option>
            <option value="Адміністратор ПЗ">Адміністратор ПЗ</option>
            <option value="SMM-фахівець">SMM-фахівець</option>
          </select>
        </div>
        <div class="form-group">
          <label for="description">Опис вакансії:</label>
          <textarea id="description" v-model="newVacancy.description" required></textarea>
        </div>
        <div class="form-group">
          <label for="salary">Зарплата:</label>
          <input type="number" id="salary" v-model="newVacancy.salary" required>
        </div>
        <button type="submit" class="btn btn-primary">Створити вакансію</button>
      </form>
      <div v-if="vacancies.length" class="vacancy-list">
        <h3>Список вакансій:</h3>
        <ul>
          <li v-for="vacancy in vacancies" :key="vacancy.id" class="vacancy-item">
            {{ vacancy.title }} - {{ vacancy.salary }}
            <button @click="editVacancy(vacancy)" class="btn btn-secondary">Редагувати</button>
            <button @click="deleteVacancy(vacancy.id)" class="btn btn-danger">Видалити</button>
          </li>
        </ul>
      </div>
      <div v-if="editingVacancy" class="edit-form">
        <h3>Редагувати вакансію</h3>
        <form @submit.prevent="updateVacancy" class="form">
          <div class="form-group">
            <label for="editTitle">Посада:</label>
            <select id="editTitle" v-model="editingVacancy.title" required>
              <option value="" disabled>Оберіть посаду</option>
              <option value="Бариста">Бариста</option>
              <option value="Інженер обслуговування обладнання">Інженер обслуговування обладнання</option>
              <option value="Адміністратор ПЗ">Адміністратор ПЗ</option>
              <option value="SMM-фахівець">SMM-фахівець</option>
            </select>
          </div>
          <div class="form-group">
            <label for="editDescription">Опис вакансії:</label>
            <textarea id="editDescription" v-model="editingVacancy.description" required></textarea>
          </div>
          <div class="form-group">
            <label for="editSalary">Зарплата:</label>
            <input type="number" id="editSalary" v-model="editingVacancy.salary" required>
          </div>
          <button type="submit" class="btn btn-primary">Оновити вакансію</button>
          <button type="button" @click="cancelEdit" class="btn btn-secondary">Скасувати</button>
        </form>
      </div>
      <div v-if="resumes.length" class="resume-list">
        <h3>Резюме:</h3>
        <ul>
          <li v-for="resume in resumes" :key="resume.id" class="resume-item">
            <p>Посада: {{ resume.vacancy_title }}</p>
            <p>ПІБ: {{ resume.last_name }} {{ resume.first_name }} {{ resume.middle_name }}</p>
            <p>Телефон: {{ resume.phone }}</p>
            <p>Спосіб зв'язку: {{ resume.contact_method }} ({{ resume.contact_detail }})</p>
            <p>Мешкає в Чернігові: {{ resume.residence }}</p>
            <p>Попередній досвід: {{ resume.experience }}</p>
            <p>Про себе: {{ resume.about }}</p>
            <p>Чому саме CoffeBoss: {{ resume.why_coffe_boss }}</p>
            <p>Дата подачі: {{ resume.created_at }}</p>
            <div class="form-group">
              <label for="shopSelect">Призначити кав'ярню:</label>
              <select id="shopSelect" v-model="resume.shop_id" @change="assignShop(resume.id, resume.shop_id)">
                <option value="" disabled>Оберіть кав'ярню</option>
                <option value="">Не призначено</option>
                <option v-for="shop in shops" :key="shop.id" :value="shop.id">{{ shop.Street }} {{ shop.nomer }}</option>
              </select>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PrimeVacancies',
  data() {
    return {
      newVacancy: {
        title: '',
        description: '',
        salary: null,
      },
      editingVacancy: null,
      vacancies: [],
      resumes: [],
      shops: [],
      loading: true, // Add loading state
    };
  },
  async mounted() {
    this.loading = true; // Start loading
    try {
      await Promise.all([
        this.fetchVacancies(),
        this.fetchResumes(),
        this.fetchShops(),
      ]);
    } catch (error) {
      console.error('Помилка при отриманні даних:', error);
    } finally {
      this.loading = false; // Stop loading
    }
  },
  methods: {
    async createVacancy() {
      try {
        const response = await fetch('http://localhost:5000/api/vacancies', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.newVacancy),
        });
        if (response.ok) {
          const vacancy = await response.json();
          this.vacancies.push(vacancy);
          this.newVacancy = { title: '', description: '', salary: null };
        } else {
          console.error('Помилка створення вакансії:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка підключення до API:', error);
      }
    },
    async deleteVacancy(vacancyId) {
      try {
        const response = await fetch(`http://localhost:5000/api/vacancies/${vacancyId}`, {
          method: 'DELETE',
        });
        if (response.ok) {
          this.vacancies = this.vacancies.filter(vacancy => vacancy.id !== vacancyId);
        } else {
          console.error('Помилка видалення вакансії:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка підключення до API:', error);
      }
    },
    editVacancy(vacancy) {
      this.editingVacancy = { ...vacancy };
    },
    async updateVacancy() {
      try {
        const response = await fetch(`http://localhost:5000/api/vacancies/${this.editingVacancy.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.editingVacancy),
        });
        if (response.ok) {
          const updatedVacancy = await response.json();
          const index = this.vacancies.findIndex(vacancy => vacancy.id === updatedVacancy.id);
          if (index !== -1) {
            this.vacancies.splice(index, 1, updatedVacancy);
          }
          this.editingVacancy = null;
        } else {
          console.error('Помилка оновлення вакансії:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка підключення до API:', error);
      }
    },
    cancelEdit() {
      this.editingVacancy = null;
    },
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
    async fetchResumes() {
      try {
        const response = await fetch('http://localhost:5000/api/feedback');
        if (response.ok) {
          const resumes = await response.json();
          for (const resume of resumes) {
            const vacancy = this.vacancies.find(v => v.id === resume.vacancy_id);
            resume.vacancy_title = vacancy ? vacancy.title : 'Невідома посада';
            const shop = this.shops.find(s => s.id === resume.shop_id);
            resume.shop_name = shop ? `${shop.Street} ${shop.nomer}` : 'Не призначено';
          }
          this.resumes = resumes;
        } else {
          console.error('Помилка завантаження резюме:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка підключення до API:', error);
      }
    },
    async fetchShops() {
      try {
        const response = await fetch('http://localhost:5000/api/shops');
        if (response.ok) {
          this.shops = await response.json();
        } else {
          console.error('Помилка завантаження кав\'ярень:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка підключення до API:', error);
      }
    },
    async assignShop(feedbackId, shopId) {
      try {
        const response = await fetch(`http://localhost:5000/api/feedback/${feedbackId}/assign-shop`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            shop_id: shopId === '' ? null : shopId
          }),
        });
        if (response.ok) {
          console.log('Shop assigned successfully');
          const resume = this.resumes.find(r => r.id === feedbackId);
          if (resume) {
            resume.shop_id = shopId === '' ? null : shopId;
            const shop = this.shops.find(s => s.id === shopId);
            resume.shop_name = shop ? `${shop.Street} ${shop.nomer}` : 'Не призначено';
          }
        } else {
          console.error('Помилка призначення кав\'ярні:', response.statusText);
        }
      } catch (error) {
        console.error('Помилка підключення до API:', error);
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.form {
  display: grid;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 5px;
  font-weight: bold;
}

select, textarea, input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.btn-danger {
  background-color: #dc3545;
}

.btn-danger:hover {
  background-color: #c82333;
}

.vacancy-list, .resume-list {
  margin-top: 20px;
}

.vacancy-item, .resume-item {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  margin-bottom: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.vacancy-item button, .resume-item button {
  margin-top: 10px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
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