<template>
  <div class="home-page">
    <header class="header-section fade-in">
      <div class="logo-container">
        <img src="/87654.png" alt="COFFEEBOSS Logo" class="logo">
      </div>
      <h1>Головна</h1>
      <p class="welcome-text">Ласкаво просимо до мережі затишних кав’ярень COFFEEBOSS!</p>
    </header>

    <section class="hero-section fade-in">
      <div class="hero-content">
        <h2>Відчуйте аромат справжньої кави</h2>
        <p>Насолоджуйтесь найкращими сортами кави та вишуканою випічкою в затишній атмосфері.</p>
      </div>
    </section>

    <section class="info-section fade-in">
      <h3>Про нас</h3>
      <p>Ми — мережа кав’ярень COFFEEBOSS у самому серці Чернігова. 16 затишних місць, де кожен може насолодитися улюбленим напоєм.</p>
      <p>Наші двері відкриті для вас щодня з <strong>6:30 до 22:00</strong>.</p>
    </section>

    <section class="map-section fade-in">
      <h3>Наші кав’ярні на мапі</h3>
      <img src="/map.png" alt="Мапа наших кав’ярень" class="map-image zoomable">
    </section>

    <section class="order-section fade-in">
      <h3>Порядок замовлення кави</h3>
      <div class="progress-container">
        <div class="progress" :style="{ width: progressWidth }"></div>
        <div v-for="(step, index) in steps" :key="index" :class="['circle', { active: index < activeIndex, current: index === activeIndex - 1 }]">
          {{ index + 1 }}
        </div>
      </div>
      <button class="btn" @click="prevStep" :disabled="activeIndex === 1">Previous</button>
      <button class="btn" @click="nextStep" :disabled="activeIndex === steps.length">Next</button>
      <p>{{ steps[activeIndex - 1] }}</p>
    </section>

    <section class="loyalty-section fade-in">
      <div class="card">
        <div class="img-container">
          <img src="/point.jpg" alt="Бали" />
        </div>
        <section class="content">
          <h3>Програма лояльності</h3>
          <p>
            Отримуйте бали за кожне замовлення! За кожне оформлене замовлення ви отримуєте 1 бал. 10 грн = 1 бал. Ви можете витратити бали на майбутні замовлення або обміняти їх на наші товари:
          </p>
          <ul>
            <li>Чашка = 70 балів</li>
            <li>Шоппер = 30 балів</li>
          </ul>
          <p>
            Щоб замовити обмін, натисніть на зображення балу в правому верхньому куті. Там ви можете обрати, аби чашку доставили на будь-яку кав’ярню чи на відділення НП, але доставка за ваш рахунок.
          </p>
          <p>
            Ви також можете перевести реальні картки в електронний вигляд, взявши їх з собою до кав’ярні, де наші баристи додадуть вам балів. Можна додати балів, проходячи міні-ігри, які так само можна активувати, натиснувши на бал в правому верхньому куті екрану. Якщо хочете взяти фізичну картку замість електронної, скажіть про це баристі.
          </p>
        </section>
      </div>
    </section>

    <section class="gallery-section fade-in">
      <h3>Обмінюй бали та вдягай любов до кави</h3>
      <div class="container">
        <div class="clip clip1" :style="{ backgroundImage: 'url(/shopper_black.jpg)' }"></div>
        <div class="clip clip2" :style="{ backgroundImage: 'url(/chashka.jpg)' }"></div>
        <div class="clip clip3" :style="{ backgroundImage: 'url(/shopper_purple.jpg)' }"></div>
      </div>
    </section>

    <section class="accordion-section fade-in">
      <h3>Дізнайтеся більше про COFFEEBOSS</h3>
      <ul id="accordion">
        <li v-for="(item, index) in accordionItems" :key="index">
          <div
              class="accordion-header"
              @click="toggleAccordion(index)"
              :class="{ active: item.isOpen }"
          >
            {{ item.title }}
            <span class="arrow" :class="{ rotated: item.isOpen }">›</span>
          </div>
          <transition name="accordion">
            <div class="accordion-content" v-show="item.isOpen">
              <p>{{ item.content }}</p>
            </div>
          </transition>
        </li>
      </ul>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      activeIndex: 1,
      steps: [
        'Оберіть кавярню на вкладці меню.',
        'Оберіть каву чи випічку.',
        'Натисніть "Оформити замовлення".',
        'Оновіть сторінку та перейдіть на вкладку "Мої замовлення".',
        'Перевірте замовлення.',
        'Оплатіть картою, балами чи за рахунок послуги "Щасливий чек".',
        'У випадку проблем перевірте вкладку "Оплата", де зберігаються ваші чеки.',
        'Отримайте своє замовлення та насолоджуйтесь ним!',
        'За ваше замовлення отримаєте 1 бал, який можна буде використати для оплати подальших замовлень.'
      ],
      accordionItems: [
        {
          title: 'Хто ми?',
          content: 'COFFEEBOSS — це мережа затишних кав\'ярень у Чернігові, де кожен може насолодитися якісною кавою та вишуканою випічкою. Ми прагнемо створювати атмосферу затишку та гарного настрою для наших гостей.',
          isOpen: false
        },
        {
          title: 'Наша історія',
          content: 'Наша перша кав\'ярня відкрилася у 2015 році. З того часу ми постійно розвиваємося, щоб задовольнити смаки наших клієнтів. Сьогодні у нас 16 закладів у різних куточках міста.',
          isOpen: false
        },
        {
          title: 'Наші особливості',
          content: 'Ми використовуємо лише найкращі сорти кави з етично вирощених плантацій. Наша випічка готується щодня з натуральних інгредієнтів. Також ми пропонуємо безглютенові та веганські страви.',
          isOpen: false
        },
        {
          title: 'Графік роботи',
          content: 'Наші двері відкриті для вас щодня з 6:30 до 22:00.',
          isOpen: false
        }
      ]
    };
  },

  computed: {
    progressWidth() {
      return ((this.activeIndex - 1) / (this.steps.length - 1)) * 100 + '%';
    }
  },
  methods: {
    nextStep() {
      if (this.activeIndex < this.steps.length) {
        this.activeIndex++;
      }
    },
    prevStep() {
      if (this.activeIndex > 1) {
        this.activeIndex--;
      }
    },
    toggleAccordion(index) {
      this.accordionItems[index].isOpen = !this.accordionItems[index].isOpen;
    },
    handleIntersection(entries, observer) {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }
  },
  mounted() {
    const observer = new IntersectionObserver(this.handleIntersection, {
      threshold: 0.1
    });

    const fadeInElements = this.$el.querySelectorAll('.fade-in');
    fadeInElements.forEach(element => {
      observer.observe(element);
    });
  }
};
</script>

