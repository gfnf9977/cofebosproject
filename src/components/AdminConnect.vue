<template>
  <div>
    <h2>Чат</h2>
    <div v-if="loading">Завантаження...</div>
    <div v-if="error">{{ error }}</div>
    <div v-if="messages.length > 0">
      <div v-for="message in messages" :key="message.id" :class="['message', message.sender_id === senderId ? 'sent' : 'received']">
        <strong>{{ message.sender_name }}:</strong> {{ message.content }}
        <br>
        <small>{{ message.message_time }}</small>
        <div v-if="message.sender_id === senderId">
          <button @click="editMessage(message)">Редагувати</button>
          <button @click="deleteMessage(message.id)">Видалити</button>
        </div>
      </div>
    </div>
    <div v-else>Повідомлень не знайдено.</div>
    <div>
      <label for="recipient">Виберіть отримувача:</label>
      <select v-model="selectedReceiverId" id="recipient">
        <option v-for="user in filteredUsers" :key="user.id" :value="user.id">
          {{ user.fullName }}
        </option>
      </select>
    </div>
    <div v-if="!editingMessage && selectedReceiverId">
      <textarea v-model="newMessage" placeholder="Введіть ваше повідомлення тут..."></textarea>
      <button @click="sendMessage">Надіслати</button>
      <div>
        <h3>Заздалегідь визначені фрази:</h3>
        <button v-for="phrase in predefinedPhrases" :key="phrase" @click="insertPhrase(phrase)">
          {{ phrase }}
        </button>
      </div>
    </div>
    <div v-if="editingMessage">
      <textarea v-model="editingMessage.content" placeholder="Редагуйте ваше повідомлення тут..."></textarea>
      <button @click="saveEditedMessage">Зберегти</button>
      <button @click="cancelEdit">Скасувати</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminConnect',
  data() {
    return {
      messages: [],
      newMessage: '',
      loading: false,
      error: null,
      senderId: this.$parent.userID, // Use the userID from the parent component
      selectedReceiverId: null, // Selected receiver ID
      users: [], // List of users for the dropdown
      userDetails: {}, // Store user details by ID
      editingMessage: null, // Message being edited
      predefinedPhrases: [
        'Добрий день!',
        'Вітаю!',
        'Зрозумів, дякую',
        'А перегляньте, будь-ласка, яка ситуація по оплаті замовлення з ID = ',
        'Дякую за зауваження. обов\'язково зробимо висновки',
        'Почув вас, колего',
        'У нас недостача (), просимо направити додатково',
        'Звертаюсь з приводу перенаправленого кандидата',
      ],
    };
  },
  async mounted() {
    this.loading = true;
    try {
      await this.fetchUsers();
      if (this.selectedReceiverId) {
        await this.fetchMessages();
      }
    } catch (error) {
      this.error = 'Помилка з\'єднання з API';
    } finally {
      this.loading = false;
    }
  },
  computed: {
    filteredUsers() {
      return this.users.filter(user => user.id !== this.senderId);
    },
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await fetch('http://localhost:5000/api/get-prime-admin-users');
        if (response.ok) {
          const users = await response.json();
          this.users = users.map(user => ({
            ...user,
            fullName: `${user.last_name} ${user.first_name} ${user.middle_name}`,
          }));
        } else {
          this.error = 'Не вдалося завантажити користувачів';
        }
      } catch (error) {
        this.error = 'Помилка з\'єднання з API';
      }
    },
    async fetchMessages() {
      if (!this.senderId || !this.selectedReceiverId) {
        this.error = 'ID відправника та отримувача повинні бути встановлені';
        return;
      }

      try {
        const response = await fetch(`http://localhost:5000/api/get-messages?sender_id=${this.senderId}&receiver_id=${this.selectedReceiverId}`);
        if (response.ok) {
          const messages = await response.json();
          this.messages = await this.addUserDetailsToMessages(messages);
        } else {
          this.error = 'Не вдалося завантажити повідомлення';
        }
      } catch (error) {
        this.error = 'Помилка з\'єднання з API';
      }
    },
    async addUserDetailsToMessages(messages) {
      const userIds = new Set([this.senderId, this.selectedReceiverId]);
      messages.forEach(message => {
        userIds.add(message.sender_id);
        userIds.add(message.receiver_id);
      });

      await this.fetchUserDetails(Array.from(userIds));

      return messages.map(message => ({
        ...message,
        sender_name: this.userDetails[message.sender_id]?.fullName || 'Невідомий',
        receiver_name: this.userDetails[message.receiver_id]?.fullName || 'Невідомий',
      }));
    },
    async fetchUserDetails(userIds) {
      for (const userId of userIds) {
        if (this.userDetails[userId]) continue;

        try {
          const response = await fetch(`http://localhost:5000/api/user-profile-by-id/${userId}`);
          if (response.ok) {
            const userData = await response.json();
            this.userDetails[userId] = {
              ...userData,
              fullName: `${userData.last_name} ${userData.first_name} ${userData.middle_name}`,
            };
          } else {
            this.error = 'Не вдалося завантажити дані користувача';
          }
        } catch (error) {
          this.error = 'Помилка з\'єднання з API';
        }
      }
    },
    async sendMessage() {
      if (!this.newMessage.trim() || !this.selectedReceiverId) {
        this.error = 'Повідомлення не може бути порожнім і отримувач повинен бути вибраний';
        return;
      }

      try {
        const response = await fetch('http://localhost:5000/api/send-message', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            sender_id: this.senderId,
            receiver_id: this.selectedReceiverId,
            content: this.newMessage,
          }),
        });

        if (response.ok) {
          this.newMessage = '';
          await this.fetchMessages();
        } else {
          this.error = 'Не вдалося надіслати повідомлення';
        }
      } catch (error) {
        this.error = 'Помилка з\'єднання з API';
      }
    },
    async deleteMessage(messageId) {
      try {
        const response = await fetch(`http://localhost:5000/api/delete-message/${messageId}`, {
          method: 'DELETE',
        });

        if (response.ok) {
          await this.fetchMessages();
        } else {
          this.error = 'Не вдалося видалити повідомлення';
        }
      } catch (error) {
        this.error = 'Помилка з\'єднання з API';
      }
    },
    editMessage(message) {
      this.editingMessage = { ...message };
    },
    async saveEditedMessage() {
      if (!this.editingMessage.content.trim()) {
        this.error = 'Вміст повідомлення не може бути порожнім';
        return;
      }

      try {
        const response = await fetch(`http://localhost:5000/api/update-message/${this.editingMessage.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            content: this.editingMessage.content,
          }),
        });

        if (response.ok) {
          this.editingMessage = null;
          await this.fetchMessages();
        } else {
          this.error = 'Не вдалося оновити повідомлення';
        }
      } catch (error) {
        this.error = 'Помилка з\'єднання з API';
      }
    },
    cancelEdit() {
      this.editingMessage = null;
    },
    insertPhrase(phrase) {
      this.newMessage += phrase + ' ';
    },
  },
  watch: {
    selectedReceiverId: 'fetchMessages',
  },
};
</script>

<style scoped>
h2 {
  color: #333;
}

.message {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
  max-width: 70%;
  word-wrap: break-word;
}

.message.sent {
  background-color: #dcf8c6;
  align-self: flex-end;
  text-align: right;
}

.message.received {
  background-color: #f1f0f0;
  align-self: flex-start;
  text-align: left;
}

textarea {
  width: 100%;
  height: 100px;
  margin-bottom: 10px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

label {
  margin-right: 10px;
}

select {
  margin-bottom: 10px;
}
</style>