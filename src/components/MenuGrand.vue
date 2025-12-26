<template>
  <div class="menu-container">
    <h2>Меню</h2>
    <div v-if="loading" class="loader-container">
      <div class="loader"></div>
    </div>
    <div v-else>
      <!-- Таблиця для напоїв -->
      <h3>Напої</h3>
      <table>
        <thead>
        <tr>
          <th>Назва</th>
          <th>Зображення</th>
          <th>Розміри та ціни</th>
          <th>Завантажити зображення</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="drink in drinks" :key="drink.id">
          <td>{{ drink.name }}</td>
          <td>
            <img :src="getMenuImageUrl(drink.id)" alt="Menu Image" width="100" class="menu-image" />
          </td>
          <td>
            <ul>
              <li v-for="size in getDrinkSizes(drink.id)" :key="size.size">
                {{ size.size }} - {{ size.price }} грн
              </li>
            </ul>
          </td>
          <td>
            <label class="upload-button">
              <input type="file" @change="uploadMenuImage(drink.id, $event)" class="file-input" />
              <i class="fas fa-upload"></i> Завантажити
            </label>
          </td>
        </tr>
        </tbody>
      </table>

      <!-- Таблиця для випічки -->
      <h3>Випічка</h3>
      <table>
        <thead>
        <tr>
          <th>Назва</th>
          <th>Зображення</th>
          <th>Ціна</th>
          <th>Завантажити зображення</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="item in bakeryItems" :key="item.id">
          <td>{{ item.name }}</td>
          <td>
            <img :src="getBakeryImageUrl(item.id)" alt="Bakery Image" width="100" class="menu-image" />
          </td>
          <td>{{ item.price }} грн</td>
          <td>
            <label class="upload-button">
              <input type="file" @change="uploadBakeryImage(item.id, $event)" class="file-input" />
              <i class="fas fa-upload"></i> Завантажити
            </label>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MenuGrand',
  data() {
    return {
      drinks: [], // Дані для напоїв
      drinkSizes: [], // Дані для розмірів напоїв
      bakeryItems: [], // Дані для випічки
      loading: true, // Add loading state
    };
  },
  async mounted() {
    this.loading = true; // Start loading
    try {
      const drinksResponse = await fetch('http://localhost:5000/api/drinks'); // Змініть URL за потреби
      const drinkSizesResponse = await fetch('http://localhost:5000/api/drink_sizes'); // Змініть URL за потреби
      const bakeryResponse = await fetch('http://localhost:5000/api/bakery'); // Змініть URL за потреби

      if (drinksResponse.ok && drinkSizesResponse.ok && bakeryResponse.ok) {
        this.drinks = await drinksResponse.json();
        this.drinkSizes = await drinkSizesResponse.json();
        this.bakeryItems = await bakeryResponse.json();
      } else {
        console.error('Помилка завантаження даних:', drinksResponse.statusText, drinkSizesResponse.statusText, bakeryResponse.statusText);
      }
    } catch (error) {
      console.error('Помилка підключення до API:', error);
    } finally {
      this.loading = false; // Stop loading
    }
  },
  methods: {
    getDrinkSizes(drinkId) {
      return this.drinkSizes.filter(size => size.drink_id === drinkId);
    },
    getMenuImageUrl(drinkId) {
      return `http://localhost:5000/api/get-menu-image/${drinkId}`;
    },
    async uploadMenuImage(drinkId, event) {
      const file = event.target.files[0];
      if (file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
          const response = await fetch(`http://localhost:5000/api/upload-menu-image/${drinkId}`, {
            method: 'POST',
            body: formData,
          });

          if (response.ok) {
            console.log('Menu image uploaded successfully');
          } else {
            console.error('Error uploading menu image:', response.statusText);
          }
        } catch (error) {
          console.error('Error uploading menu image:', error);
        }
      }
    },
    getBakeryImageUrl(bakeryId) {
      return `http://localhost:5000/api/get-bakery-image/${bakeryId}`;
    },
    async uploadBakeryImage(bakeryId, event) {
      const file = event.target.files[0];
      if (file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
          const response = await fetch(`http://localhost:5000/api/upload-bakery-image/${bakeryId}`, {
            method: 'POST',
            body: formData,
          });

          if (response.ok) {
            console.log('Bakery image uploaded successfully');
          } else {
            console.error('Error uploading bakery image:', response.statusText);
          }
        } catch (error) {
          console.error('Error uploading bakery image:', error);
        }
      }
    },
  },
};
</script>

<style scoped>
.menu-container {
  font-family: 'Arial', sans-serif;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #333;
  margin-bottom: 15px;
  font-size: 24px;
}

p {
  color: #666;
  font-size: 16px;
}

h3 {
  color: #333;
  margin-top: 20px;
  font-size: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

th, td {
  border: 1px solid #ddd;
  padding: 15px;
  text-align: left;
  font-size: 14px;
}

th {
  background: linear-gradient(135deg, #f4f4f4, #eaeaea);
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

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 5px;
}

.menu-image {
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.upload-button {
  display: inline-block;
  padding: 10px 15px;
  background-color: #007bff;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.upload-button:hover {
  background-color: #0056b3;
}

.file-input {
  display: none;
}

.fas.fa-upload {
  margin-right: 5px;
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