<template>
  <div class="stores-page">
    <h2>Наші кав'ярні</h2>
    <div v-if="loading" class="loading-animation">
      <span class="loader"></span>
    </div>
    <div v-else class="store-cards-container">
      <div class="store-cards" :style="{ transform: `translateX(-${activeIndex * 320}px)` }">
        <div
            class="store-card"
            :class="{ active: activeStoreId === store.id, adjacent: isAdjacent(store.id) }"
            v-for="store in stores"
            :key="store.id"
            @click="setActiveStore(store.id)"
        >
          <div class="store-info">
            <h3>{{ store.Street }}, {{ store.nomer }}</h3>
            <p>{{ store.loc_desc }}</p>
          </div>
          <div class="store-media">
            <img :src="store.photo1" alt="Photo 1" class="store-image">
            <iframe
                :src="getMapUrl(store.id)"
                width="600"
                height="450"
                style="border:0;"
                allowfullscreen=""
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade">
            </iframe>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
export default {
  name: 'StoresPage',
  data() {
    return {
      stores: [], // Дані для кав'ярень
      loading: true, // Loading state
      activeStoreId: null, // Active store ID
    };
  },
  computed: {
    activeIndex() {
      return this.stores.findIndex(store => store.id === this.activeStoreId);
    },
  },
  async mounted() {
    try {
      const response = await fetch('http://localhost:5000/api/shops'); // Змініть URL за потреби
      if (response.ok) {
        this.stores = await response.json();
        if (this.stores.length > 0) {
          this.activeStoreId = this.stores[0].id; // Set the first store as active by default
        }
      } else {
        console.error('Помилка завантаження даних:', response.statusText);
      }
    } catch (error) {
      console.error('Помилка підключення до API:', error);
    } finally {
      this.loading = false; // Update loading state
    }
  },
  methods: {
    getMapUrl(id) {
      const mapUrls = {
        1: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1082.4264269615535!2d31.301268777630547!3d51.49150388619877!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d54990cdb6e86f%3A0xee8a4db483adabae!2sCoffee%20Boss%20Dram!5e1!3m2!1sru!2sua!4v1737229612896!5m2!1sru!2sua',
        2: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3306.070063905522!2d31.27692040606485!3d51.512170697893986!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d5495a2991abc5%3A0x646fa506faef438d!2sCOFFEE%20BOSS!5e1!3m2!1sru!2sua!4v1737238444726!5m2!1sru!2sua',
        3: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d21217.844088919923!2d31.298464551673995!3d51.51091046219868!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d5494e34a35aed%3A0xff8dd937c709a002!2sCoffee%20Boss!5e1!3m2!1sru!2sua!4v1737236934139!5m2!1sru!2sua',
        6: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d21217.844088919923!2d31.298464551673995!3d51.51091046219868!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d54966cd4f1771%3A0xf1751752c37c2dfa!2sCoffee%20Boss!5e1!3m2!1sru!2sua!4v1737236969936!5m2!1sru!2sua',
        7: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d21134.355569075753!2d31.222076850932808!3d51.52796013420703!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d5464c745f31f5%3A0xffd652eff4f3e4e5!2sCoffee%20Boss!5e1!3m2!1sru!2sua!4v1737237009140!5m2!1sru!2sua',
        9: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d21134.355569075753!2d31.222076850932808!3d51.52796013420703!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d5473caf5af5e9%3A0x2f6e074e8fc49be7!2sCOFFEE%20BOSS%20MSN!5e1!3m2!1sru!2sua!4v1737237052336!5m2!1sru!2sua',
        10: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d12470.442972670746!2d31.26712796219871!3d51.5055648157651!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d549b2cbc0bd5d%3A0x18d038b3870177fc!2sCoffee%20Boss!5e1!3m2!1sru!2sua!4v1737237285259!5m2!1sru!2sua',
        11: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d12470.442972670746!2d31.26712796219871!3d51.5055648157651!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d549bc00ba3987%3A0x35e52073f116e91b!2sCoffee%20Boss!5e1!3m2!1sru!2sua!4v1737237324501!5m2!1sru!2sua',
        12: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d12490.525048005931!2d31.27219123403353!3d51.50204461806711!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d549e02156c073%3A0x9f63ad2a42e52f8b!2sCoffee%20Boss!5e1!3m2!1sru!2sua!4v1737237358094!5m2!1sru!2sua',
        15: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d12490.525048005931!2d31.27219123403353!3d51.50204461806711!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d54953a434c43f%3A0x39df7cbc48efd9cf!2sCoffee%20Boss!5e1!3m2!1sru!2sua!4v1737237628874!5m2!1sru!2sua',
        16: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d12490.525048005931!2d31.27219123403353!3d51.50204461806711!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d549c2bc1b6837%3A0xf3bb83e91fceadb7!2sCoffee%20Boss!5e1!3m2!1sru!2sua!4v1737237695729!5m2!1sru!2sua',
        17: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d12490.525048005931!2d31.27219123403353!3d51.50204461806711!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d549fdbc9a06bd%3A0xf8ea924ec8851cd4!2sCoffee%20Boss%20Progress%202!5e1!3m2!1sru!2sua!4v1737237753489!5m2!1sru!2sua',
        18: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d12485.635851824365!2d31.28862428249251!3d51.49000360690746!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d549b0011b4bbd%3A0xe4f0679d4838d7b7!2sCoffee%20boss!5e1!3m2!1sru!2sua!4v1737237795706!5m2!1sru!2sua',
        19: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d25270.598628679618!2d31.256738069631723!3d51.508914878295116!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d54900046c6773%3A0x495d065acba8f5!2sCoffee%20Boss!5e1!3m2!1sru!2sua!4v1737237842383!5m2!1sru!2sua',
        20: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d25270.598628679618!2d31.256738069631723!3d51.508914878295116!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d549e144ef8c6d%3A0xd8aece2d023919c5!2sCoffee%20Boss!5e1!3m2!1sru!2sua!4v1737237879043!5m2!1sru!2sua',
        21: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d768.1298914321636!2d31.297962085459233!3d51.49206668252707!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d548edc6da79b1%3A0x389c8fa5afe3481!2sz0JvQvtC60L7Qt9Cw0LLQvtC00YHQutC-0Lkg0YDQsNC50L7QvSwg0J_QsNGA0LjQutC80LDRhdC10YDRgdC60LDRjw!5e1!3m2!1sru!2sua!4v1737237917783!5m2!1sru!2sua',
      };
      return mapUrls[id] || '';
    },
    setActiveStore(id) {
      this.activeStoreId = id;
    },
    isAdjacent(id) {
      const index = this.stores.findIndex(store => store.id === this.activeStoreId);
      const adjacentIndices = [index - 1, index + 1];
      return adjacentIndices.includes(this.stores.findIndex(store => store.id === id));
    },
  },
};
</script>

