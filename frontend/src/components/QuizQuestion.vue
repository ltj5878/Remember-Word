<script setup lang="ts">
import { ref } from 'vue'
import type { QuizQuestion } from '../composables/useApi'

const props = defineProps<{
  question: QuizQuestion
  index: number
  total: number
}>()

const emit = defineEmits<{
  answer: [correct: boolean]
}>()

const selected = ref<number | null>(null)
const answered = ref(false)

function select(i: number) {
  if (answered.value) return
  selected.value = i
  answered.value = true
  setTimeout(() => {
    emit('answer', i === props.question.answer_index)
  }, 1000)
}

function optionClass(i: number) {
  if (!answered.value) return ''
  if (i === props.question.answer_index) return 'correct'
  if (i === selected.value) return 'wrong'
  return ''
}
</script>

<template>
  <div class="quiz-question">
    <p class="progress">第 {{ index + 1 }} / {{ total }} 题</p>
    <p class="original">{{ question.original }}</p>
    <div class="options">
      <button
        v-for="(opt, i) in question.options"
        :key="i"
        class="option-btn"
        :class="optionClass(i)"
        :disabled="answered"
        @click="select(i)"
      >
        {{ opt }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.quiz-question {
  text-align: center;
}

.progress {
  color: #888;
  font-size: 14px;
  margin-bottom: 8px;
}

.original {
  font-size: 22px;
  font-weight: 600;
  color: #333;
  margin-bottom: 24px;
  line-height: 1.5;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 400px;
  margin: 0 auto;
}

.option-btn {
  padding: 12px 20px;
  font-size: 16px;
  border: 2px solid #e5e5e5;
  background: #fff;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: #333;
}

.option-btn:hover:not(:disabled) {
  border-color: #4f46e5;
}

.option-btn:disabled {
  cursor: default;
}

.option-btn.correct {
  border-color: #16a34a;
  background: #f0fdf4;
  color: #16a34a;
}

.option-btn.wrong {
  border-color: #dc2626;
  background: #fef2f2;
  color: #dc2626;
}
</style>
