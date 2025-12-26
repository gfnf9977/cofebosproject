<template>
  <div>
    <h2>Кандидати на роботу для кав'ярні ID: {{ shopId }}</h2>
    <div v-if="loading" class="loader-container">
      <div class="loader"></div>
    </div>
    <div v-else>
      <div v-if="filteredFeedbackList.length > 0">
        <div v-for="feedback in filteredFeedbackList" :key="feedback.id" class="feedback-item">
          <p><strong>Ім'я:</strong> {{ feedback.first_name }} {{ feedback.middle_name }} {{ feedback.last_name }}</p>
          <p><strong>Телефон:</strong> {{ feedback.phone }}</p>
          <p><strong>Метод зв'язку:</strong> {{ feedback.contact_method }}</p>
          <p><strong>Деталі зв'язку:</strong> {{ feedback.contact_detail }}</p>
          <p><strong>Місце проживання:</strong> {{ feedback.residence }}</p>
          <p><strong>Досвід:</strong> {{ feedback.experience }}</p>
          <p><strong>Про себе:</strong> {{ feedback.about }}</p>
          <p><strong>Чому CoffeBoss:</strong> {{ feedback.why_coffe_boss }}</p>
          <p><strong>Дата створення:</strong> {{ feedback.created_at }}</p>
          <p><strong>ID кав'ярні:</strong> {{ feedback.shop_id }}</p>
        </div>
      </div>
      <div v-else>
        <p>Немає записів відгуків для цієї кав'ярні.</p>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'AdminVacancies',
  props: {
    shopId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      feedbackList: [],
      loading: false
    };
  },
  computed: {
    filteredFeedbackList() {
      return this.feedbackList.filter(feedback => feedback.shop_id === this.shopId);
    }
  },
  async mounted() {
    this.loading = true;
    try {
      const response = await fetch('http://localhost:5000/api/feedback');
      if (response.ok) {
        this.feedbackList = await response.json();
      } else {
        console.error('Помилка завантаження даних відгуків:', response.statusText);
      }
    } catch (error) {
      console.error('Помилка підключення до API:', error);
    } finally {
      this.loading = false;
    }
  }
};
</script>


<style scoped>
.feedback-item {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  background-color: #f9f9f9;
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