<style scoped>
.home-page {
  background-color: #121212;
  color: #ffffff;
  padding: 40px;
  max-width: 1100px;
  margin: auto;
  font-family: 'Arial', sans-serif;
}

.header-section {
  text-align: center;
  margin-bottom: 40px;
}

.logo-container {
  display: inline-block;
  border: 2px solid #fff;
  border-radius: 50%;
  padding: 10px;
  margin-bottom: 20px;
}

.logo {
  width: 150px;
  height: auto;
}

h1 {
  font-size: 2.8rem;
  color: #ffb703;
}

.welcome-text {
  font-size: 1.6rem;
  color: #ffdd57;
}

.hero-content h2 {
  font-size: 2.2rem;
  color: #ffffff;
}

.hero-content p {
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.cta-button {
  background-color: #ffb703;
  color: #121212;
  padding: 12px 20px;
  border-radius: 6px;
  font-size: 1.2rem;
  text-decoration: none;
}

.info-section {
  text-align: center;
  margin: 40px 0;
}

.map-section {
  text-align: center;
  margin-bottom: 40px;
}

.map-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.map-image.zoomable:hover {
  transform: scale(1.25);
}

.order-section {
  text-align: center;
  margin-bottom: 40px;
}

.order-section h3 {
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: #ffb703;
}

.progress-container {
  display: flex;
  justify-content: space-between;
  position: relative;
  margin-bottom: 30px;
  max-width: 100%;
  width: 800px;
  margin: 0 auto;
}

.progress-container::before {
  content: "";
  background-color: #e0e0e0; /* Сірий колір для неактивних ліній */
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
  height: 4px;
  width: 100%;
  z-index: -1;
}

.progress {
  background-color: #ffb703; /* Червоний колір для активних ліній */
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
  height: 4px;
  width: 0%;
  z-index: -1;
  transition: 0.4s ease;
}

.circle {
  position: relative;
  background-color: #fff;
  color: #999;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 3px solid #e0e0e0; /* Сірий колір для неактивних кружків */
  transition: 0.4s ease;
  z-index: 1;
}

.circle.active {
  border-color: #ffb703; /* Червоний колір для активних кружків */
}

.circle.current {
  background-color: #ff4500; /* Червоний колір для активного кружка */
  color: #fff;
  border-color: #ff0000; /* Червоний колір для активного кружка */
}

.btn {
  background-color: #ffb703;
  color: #121212;
  border: 0;
  font-family: inherit;
  padding: 8px 30px;
  margin: 5px;
  font-size: 14px;
  cursor: pointer;
}

.btn:active {
  transform: scale(0.98);
}

.btn:disabled {
  background-color: #e0e0e0;
  cursor: not-allowed;
}

.loyalty-section {
  text-align: center;
  margin-bottom: 40px;
}

.loyalty-section h3 {
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: #ffb703;
}

.loyalty-section p {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.loyalty-section ul {
  list-style-type: none;
  padding: 0;
}

.loyalty-section ul li {
  font-size: 1.2rem;
  margin-bottom: 5px;
}

.loyalty-image {
  max-width: 100px;
  height: auto;
  margin-bottom: 20px;
  border-radius: 8px;
}

.gallery-section {
  text-align: center;
  margin-bottom: 40px;
}

.container {
  position: relative;
  width: 800px;
  height: 500px;
  background: #222;
  margin: 0 auto;
}

.clip {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transition: all 0.5s;
  background-size: cover;
  background-position: center;
}

.clip1 {
  clip-path: polygon(0 0, 46% 0, 39% 100%, 0 100%);
}

.clip2 {
  clip-path: polygon(19% 0, 87% 0, 64% 100%, 33% 100%);
}

.clip3 {
  clip-path: polygon(82% 0, 100% 0, 100% 100%, 63% 100%);
}

.container:hover .clip {
  clip-path: polygon(100% 0, 100% 0, 100% 100%, 100% 100%);
}

.container .clip:hover {
  clip-path: polygon(0 0, 100% 0, 100% 100%, 0% 100%);
}

.features-section {
  display: flex;
  gap: 20px;
  justify-content: space-between;
}

.feature {
  background-color: #1e1e1e;
  padding: 20px;
  border-radius: 8px;
  flex: 1;
  text-align: center;
  transition: transform 0.3s ease;
}

.feature:hover {
  transform: translateY(-5px);
}

.feature h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #ffb703;
}

.feature p {
  font-size: 1rem;
  color: #cccccc;
}

.feature-link {
  display: inline-block;
  margin-top: 10px;
  color: #ffdd57;
  text-decoration: none;
  font-weight: bold;
}

.fade-in {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 1s ease-out, transform 1s ease-out;
}

.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}

