<template>
  <div class="stores-page">
    <h2>Наші кав'ярні</h2>
    <div v-if="loading" class="loader-container">
      <div class="loader"></div>
    </div>
    <div v-else class="store-cards">
      <div class="store-card" v-for="store in stores" :key="store.id">
        <div class="store-info">
          <h3>{{ store.Street }}, {{ store.nomer }}</h3>
          <p>{{ store.loc_desc }}</p>
        </div>
        <div class="store-media">
          <img :src="store.photo1" alt="Photo 1" class="store-photo">
          <iframe
              :src="getMapUrl(store.id)"
              class="store-map"
              allowfullscreen=""
              loading="lazy"
              referrerpolicy="no-referrer-when-downgrade">
          </iframe>
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
      loading: true // Loading state
    };
  },
  async mounted() {
    try {
      const response = await fetch('http://localhost:5000/api/shops'); // Змініть URL за потреби
      if (response.ok) {
        this.stores = await response.json();
      } else {
        console.error('Помилка завантаження даних:', response.statusText);
      }
    } catch (error) {
      console.error('Помилка підключення до API:', error);
    } finally {
      this.loading = false; // Hide the loader
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
        21: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d768.1298914321636!2d31.297962085459233!3d51.49206668252707!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46d548edc6da79b1%3A0x389c8fa5afe3481!2z0JvQvtC60L7Qt9Cw0LLQvtC00YHQutC-0Lkg0YDQsNC50L7QvSwg0J_QsNGA0LjQutC80LDRhdC10YDRgdC60LDRjw!5e1!3m2!1sru!2sua!4v1737237917783!5m2!1sru!2sua',
      };
      return mapUrls[id] || '';
    }
  }
};
</script>

<style scoped>
.stores-page {
  padding: 20px;
  background: linear-gradient(135deg, #e6e6e6, #ffffff);
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  position: relative; /* Ensure the loader is positioned relative to this container */
}

h2 {
  color: #444;
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: bold;
}

.store-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.store-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  width: 300px;
  transition: transform 0.2s ease;
}

.store-card:hover {
  transform: translateY(-10px);
}

.store-info {
  padding: 20px;
  text-align: center;
}

.store-info h3 {
  margin: 0 0 10px;
  font-size: 18px;
  color: #333;
}

.store-info p {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.store-media {
  position: relative;
}

.store-photo {
  width: 100%;
  height: auto;
}

.store-map {
  width: 100%;
  height: 200px;
  border: 0;
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8); /* Semi-transparent background */
}

.loader {
  width: 50px;
  aspect-ratio: 1;
  display: grid;
  -webkit-mask: conic-gradient(from 15deg, #0000, #000);
  animation: l26 1s infinite steps(12);
  background:
      radial-gradient(closest-side at 50% 12.5%,
      #000 96%, #0000) 50% 0/20% 80% repeat-y,
      radial-gradient(closest-side at 12.5% 50%,
      #000 96%, #0000) 0 50%/80% 20% repeat-x;
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
  100% { transform: rotate(1turn); }
}
</style>