<style scoped>
.stores-page {
  padding: 40px;
  background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
  border-radius: 16px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  font-family: 'Arial', sans-serif;
  overflow: hidden;
}

h2 {
  color: #2c3e50;
  text-align: center;
  font-size: 36px;
  margin-bottom: 40px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  position: relative;
}

h2::after {
  content: '';
  position: absolute;
  width: 100px;
  height: 4px;
  background: #FF3D00;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 2px;
}

.store-cards-container {
  overflow: hidden;
  position: relative;
  width: 100%;
}

.store-cards {
  display: flex;
  gap: 20px;
  transition: transform 0.5s ease-in-out;
}

.store-card {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  width: 300px;
  transition: transform 0.3s ease, box-shadow 0.3s ease, flex 0.3s ease;
  flex: 0 0 auto;
  cursor: pointer;
  position: relative;
}

.store-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 61, 0, 0.1);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 12px;
}

.store-card:hover::before {
  opacity: 1;
}

.store-card.active {
  flex: 1 0 1100px;
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.store-card.adjacent {
  flex: 1 0 400px;
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.store-info {
  padding: 20px;
  text-align: center;
  position: relative;
  z-index: 1;
}

.store-info h3 {
  margin: 0 0 15px;
  font-size: 24px;
  color: #34495e;
  font-weight: 600;
  transition: color 0.3s ease;
}

.store-card.active .store-info h3 {
  color: #FF3D00;
}

.store-info p {
  margin: 0;
  font-size: 18px;
  color: #7f8c8d;
  line-height: 1.5;
}

.store-media {
  text-align: center;
  padding: 15px;
}

.store-media img {
  display: block;
  margin: 0 auto 15px;
  border-radius: 8px;
  width: 100%;
  max-width: 280px;
  height: auto;
  transition: transform 0.3s ease;
}

.store-card.active .store-media img {
  transform: scale(1.1);
}

.store-media iframe {
  display: block;
  margin: 0 auto;
  width: 100%;
  height: 250px;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.store-card.active .store-media iframe {
  transform: scale(1.1);
}

.loading-animation {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 500px;
}

.loader {
  position: relative;
  width: 200px;
  height: 240px;
  background-image: radial-gradient(circle 50px, #000 100%, transparent 0),
  radial-gradient(circle 10px, #000 100%, transparent 0),
  radial-gradient(circle 10px, #000 100%, transparent 0),
  linear-gradient(#000 40px, transparent 0);
  background-position: center 210px , 150px 170px , 30px 30px, center 190px;
  background-size: 100px 100px, 20px 20px , 20px 20px , 8px 28px;
  background-repeat: no-repeat;
  z-index: 10;
  perspective: 1000px;
}

.loader::before {
  content: '';
  position: absolute;
  width: 180px;
  height: 180px;
  border-radius:50%;
  border: 6px solid #000;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -55%) rotate(-45deg);
  border-right-color: transparent;
  box-sizing: border-box;
}

.loader::after {
  content: '';
  position: absolute;
  height: 140px;
  width: 140px;
  transform: translate(-50%, -55%) rotate(-45deg) rotateY(0deg);
  left: 50%;
  top: 50%;
  box-sizing: border-box;
  border: 12px solid #FF3D00;
  border-radius:50%;
  animation: rotate 0.5s linear infinite;
}

@keyframes rotate {
  to{transform: translate(-50%, -55%) rotate(-45deg) rotateY(360deg)}
}
</style>