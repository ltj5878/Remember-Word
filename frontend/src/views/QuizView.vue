<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi, type QuizQuestion } from '../composables/useApi'
import QuizSetup from '../components/QuizSetup.vue'
import QuizQuestionComp from '../components/QuizQuestion.vue'
import QuizResult from '../components/QuizResult.vue'

const { getWordCount, getQuiz } = useApi()

type Phase = 'setup' | 'playing' | 'result'
export interface WrongAnswer {
  question: QuizQuestion
  selectedIndex: number
}
const phase = ref<Phase>('setup')
const wordCount = ref(0)
const questions = ref<QuizQuestion[]>([])
const currentIndex = ref(0)
const score = ref(0)
const wrongAnswers = ref<WrongAnswer[]>([])
const loading = ref(false)
const error = ref('')

async function loadCount() {
  wordCount.value = await getWordCount()
}

async function startQuiz(num: number, mode: string, difficultOnly: boolean) {
  loading.value = true
  error.value = ''
  try {
    questions.value = await getQuiz(num, mode, difficultOnly)
    currentIndex.value = 0
    score.value = 0
    wrongAnswers.value = []
    phase.value = 'playing'
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function handleAnswer(correct: boolean, selectedIndex: number) {
  if (correct) {
    score.value++
  } else {
    wrongAnswers.value.push({
      question: questions.value[currentIndex.value],
      selectedIndex,
    })
  }
  if (currentIndex.value + 1 < questions.value.length) {
    currentIndex.value++
  } else {
    phase.value = 'result'
  }
}

function retry() {
  phase.value = 'setup'
  loadCount()
}

onMounted(loadCount)
</script>

<template>
  <div class="page">
    <div class="card">
      <h2 v-if="phase === 'setup'">单词测验</h2>
      <p v-if="error" class="error">{{ error }}</p>

      <QuizSetup
        v-if="phase === 'setup'"
        :word-count="wordCount"
        :loading="loading"
        @start="startQuiz"
      />

      <QuizQuestionComp
        v-if="phase === 'playing'"
        :key="currentIndex"
        :question="questions[currentIndex]"
        :index="currentIndex"
        :total="questions.length"
        @answer="handleAnswer"
      />

      <QuizResult
        v-if="phase === 'result'"
        :score="score"
        :total="questions.length"
        :wrong-answers="wrongAnswers"
        @retry="retry"
      />
    </div>
  </div>
</template>

<style scoped>
h2 {
  margin: 0 0 20px;
  font-size: 18px;
  color: #333;
  text-align: center;
}

.error {
  text-align: center;
  color: #dc2626;
  font-size: 14px;
}
</style>
