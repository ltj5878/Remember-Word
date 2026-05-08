<script setup lang="ts">
import type { QuizQuestion } from '../composables/useApi'

interface WrongAnswer {
  question: QuizQuestion
  selectedIndex: number
}

defineProps<{
  score: number
  total: number
  wrongAnswers: WrongAnswer[]
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

    <div v-if="wrongAnswers.length > 0" class="wrong-list">
      <h3 class="wrong-title">错题回顾（{{ wrongAnswers.length }}）</h3>
      <ul>
        <li v-for="(w, i) in wrongAnswers" :key="i" class="wrong-item">
          <p class="wrong-original">{{ w.question.original }}</p>
          <p class="wrong-line">
            <span class="label">你的答案：</span>
            <span class="your-answer">{{ w.question.options[w.selectedIndex] }}</span>
          </p>
          <p class="wrong-line">
            <span class="label">正确答案：</span>
            <span class="correct-answer">{{ w.question.options[w.question.answer_index] }}</span>
          </p>
        </li>
      </ul>
    </div>

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

.wrong-list {
  text-align: left;
  max-width: 500px;
  margin: 0 auto 24px;
  background: #fafafa;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 16px 20px;
}

.wrong-title {
  margin: 0 0 12px;
  font-size: 16px;
  color: #dc2626;
}

.wrong-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.wrong-item {
  padding: 12px 0;
  border-bottom: 1px dashed #e5e5e5;
}

.wrong-item:last-child {
  border-bottom: none;
}

.wrong-original {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 6px;
}

.wrong-line {
  font-size: 14px;
  margin: 2px 0;
  color: #555;
}

.label {
  color: #888;
}

.your-answer {
  color: #dc2626;
}

.correct-answer {
  color: #16a34a;
  font-weight: 600;
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
