<template>
  <div class="points-options-overlay">
    <div class="points-options-content">
      <button class="close-button" @click="close">&times;</button>
      <div class="points-blocks">
        <div
            class="points-block"
            @click="selectComponent('PointsGames')"
            @mouseover="hoverBlock('games')"
            @mouseleave="leaveBlock('games')"
            :class="{ hovered: hoveredBlock === 'games' }"
        >
          <h3>Міні-ігри</h3>
        </div>
        <div
            class="points-block"
            @click="openPointsChange"
            @mouseover="hoverBlock('change')"
            @mouseleave="leaveBlock('change')"
            :class="{ hovered: hoveredBlock === 'change' }"
        >
          <h3>Обмін балів</h3>
        </div>
      </div>
      <component
          :is="selectedComponent"
          v-if="selectedComponent"
          @close="closeSelectedComponent"
      ></component>
    </div>
    <PointsChange v-if="showPointsChange" @close="closePointsChange" :userId="userId" :username="username" :points="points" />
  </div>
</template>

<script>
import PointsChange from './PointsChange.vue';

export default {
  name: 'PointsOptions',
  components: { PointsChange },
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
      hoveredBlock: null,
      selectedComponent: null,
      showPointsChange: false,
    };
  },
  methods: {
    close() {
      this.$emit('close');
    },
    async selectComponent(componentName) {
      if (componentName === 'PointsGames') {
        const PointsGames = await import('./PointsGames.vue');
        this.selectedComponent = PointsGames.default;
      }
    },
    closeSelectedComponent() {
      this.selectedComponent = null;
    },
    openPointsChange() {
      this.showPointsChange = true;
    },
    closePointsChange() {
      this.showPointsChange = false;
    },
    hoverBlock(block) {
      this.hoveredBlock = block;
    },
    leaveBlock(block) {
      if (this.hoveredBlock === block) {
        this.hoveredBlock = null;
      }
    },
  },
};
</script>

<style scoped>
.points-options-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.points-options-content {
  background: linear-gradient(135deg, #ffffff, #f1f1f1);
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  position: relative;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  width: 400px;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 20px;
  color: #555;
  cursor: pointer;
  transition: color 0.3s;
}

.close-button:hover {
  color: #d9534f;
}

.points-blocks {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
  gap: 15px;
}

.points-block {
  padding: 20px;
  background: white;
  border-radius: 10px;
  width: 50%;
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.points-block.hovered {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
}

.points-block h3 {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
}
</style>
