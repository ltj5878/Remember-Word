<script setup lang="ts">
import WordForm from '../components/WordForm.vue'
</script>

<template>
  <div class="page">
    <div class="card">
      <h2>录入新单词</h2>
      <WordForm />
    </div>
  </div>
</template>

<style scoped>
h2 {
  margin: 0 0 20px;
  font-size: 18px;
  color: #333;
}
</style>
