<template>
<div>
  <button class="open-button" v-on:click="chatHidden = !chatHidden" v-if="chatHidden">Chat</button>
      <div class="chat-popup" v-if="!chatHidden">
        <form @submit="sendMessage">
            <h1>Chat with Sam the Bot</h1>
            <div class="all-container" v-for="msg in messages" v-bind:key="msg.id">
                <div class="sent-msg" 
                v-bind:class="{'bot-container': msg.source === 'bot', 'you-container': msg.source === 'user'}">
                    {{msg.message}}
                </div>
            </div>
            <div class="typing" v-if="thinking">Typing...</div>

            <textarea placeholder="Type a message" name="message" v-model="typedMessage" required></textarea>

            <button type="submit" class="btn">Send</button>
            <button type="button" class="btn cancel" v-on:click="chatHidden = !chatHidden">Hide</button>
        </form>
      </div>
</div>
</template>

<script>
import axios from 'axios';
import { v4 as uuid } from 'uuid';

export default {
  name: 'Chat',
  props: ['firstQuestions'],
  data () {
      return {
          chatHidden: true,
          typedMessage: '',
          thinking: false,
          messages: []
      }
  },
  methods: {
      sendMessage (e) {
          e.preventDefault();
          const typedMsg = {
              id: uuid(),
              source: 'user',
              message: this.typedMessage
          }
          this.typedMessage = '';
          this.messages.push(typedMsg);
          this.thinking = true;

          const config = {
              baseURL: 'http://localhost:8000/api'
          }
          axios.get(`/chat/${typedMsg.message}`, config)
            .then((res) => {
                const botMsg = {
                    id: uuid(),
                    source: 'bot',
                    message: res.data.bot
                }
                this.messages.push(botMsg);
                this.thinking = false;
            })
            .catch((err) => {
                console.error(err);
                this.thinking = false;
            })
      }
  }
}
</script>

<style scoped>

/* Button used to open the chat form - fixed at the bottom of the page */
.open-button {
  background-color: #f1f1f1;
  color: black;
  padding: 16px 20px;
  border: none;
  cursor: pointer;
  opacity: 0.8;
  position: fixed;
  bottom: 23px;
  right: 28px;
  width: 300px;
}

.bot-container {
    text-align: left;
}

.you-container {
    text-align: right;
}

.sent-msg {
    display: block;
    border: 3px solid #f1f1f1;
}

/* The popup chat - hidden by default */
.chat-popup {
  position: fixed;
  bottom: 0;
  right: 15px;
  border: 3px solid #f1f1f1;
  z-index: 9;
  max-width: 300px;
  padding: 10px;
  background-color: white;
}

/* Full-width textarea */
.chat-popup textarea {
  width: 90%;
  padding: 15px;
  margin: 5px 0 22px 0;
  border: none;
  background: #f1f1f1;
  resize: none;
  min-height: 60px;
}

/* When the textarea gets focus, do something */
.chat-popup textarea:focus {
  background-color: #ddd;
  outline: none;
}

/* Set a style for the submit/login button */
.chat-popup .btn {
  background-color: #4CAF50;
  color: white;
  padding: 16px 20px;
  border: none;
  cursor: pointer;
  width: 100%;
  margin-bottom:10px;
  opacity: 0.8;
}

/* Add a red background color to the cancel button */
.chat-popup .cancel {
  background-color: red;
}

/* Add some hover effects to buttons */
.chat-popup .btn:hover, .open-button:hover {
  opacity: 1;
}
</style>
