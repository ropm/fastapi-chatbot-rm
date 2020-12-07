<template>
  <div class="message-item">
    <p>
      <input type="checkbox" v-on:change="markComplete" v-bind:checked="todo.completed">
      {{todo.title}}
      <button @click="$emit('send-message', todo.id)" class="del">x</button>
      </p>
  </div>
</template>

<script>
export default {
  name: "Message",
  props: ["message"],
  methods: {}
}
</script>

<style scoped>

</style>