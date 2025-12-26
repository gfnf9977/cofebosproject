<template>
  <div class="slider-container" ref="sliderContainer">
    <section class="left-slid" ref="leftSlid">
      <div class="shopper-two">
        <h1>Шоппер фіолетовий</h1>
      </div>
      <div class="shopper-one">
        <h1>Шоппер чорний</h1>
      </div>
    </section>

    <section class="right-slid" ref="rightSlid">
      <div class="img img-one">
        <img src="/shopper_black.jpg" alt="Шоппер чорний" />
      </div>
      <div class="img img-two">
        <img src="/shopper_purple.jpg" alt="Шоппер фіолетовий" />
      </div>
    </section>

    <section class="buttons-container">
      <button id="down-btn" @click="nextSlide('up')">&#8595;</button>
      <button id="up-btn" @click="nextSlide('down')">&#8593;</button>
    </section>

    <button class="order-button" @click="openModal">Замовити</button>

    <ShopperPay v-if="isModalOpen" :orderItem="orderItem" :userId="userId" @close="closeModal" />
  </div>
</template>

<script>
import ShopperPay from './ShopperPay.vue';

export default {
  name: 'ShopperComponent',
  components: {
    ShopperPay,
  },
  props: {
    userId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      activeSlideIndex: 0,
      sliderLength: 2, // Кількість слайдів
      isModalOpen: false,
    };
  },
  methods: {
    nextSlide(direction) {
      if (direction === 'up') {
        this.activeSlideIndex++;
        if (this.activeSlideIndex > this.sliderLength - 1) {
          this.activeSlideIndex = 0;
        }
      } else if (direction === 'down') {
        this.activeSlideIndex--;
        if (this.activeSlideIndex < 0) {
          this.activeSlideIndex = this.sliderLength - 1;
        }
      }

      this.updateSlidePositions();
    },
    updateSlidePositions() {
      if (this.$refs.sliderContainer && this.$refs.rightSlid && this.$refs.leftSlid) {
        const sliderHeight = this.$refs.sliderContainer.clientHeight;
        this.$refs.rightSlid.style.transform = `translateY(-${this.activeSlideIndex * sliderHeight}px)`;
        this.$refs.leftSlid.style.transform = `translateY(${this.activeSlideIndex * sliderHeight}px)`;
      }
    },
    openModal() {
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },
  },
  computed: {
    orderItem() {
      return this.activeSlideIndex === 0 ? 'Шоппер чорний' : 'Шоппер фіолетовий';
    },
  },
  mounted() {
    this.$nextTick(() => {
      if (this.$refs.leftSlid) {
        this.$refs.leftSlid.style.top = `-${(this.sliderLength - 1) * 100}vh`;
      }
    });
  },
};
</script>

<style scoped>
.slider-container {
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 100%;
}

.left-slid {
  height: 100%;
  width: 35%;
  position: absolute;
  top: 0;
  left: 0;
  transition: transform 0.8s ease-in-out;
}

.left-slid > div {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #000;
}

.left-slid h1 {
  font-size: 2.5rem;
}

.right-slid {
  height: 100%;
  position: absolute;
  top: 0;
  left: 35%;
  width: 65%;
  transition: transform 0.8s ease-in-out;
}

.right-slid > div {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.right-slid img {
  max-width: 80%; /* Зменшіть ширину зображення */
  max-height: 80%; /* Зменшіть висоту зображення */
  object-fit: contain; /* Збережіть пропорції зображення */
}

.buttons-container {
  position: absolute;
  left: 35%;
  top: 50%;
  transform: translateY(-50%);
}

.buttons-container button {
  border: none;
  cursor: pointer;
  padding: 10px;
  background: transparent;
  color: #000;
  font-size: 2.2rem;
}

#down-btn {
  transform: translateX(-100%);
}

#up-btn {
  transform: translateY(-100%);
}

.shopper-one {
  background-color: #f0f0f0;
}

.shopper-two {
  background-color: #e0e0e0;
}

.order-button {
  position: absolute;
  top: 20px; /* Adjust the position as needed */
  right: 20px; /* Adjust the position as needed */
  border: none;
  cursor: pointer;
  padding: 10px 20px;
  background-color: #007BFF;
  color: #fff;
  font-size: 1.2rem;
  border-radius: 5px;
  transition: background-color 0.3s ease;
  z-index: 10; /* Ensure the button is above other elements */
}

.order-button:hover {
  background-color: #0056b3;
}
</style>