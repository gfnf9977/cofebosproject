<template>
  <div class="container">
    <h2>Чат</h2>
    <div v-if="loading">Завантаження...</div>
    <div v-if="error">{{ error }}</div>
    <div class="chat-list">
      <input v-model="searchQuery" placeholder="Пошук за прізвищем" class="search-input" />
      <div v-for="user in filteredUsers" :key="user.id" class="chat-item" @click="selectReceiver(user.id)">
        <strong>{{ user.fullName }}</strong>
        <p>{{ getLatestMessage(user.id) }}</p>
      </div>
    </div>
    <div v-if="selectedReceiverId" class="message-container">
      <div v-for="message in messages" :key="message.id" :class="['message', message.sender_id === senderId ? 'sent' : 'received']">
        <strong>{{ message.sender_name }}:</strong> {{ message.content }}
        <br>
        <small>{{ message.message_time }}</small>
        <div v-if="message.sender_id === senderId" class="message-actions">
          <button @click="editMessage(message)">Редагувати</button>
          <button @click="deleteMessage(message.id)">Видалити</button>
        </div>
      </div>
    </div>
    <div v-else>Виберіть отримувача для початку чату.</div>
    <div v-if="selectedReceiverId" class="input-container">
      <div v-if="!editingMessage">
        <textarea v-model="newMessage" placeholder="Введіть ваше повідомлення тут..."></textarea>
        <button @click="sendMessage">Надіслати</button>
        <div class="predefined-phrases">
          <h3>Заздалегідь визначені фрази:</h3>
          <button v-for="phrase in predefinedPhrases" :key="phrase" @click="insertPhrase(phrase)">
            {{ phrase }}
          </button>
        </div>
        <div class="emoji-section">
          <h3>Емоджі:</h3>
          <button v-for="emoji in emojis" :key="emoji" @click="insertEmoji(emoji)">
            {{ emoji }}
          </button>
        </div>
      </div>
      <div v-if="editingMessage">
        <textarea v-model="editingMessage.content" placeholder="Редагуйте ваше повідомлення тут..."></textarea>
        <button @click="saveEditedMessage">Зберегти</button>
        <button @click="cancelEdit">Скасувати</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PrimeConnect',
  data() {
    return {
      messages: [],
      newMessage: '',
      loading: false,
      error: null,
      senderId: 1, // Replace with actual sender ID
      selectedReceiverId: null, // Selected receiver ID
      users: [], // List of users for the chat list
      userDetails: {}, // Store user details by ID
      editingMessage: null, // Message being edited
      searchQuery: '', // Search query for filtering users
      predefinedPhrases: [
        'Добрий день!',
        'Вітаю!',
        'Вітаємо!',
        'Поясніть, що у вас відбулось із замовленням, ID = ',
        'Зрозуміло, дякую',
        'Все буде враховано при розрахунку вашого заробітку',
        'Колеги, давайте уважніше в майбутньому!)',
        'Дякую за відгук!',
        'Дякую за зауваження. Обов\'язково зробимо висновки',
        'Почув вас, колеги',
        'Замовлення опрацьовано',
        'Очікуйте надходження товару (дата) ближче до (час)',
        'Звертаюсь з приводу поданої вами анкети',
        'До вас має сьогоднішні завітати потенційний кандидат на роботу, розкажи йому про основні аспекти',
        'Команда Coffeboss щиро вітає вас з днем народження та дарує 7 бонусних балів на ваш баланс. Нехай ваше свято стане найкращим та найсвітлішим днем у цьому році'
      ],
      emojis: [
        '😊', '👍', '👋', '❤️', '😂', '🤔',
        '😃', '😱', '😮', '😈', '😇', '😋',
        '😌', '😘', '😜', '😝', '😞', '😟',
        '😠', '😡', '😢', '😣', '😤', '😥',
        '😪', '😫', '😴', '😌', '😵', '😶',
        '😐', '😑', '😒', '🙄', '🤔', '😬',
        '🤐', '🤑', '🤒', '🤕', '🤖', '🤗',
        '🤠', '🤢', '🤧', '🤨', '🤩', '🤪',
        '🤫', '🤬', '🤭', '🤮', '🤯', '🤰',
        '🤱', '🤲', '🤳', '🤴', '🤵', '🤶',
        '🤷', '🤸', '🤹', '🤺', '🤼', '🤽',
        '🤾', '🤿', '🥀', '🥁', '🥂', '🥃',
        '🥄', '🥅', '🥆', '🥇', '🥈', '🥉',
      ],
    };
  },
  async mounted() {
    this.loading = true;
    try {
      await this.fetchUsers();
      await this.fetchMessages();
    } catch (error) {
      this.error = 'Помилка з\'єднання з API';
    } finally {
      this.loading = false;
    }
  },
  computed: {
    filteredUsers() {
      return this.users.filter(user =>
          user.fullName.toLowerCase().includes(this.searchQuery.toLowerCase()) && user.id !== this.senderId
      );
    },
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await fetch('http://localhost:5000/api/get_all_users');
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
      if (!this.selectedReceiverId) return;

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
            this.error = 'Не вдалося завантажити деталі користувача';
          }
        } catch (error) {
          this.error = 'Помилка з\'єднання з API';
        }
      }
    },
    async sendMessage() {
      if (!this.newMessage.trim() || !this.selectedReceiverId) {
        this.error = 'Повідомлення не може бути порожнім і отримувач має бути вибраний';
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
      const receiverName = this.userDetails[this.selectedReceiverId]?.fullName || 'Невідомий';
      this.newMessage += phrase.replace('{{receiverName}}', receiverName) + ' ';
    },
    insertEmoji(emoji) {
      this.newMessage += emoji + ' ';
    },
    selectReceiver(userId) {
      this.selectedReceiverId = userId;
      this.fetchMessages();
    },
    getLatestMessage(userId) {
      const messages = this.messages.filter(message => message.sender_id === userId || message.receiver_id === userId);
      return messages.length > 0 ? messages[messages.length - 1].content : '';
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
  text-align: center;
  margin-bottom: 20px;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.chat-list {
  width: 100%;
  max-width: 600px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
  overflow-y: auto;
  max-height: 300px;
}

.search-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
}

.chat-item {
  padding: 10px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.3s;
}

.chat-item:hover {
  background-color: #e0e0e0;
}

.chat-item strong {
  font-weight: bold;
}

.chat-item p {
  margin: 0;
  color: #666;
}

.message-container {
  width: 100%;
  max-width: 600px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.message {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 10px;
  background-color: #fff;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s;
  max-width: 70%;
  word-wrap: break-word;
  position: relative;
}

.message:hover {
  background-color: #e0e0e0;
}

.message strong {
  font-weight: bold;
}

.message small {
  color: #999;
  font-size: 0.8em;
}

.message-actions {
  display: none;
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: rgba(0, 0, 0, 0.7);
  border-radius: 5px;
  padding: 5px;
}

.message:hover .message-actions {
  display: flex;
  gap: 5px;
}

.message-actions button {
  padding: 5px 10px;
  background-color: #ff6347;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.message-actions button:hover {
  background-color: #ff4500;
}

.sent {
  align-self: flex-end;
  background-color: #dcf8c6;
}

.received {
  align-self: flex-start;
  background-color: #fff;
}

.input-container {
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

textarea {
  width: 100%;
  height: 100px;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
  resize: vertical;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3;
}

.predefined-phrases,
.emoji-section {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.predefined-phrases button,
.emoji-section button {
  background-color: #28a745;
}

.predefined-phrases button:hover,
.emoji-section button:hover {
  background-color: #218838;
}
</style>
