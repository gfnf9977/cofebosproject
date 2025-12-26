<template>
  <div class="calculator-container">
    <div class="calculator">
      <h1>Калькулятор</h1>

      <div class="section">
        <div class="column">
          <h2>Монети</h2>
          <div class="input-group">
            <label for="denomination-10kop">10 коп:</label>
            <input type="number" id="denomination-10kop" v-model="denominations['10kop']" min="0" @focus="clearInput('10kop')" @blur="resetIfEmpty('10kop')" @input="limitDecimalPlaces('10kop'); calculateTotal()">
          </div>
          <div class="input-group">
            <label for="denomination-50kop">50 коп:</label>
            <input type="number" id="denomination-50kop" v-model="denominations['50kop']" min="0" @focus="clearInput('50kop')" @blur="resetIfEmpty('50kop')" @input="limitDecimalPlaces('50kop'); calculateTotal()">
          </div>
        </div>

        <div class="column">
          <h2>Монети/Купюри</h2>
          <div class="input-group">
            <label for="denomination-1">1 грн:</label>
            <input type="number" id="denomination-1" v-model="denominations['1']" min="0" @focus="clearInput('1')" @blur="resetIfEmpty('1')" @input="limitDecimalPlaces('1'); calculateTotal()">
          </div>
          <div class="input-group">
            <label for="denomination-2">2 грн:</label>
            <input type="number" id="denomination-2" v-model="denominations['2']" min="0" @focus="clearInput('2')" @blur="resetIfEmpty('2')" @input="limitDecimalPlaces('2'); calculateTotal()">
          </div>
          <div class="input-group">
            <label for="denomination-5">5 грн:</label>
            <input type="number" id="denomination-5" v-model="denominations['5']" min="0" @focus="clearInput('5')" @blur="resetIfEmpty('5')" @input="limitDecimalPlaces('5'); calculateTotal()">
          </div>
          <div class="input-group">
            <label for="denomination-10">10 грн:</label>
            <input type="number" id="denomination-10" v-model="denominations['10']" min="0" @focus="clearInput('10')" @blur="resetIfEmpty('10')" @input="limitDecimalPlaces('10'); calculateTotal()">
          </div>
        </div>

        <div class="column">
          <h2>Купюри</h2>
          <div class="input-group">
            <label for="denomination-20">20 грн:</label>
            <input type="number" id="denomination-20" v-model="denominations['20']" min="0" @focus="clearInput('20')" @blur="resetIfEmpty('20')" @input="limitDecimalPlaces('20'); calculateTotal()">
          </div>
          <div class="input-group">
            <label for="denomination-50">50 грн:</label>
            <input type="number" id="denomination-50" v-model="denominations['50']" min="0" @focus="clearInput('50')" @blur="resetIfEmpty('50')" @input="limitDecimalPlaces('50'); calculateTotal()">
          </div>
          <div class="input-group">
            <label for="denomination-100">100 грн:</label>
            <input type="number" id="denomination-100" v-model="denominations['100']" min="0" @focus="clearInput('100')" @blur="resetIfEmpty('100')" @input="limitDecimalPlaces('100'); calculateTotal()">
          </div>
          <div class="input-group">
            <label for="denomination-200">200 грн:</label>
            <input type="number" id="denomination-200" v-model="denominations['200']" min="0" @focus="clearInput('200')" @blur="resetIfEmpty('200')" @input="limitDecimalPlaces('200'); calculateTotal()">
          </div>
          <div class="input-group">
            <label for="denomination-500">500 грн:</label>
            <input type="number" id="denomination-500" v-model="denominations['500']" min="0" @focus="clearInput('500')" @blur="resetIfEmpty('500')" @input="limitDecimalPlaces('500'); calculateTotal()">
          </div>
          <div class="input-group">
            <label for="denomination-1000">1000 грн:</label>
            <input type="number" id="denomination-1000" v-model="denominations['1000']" min="0" @focus="clearInput('1000')" @blur="resetIfEmpty('1000')" @input="limitDecimalPlaces('1000'); calculateTotal()">
          </div>
        </div>
      </div>

      <div class="input-group">
        <label for="expectedAmount">Очікувана сума:</label>
        <input type="number" id="expectedAmount" v-model="expectedAmount" min="0" @input="calculateTotal()">
      </div>

      <div class="results">
        <div id="cashAmount" class="result neutral">Сума готівки: {{ cashAmount.toFixed(2) }}</div>
        <div id="expectedAmountResult" class="result neutral">Очікувана сума: {{ expectedAmount.toFixed(2) }}</div>
        <div id="difference" :class="['result', differenceClass]">Різниця: {{ difference.toFixed(2) }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      denominations: {
        '10kop': 0,
        '50kop': 0,
        '1': 0,
        '2': 0,
        '5': 0,
        '10': 0,
        '20': 0,
        '50': 0,
        '100': 0,
        '200': 0,
        '500': 0,
        '1000': 0,
      },
      expectedAmount: 0,
      cashAmount: 0,
      difference: 0,
    };
  },
  computed: {
    differenceClass() {
      return this.difference === 0 ? 'neutral' : this.difference > 0 ? 'positive' : 'negative';
    },
  },
  methods: {
    calculateTotal() {
      const cashAmount =
          this.denominations['10kop'] * 0.1 +
          this.denominations['50kop'] * 0.5 +
          this.denominations['1'] * 1 +
          this.denominations['2'] * 2 +
          this.denominations['5'] * 5 +
          this.denominations['10'] * 10 +
          this.denominations['20'] * 20 +
          this.denominations['50'] * 50 +
          this.denominations['100'] * 100 +
          this.denominations['200'] * 200 +
          this.denominations['500'] * 500 +
          this.denominations['1000'] * 1000;

      this.cashAmount = cashAmount;
      this.difference = cashAmount - this.expectedAmount;
    },
    clearInput(key) {
      if (this.denominations[key] === 0) {
        this.denominations[key] = '';
      }
    },
    resetIfEmpty(key) {
      if (this.denominations[key] === '') {
        this.denominations[key] = 0;
      }
      this.calculateTotal();
    },
    limitDecimalPlaces(key) {
      const value = this.denominations[key];
      const parts = value.toString().split('.');
      if (parts.length > 1 && parts[1].length > 2) {
        this.denominations[key] = parseFloat(parts[0] + '.' + parts[1].slice(0, 2));
      }
    },
  },
  mounted() {
    this.calculateTotal();
  },
};
</script>

