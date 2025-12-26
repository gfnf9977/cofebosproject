<template>
  <div class="chat-container">
    <h2 class="chat-title">Чат з адміністратором</h2>
    <div v-if="loading" class="loader-container">
      <div class="coffee-cup">
        <img src="/coffeboss.png" alt="Coffeboss" class="coffee-image" />
      </div>
    </div>
    <div v-else>
      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="messages.length > 0" class="messages-container" ref="messagesContainer">
        <div v-for="message in messages" :key="message.id" class="message-wrapper">
          <div :class="['message', message.sender_id === senderId ? 'message-right' : 'message-left']">
            <strong>{{ message.sender_name }}:</strong> {{ message.content }}
            <br>
            <small>{{ message.message_time }}</small>
          </div>
          <div v-if="message.sender_id === senderId" class="message-actions">
            <div @click="editMessage(message)" class="pencil-icon-container">
              <i class="pencil-icon"></i>
            </div>
            <div @click="deleteMessage(message.id)" class="icon-trash">
              <div class="trash-lid"></div>
              <div class="trash-container"></div>
              <div class="trash-line-1"></div>
              <div class="trash-line-2"></div>
              <div class="trash-line-3"></div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="no-messages">Повідомлень не знайдено.</div>
      <div v-if="!editingMessage" class="new-message-container">
        <textarea v-model="newMessage" placeholder="Введіть ваше повідомлення тут..." class="message-input"></textarea>
        <img src="/send.png" alt="Send" @click="sendMessage" class="send-button" />
        <div class="predefined-phrases">
          <h3>Заздалегідь визначені фрази:</h3>
          <button v-for="phrase in predefinedPhrases" :key="phrase" @click="insertPhrase(phrase)" class="phrase-button">
            {{ phrase }}
          </button>
        </div>
        <div class="emoji-section">
          <h3>Емоджі:</h3>
          <button v-for="emoji in emojis" :key="emoji" @click="insertEmoji(emoji)" class="emoji-button">
            {{ emoji }}
          </button>
        </div>
      </div>
      <div v-if="editingMessage" class="edit-message-container">
        <textarea v-model="editingMessage.content" placeholder="Редагуйте ваше повідомлення тут..." class="message-input"></textarea>
        <div class="edit-buttons-container">
          <div @click="saveEditedMessage" class="check-icon-container">
            <i class="check-icon"></i>
          </div>
          <div @click="cancelEdit" class="ban-circle-icon-container">
            <i class="ban-circle-icon"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserConnect',
  data() {
    return {
      messages: [],
      newMessage: '',
      loading: true,
      error: null,
      senderId: this.$parent.userId,
      supportId: 1,
      userDetails: {},
      editingMessage: null,
      predefinedPhrases: [
        'Добрий день!',
        'Вітаю!',
        'А поясніть, будь ласка, який нині статус замовлення, яке я проводив ()',
        'Зрозуміло, дякую',
        'Я б хотів змінити в своїй анкеті ',
        'Я хочу змінити пароль',
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
      await this.fetchMessages();
      this.scrollToBottom();
    } catch (error) {
      this.error = 'Помилка з\'єднання з API';
    } finally {
      setTimeout(() => {
        this.loading = false;
      }, 3000);
    }
  },
  methods: {
    async fetchMessages() {
      if (!this.senderId || !this.supportId) {
        this.error = 'ID відправника та ID підтримки повинні бути встановлені';
        return;
      }

      try {
        const response = await fetch(`http://localhost:5000/api/get-messages?sender_id=${this.senderId}&receiver_id=${this.supportId}`);
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
      const userIds = new Set([this.senderId, this.supportId]);
      messages.forEach(message => {
        userIds.add(message.sender_id);
        userIds.add(message.receiver_id);
      });

      await this.fetchUserDetails(Array.from(userIds));

      return messages.map(message => ({
        ...message,
        sender_name: this.userDetails[message.sender_id]?.fullName || 'Невідомо',
        receiver_name: this.userDetails[message.receiver_id]?.fullName || 'Невідомо',
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
      if (!this.newMessage.trim()) {
        this.error = 'Повідомлення не може бути порожнім';
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
            receiver_id: this.supportId,
            content: this.newMessage,
          }),
        });

        if (response.ok) {
          this.newMessage = '';
          await this.fetchMessages();
          this.scrollToBottom();
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
          this.scrollToBottom();
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
        this.error = 'Зміст повідомлення не може бути порожнім';
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
          this.scrollToBottom();
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
    insertEmoji(emoji) {
      this.newMessage += emoji + ' ';
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },
  },
};
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chat-title {
  color: #333;
  font-size: 24px;
  margin-bottom: 20px;
  text-align: center;
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.coffee-cup {
  width: 200px;
  height: 200px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.coffee-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.error-message {
  color: red;
  margin-bottom: 20px;
  text-align: center;
}

.messages-container {
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
}

.message-wrapper {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.message {
  padding: 10px;
  border-radius: 5px;
  max-width: 70%;
  word-wrap: break-word;
  position: relative;
}

.message-left {
  background-color: #f1f1f1;
  align-self: flex-start;
  text-align: left;
}

.message-right {
  background-color: #007bff;
  color: white;
  align-self: flex-end;
  text-align: right;
}

.message-actions {
  display: flex;
  gap: 30px;
  margin-left: 10px;
  align-items: center;
}

.pencil-icon-container {
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  margin-top: 20px;
}

.pencil-icon {
  display: inline-block;
  position: relative;
  width: 6px;
  height: 20px;
  background: #000;
  transform: rotate(45deg);
}

.pencil-icon:after {
  content: '';
  position: absolute;
  border: 3px solid rgba(0, 0, 0, 0);
  border-top-color: #000;
  top: 105%;
  left: 0;
}

.pencil-icon:before {
  content: '';
  position: absolute;
  width: 6px;
  height: 5px;
  background: #000;
  top: -7px;
  left: 0;
}

.icon-trash {
  width: 48px;
  height: 48px;
  position: relative;
  overflow: hidden;
  margin-left: 25px;
  margin-bottom: 25px;
  cursor: pointer;
  margin-top: 30px;
}

.icon-trash .trash-lid {
  width: 62%;
  height: 10%;
  position: absolute;
  left: 50%;
  margin-left: -31%;
  top: 10.5%;
  background-color: #ff0000;
  border-top-left-radius: 80%;
  border-top-right-radius: 80%;
  transform: rotate(-5deg);
}

.icon-trash .trash-lid:after {
  content: "";
  width: 26%;
  height: 100%;
  position: absolute;
  left: 50%;
  margin-left: -13%;
  margin-top: -10%;
  background-color: inherit;
  border-top-left-radius: 30%;
  border-top-right-radius: 30%;
  transform: rotate(-1deg);
}

.icon-trash .trash-container {
  width: 56%;
  height: 65%;
  position: absolute;
  left: 50%;
  margin-left: -28%;
  bottom: 10%;
  background-color: #ff0000;
  border-bottom-left-radius: 15%;
  border-bottom-right-radius: 15%;
}

.icon-trash .trash-container:after {
  content: "";
  width: 110%;
  height: 12%;
  position: absolute;
  left: 50%;
  margin-left: -55%;
  top: 0;
  background-color: inherit;
  border-bottom-left-radius: 45%;
  border-bottom-right-radius: 45%;
}

.icon-trash .trash-line-1 {
  width: 4%;
  height: 50%;
  position: absolute;
  left: 38%;
  margin-left: -2%;
  bottom: 17%;
  background-color: #252527;
}

.icon-trash .trash-line-2 {
  width: 4%;
  height: 50%;
  position: absolute;
  left: 50%;
  margin-left: -2%;
  bottom: 17%;
  background-color: #252527;
}

.icon-trash .trash-line-3 {
  width: 4%;
  height: 50%;
  position: absolute;
  left: 62%;
  margin-left: -2%;
  bottom: 17%;
  background-color: #252527;
}

.no-messages {
  text-align: center;
  margin-bottom: 20px;
  color: #666;
}

.new-message-container,
.edit-message-container {
  margin-bottom: 20px;
}

.message-input {
  width: 100%;
  height: 100px;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
}

.send-button {
  width: 48px;
  height: 48px;
  cursor: pointer;
  border: none;
  background: none;
}

.send-button:hover {
  opacity: 0.8;
}

.edit-message-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.edit-buttons-container {
  display: flex;
  gap: 20px; /* Збільшена відстань між кнопками */
  justify-content: flex-end;
}

.check-icon-container,
.ban-circle-icon-container {
  cursor: pointer;
  display: inline-block;
}

.check-icon {
  display: inline-block;
  width: 5px;
  height: 17px;
  border-right: 5px solid #00ff00;
  border-bottom: 5px solid #00ff00;
  transform: rotate(45deg);
}

.ban-circle-icon {
  width: 25px;
  height: 25px;
  display: inline-block;
  position: relative;
  border: 5px solid #ff0000;
  border-radius: 100%;
}

.ban-circle-icon:after {
  content: '';
  position: absolute;
  width: 5px;
  height: 100%;
  background: #ff0000;
  top: 0;
  left: 10px;
  transform: rotate(45deg);
}

.predefined-phrases,
.emoji-section {
  margin-top: 20px;
}

.phrase-button,
.emoji-button {
  background: none;
  border: 1px solid #007bff;
  color: #007bff;
  cursor: pointer;
  margin-right: 10px;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 14px;
}

.phrase-button:hover,
.emoji-button:hover {
  background-color: #007bff;
  color: white;
}
</style>