<template>
  <div class="points-change-overlay">
    <div class="points-change-content">
      <button class="close-button" @click="close">×</button>
      <div class="side-nav">
        <div class="user-info">
          <p>Користувач: {{ username }}</p>
          <p>Кількість балів: {{ points }}</p>
        </div>
        <button
            @click="changeOption('ShopperComponent')"
            :class="{ active: selectedOption === 'ShopperComponent' }"
        >
          <img src="/shopper.png" alt="Шоппер" class="tab-icon" />
          <span>Шоппер</span>
        </button>
        <button
            @click="changeOption('CupComponent')"
            :class="{ active: selectedOption === 'CupComponent' }"
        >
          <img src="/cup.png" alt="Чашка" class="tab-icon" />
          <span>Чашка</span>
        </button>
      </div>
      <div class="main-content">
        <component :is="selectedOption" :userId="userId"></component>
      </div>
    </div>
  </div>
</template>

<script>
import ShopperComponent from './ShopperComponent.vue';
import CupComponent from './CupComponent.vue';

export default {
  name: 'PointsChange',
  components: {
    ShopperComponent,
    CupComponent,
  },
  props: {
    userId: {
      type: Number,
      required: true,
    },
    username: {
      type: String,
      required: true,
    },
    points: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      selectedOption: 'ShopperComponent',
      options: ['ShopperComponent', 'CupComponent'],
    };
  },
  methods: {
    close() {
      this.$emit('close');
    },
    changeOption(option) {
      this.selectedOption = option;
    },
  },
};
</script>

<style scoped>
.points-change-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.points-change-content {
  background: white;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  position: relative;
  display: flex;
  width: 90%;
  height: 90%;
  max-width: 1200px;
  max-height: 800px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.close-button {
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: #ff4757;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  padding: 10px;
  width: 40px;
  height: 40px;
  font-size: 20px;
  line-height: 20px;
  transition: background-color 0.3s ease;
}

.close-button:hover {
  background-color: #ff6b81;
}

.side-nav {
  width: 250px;
  background: #2f3542;
  padding: 20px;
  border-radius: 8px 0 0 8px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.user-info {
  margin-bottom: 20px;
  text-align: left;
  color: #ffffff;
}

.user-info p {
  margin: 5px 0;
  font-size: 16px;
  color: #ffffff;
}

.side-nav button {
  background: none;
  border: none;
  padding: 15px;
  cursor: pointer;
  width: 100%;
  text-align: left;
  font-size: 18px;
  color: #ffffff;
  display: flex;
  align-items: center;
  transition: background-color 0.3s ease;
  border-radius: 5px;
}

.side-nav button.active {
  background-color: #57606f;
}

.side-nav button:hover {
  background-color: #747d8c;
}

.tab-icon {
  width: 30px;
  height: 30px;
  margin-right: 10px;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
  text-align: left;
  background: #f1f2f6;
  border-radius: 0 8px 8px 0;
}

.main-content h1 {
  margin-top: 0;
  color: #2f3542;
}

.main-content p {
  color: #57606f;
}
</style>