<style scoped>
body {
  font-family: 'Arial', sans-serif;
  background-color: #ffffff; /* Білий фон */
  color: #333333; /* Темно-сірий текст */
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.calculator-container {
  background-color: #f0f0f0; /* Світло-сірий фон */
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  max-width: 900px;
  width: 100%;
  border-left: 8px solid #666666; /* Темно-сірий акцент */
  animation: fadeIn 0.5s ease-in-out;
  transition: background-color 0.3s ease, color 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.calculator h1 {
  font-size: 28px;
  margin-bottom: 20px;
  text-align: center;
  color: #444444; /* Темно-сірий */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  transition: color 0.3s ease;
}

.section {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
}

.input-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.input-group label {
  font-size: 18px;
  margin-right: 10px;
  color: #555555; /* Сірий */
  font-weight: bold;
  transition: color 0.3s ease;
}

.input-group input {
  width: 80px;
  padding: 8px;
  font-size: 18px;
  border: 1px solid #cccccc; /* Світло-сірий */
  border-radius: 8px;
  text-align: right;
  background-color: #ffffff; /* Білий */
  color: #333333; /* Темно-сірий */
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s ease, background-color 0.3s ease, color 0.3s ease;
}

.input-group input:focus {
  border-color: #666666; /* Темно-сірий */
  outline: none;
}

.column {
  width: 30%;
  margin-right: 2%;
}

.column h2 {
  font-size: 22px;
  margin-bottom: 15px;
  color: #444444; /* Темно-сірий */
  border-bottom: 3px solid #666666; /* Темно-сірий */
  padding-bottom: 5px;
  text-align: center;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  transition: color 0.3s ease, border-bottom-color 0.3s ease;
}

.results {
  clear: both;
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}

.result {
  width: 30%;
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, color 0.3s ease;
}

.result.negative {
  background-color: #ffcccc; /* Світло-червоний */
  color: #cc0000; /* Темно-червоний */
}

.result.positive {
  background-color: #ccffcc; /* Світло-зелений */
  color: #006600; /* Темно-зелений */
}

.result.neutral {
  background-color: #e0e0e0; /* Світло-сірий */
  color: #333333; /* Темно-сірий */
}

.close-button {
  color: #000000; /* Чорний */
  transition: color 0.3s ease;
}

.close-button:hover {
  color: #ff0000; /* Червоний */
}
</style>