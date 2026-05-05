<script setup lang="ts">
defineProps<{
  score: number
  total: number
}>()

const emit = defineEmits<{
  retry: []
}>()
</script>

<template>
  <div class="quiz-result">
    <p class="score-label">测验结束！</p>
    <p class="score">{{ score }} / {{ total }}</p>
    <p class="rate">正确率 {{ Math.round((score / total) * 100) }}%</p>
    <div class="actions">
      <button class="btn-primary" @click="emit('retry')">再来一次</button>
      <RouterLink to="/review" class="btn-secondary">去复习</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.quiz-result {
  text-align: center;
}

.score-label {
  font-size: 18px;
  color: #555;
  margin-bottom: 8px;
}

.score {
  font-size: 48px;
  font-weight: 700;
  color: #4f46e5;
  margin: 0;
}

.rate {
  font-size: 16px;
  color: #888;
  margin-bottom: 24px;
}

.actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-primary {
  padding: 10px 24px;
  background: #4f46e5;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover { background: #4338ca; }

.btn-secondary {
  padding: 10px 24px;
  border: 2px solid #e5e5e5;
  border-radius: 8px;
  font-size: 15px;
  color: #555;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-secondary:hover {
  border-color: #4f46e5;
  color: #4f46e5;
}
</style>
