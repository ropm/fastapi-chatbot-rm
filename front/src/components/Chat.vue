<template>
<div>
  <font-awesome-icon icon="comment-dots" class="open-button" v-on:click="chatHidden = !chatHidden" v-if="chatHidden"/>
      <div class="chat-popup" v-if="!chatHidden">
        <form @submit="sendMessage">
          <div class="chat-header">
            <h2>Chat with the Fidsbot</h2>
            <span class="close-button"><font-awesome-icon icon="times" v-on:click="chatHidden = !chatHidden"/></span>
            </div>
            <div class="all-all-container">
            <div class="all-container" v-for="msg in messages" v-bind:key="msg.id">
                <div class="sent-msg" 
                v-bind:class="{'bot-container': msg.source === 'bot', 'you-container': msg.source === 'user'}">
                    {{msg.message}}
                </div>
            </div>
            </div>
            <div class="typing" v-if="thinking">Typing...</div>

            <textarea placeholder="Type a message" name="message" v-model="typedMessage" required></textarea>

            <button type="submit" class="btn">Send</button>
        </form>
      </div>
</div>
</template>

<script>
import axios from 'axios';
import { v4 as uuid } from 'uuid';

export default {
  name: 'Chat',
  data () {
      return {
          chatHidden: true,
          typedMessage: '',
          thinking: false,
          messages: [{id: uuid(), source: 'bot', message: 'Hello there! What can I help you with today?'}]
      }
  },
  methods: {
      async sendMessage (e, reSendMsg = null) {
          e.preventDefault();
          if (this.typedMessage === '' && !reSendMsg) {
            return;
          }
          let msgToSend;
          if (reSendMsg) {
            msgToSend = reSendMsg;
          } else {
            msgToSend = {
                id: uuid(),
                source: 'user',
                message: this.typedMessage
            }
            this.typedMessage = '';
            this.messages.push(msgToSend);
            this.thinking = true;
          }

          const config = {
              baseURL: 'https://chat-lw-test.herokuapp.com/api'
          }
          try {
              const res = await axios.get(`/chat/${msgToSend.message}`, config);
              if (res.status === 200) {
                const botMsg = {
                      id: uuid(),
                      source: 'bot',
                      message: res.data.bot
                  }
                  this.messages.push(botMsg);
                  this.thinking = false;
              } else {
                this.thinking = false;
                console.warn('Something has gone wrong with bot response!', res.status)
              }
          } catch(err) {
            const trained = await this.sendTrain(config);
            if (trained && trained.success) {
              this.sendMessage(e, msgToSend)
            } else {
              this.messages.push({id: uuid(), source: 'bot', message: 'I am unfortunately down for maintenance... :-('})
              this.thinking = false;
            }
          }
      },
      async sendTrain(conf) {
        try {
          const trainRes = await axios.get('/train?epochs=3000', conf);
          if (trainRes.status === 200) {
            return {'success': true}
          } else {
            return {'success': false}
          }
        } catch(err) {
          this.messages.push({id: uuid(), source: 'bot', message: 'I am unfortunately down for maintenance... :-('})
          this.thinking = false;
        }
      }
  }
}
</script>

<style scoped>

/* Button used to open the chat form - fixed at the bottom of the page */
.open-button {
  background-color: #b83a3a;
  padding: 16px 20px;
  border: none;
  cursor: pointer;
  opacity: 0.9;
  position: fixed;
  bottom: 23px;
  right: 28px;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  display: block;
}

.bot-container {
    padding: 10px;
    text-align: left;
}

.you-container {
    padding: 10px;
    text-align: right;
    font-weight: bold;
}

.sent-msg {
    display: block;
    border: 3px solid #f1f1f1;
}

.chat-header {
  display: flex;
  direction: row;
  justify-content: space-between;
  margin-left: 1%;
}

.close-button {
  cursor: pointer;
}

/* The popup chat - hidden by default */
.chat-popup {
  position: fixed;
  bottom: 0;
  right: 15px;
  border: 3px solid #f1f1f1;
  z-index: 9;
  padding: 10px;
  background-color: white;
  max-width: 85vw;
  overflow: scroll;
}

.all-all-container {
  max-height: 50vh;
  overflow: auto;
}

/* Full-width textarea */
.chat-popup textarea {
  width: 90%;
  padding: 15px;
  margin: 5px 0 22px 0;
  border: none;
  background: #f1f1f1;
  resize: none;
}

/* When the textarea gets focus, do something */
.chat-popup textarea:focus {
  background-color: #ddd;
  outline: none;
}

/* Set a style for the submit/login button */
.chat-popup .btn {
  background-color: #b83a3a;
  color: white;
  padding: 16px 20px;
  border: none;
  cursor: pointer;
  width: 100%;
  margin-bottom:10px;
  opacity: 0.8;
}

/* Add some hover effects to buttons */
.chat-popup .btn:hover, .open-button:hover {
  opacity: 1;
}
</style>