/* Additional styles for the loyalty card */
.card {
  position: relative;
  width: 32rem;
  height: 42rem;
  background-color: black;
  box-shadow: 0px 30px 30px rgba(0, 0, 0, 0.5);
  margin: 0 auto;
}

.content {
  position: absolute;
  bottom: 0px;
  width: 80%;
  height: 10px;
  background: crimson;
  left: 10%;
  text-align: center;
  transition: 0.5s;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.content h3 {
  font-size: 30px;
  text-transform: uppercase;
  margin: 25px;
  color: #fff;
}

.content p, .content ul {
  width: 80%;
  margin: 10px auto;
  font-size: 18px;
  transition: 0.5s;
  opacity: 0;
  line-height: 25px;
  color: #fff;
}

.content ul {
  list-style-type: none;
  padding: 0;
}

.content ul li {
  margin-bottom: 5px;
}

.img-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transition: 1s;
}

.img-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: 1s;
}

.card:hover .content {
  height: 100%;
  width: 100%;
  left: 0;
}

.card:hover p,
.card:hover ul,
.card:hover ul li {
  opacity: 1;
  transition-delay: 0.5s;
}

.card:hover img {
  opacity: 0;
}
.accordion-section {
  text-align: center;
  margin-bottom: 40px;
}

#accordion {
  list-style: none;
  padding: 0;
  max-width: 600px;
  margin: 0 auto;
}

.accordion-header {
  background: #ffb703;
  color: #121212;
  padding: 15px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 5px;
  margin-top: 5px;
}

.accordion-content {
  background: #fff;
  color: #121212;
  padding: 10px;
  border-radius: 5px;
  margin-top: 3px;
}

.arrow {
  transition: transform 0.3s ease;
}

.rotated {
  transform: rotate(90deg);
}
</style>