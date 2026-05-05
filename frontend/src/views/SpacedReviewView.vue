<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApi, type Word } from '../composables/useApi'

const { getTodayReview, submitReviewResult, toggleDifficult } = useApi()

type Phase = 'loading' | 'reviewing' | 'done'
const phase = ref<Phase>('loading')
const words = ref<Word[]>([])
const currentIndex = ref(0)
const results = ref<{ word: Word; correct: boolean; nextDays: number }[]>([])
const showAnswer = ref(false)

const currentWord = computed(() => words.value[currentIndex.value])
const progress = computed(() => `${currentIndex.value + 1} / ${words.value.length}`)
const correctCount = computed(() => results.value.filter(r => r.correct).length)

async function loadReview() {
  phase.value = 'loading'
  words.value = await getTodayReview()
  currentIndex.value = 0
  results.value = []
  showAnswer.value = false
  phase.value = words.value.length > 0 ? 'reviewing' : 'done'
}

function reveal() {
  showAnswer.value = true
}

async function answer(correct: boolean) {
  const word = currentWord.value
  const res = await submitReviewResult(word.id, correct)
  results.value.push({ word, correct, nextDays: res.new_interval_days })

  if (currentIndex.value + 1 < words.value.length) {
    currentIndex.value++
    showAnswer.value = false
  } else {
    phase.value = 'done'
  }
}

async function handleToggleDifficult() {
  const word = currentWord.value
  const updated = await toggleDifficult(word.id, !word.is_difficult)
  words.value[currentIndex.value] = updated
}

onMounted(loadReview)
</script>

<template>
  <div class="page">
    <div class="card">
      <!-- Loading -->
      <p v-if="phase === 'loading'" class="center-text">加载中...</p>

      <!-- Reviewing -->
      <template v-if="phase === 'reviewing'">
        <div class="review-header">
          <p class="progress">{{ progress }}</p>
          <button
            class="btn-star"
            :class="{ active: currentWord.is_difficult }"
            @click="handleToggleDifficult"
            :title="currentWord.is_difficult ? '取消困难标记' : '标记为困难'"
          >{{ currentWord.is_difficult ? '★' : '☆' }}</button>
        </div>

        <div class="word-card">
          <p class="word-original">{{ currentWord.original }}</p>
          <div v-if="showAnswer" class="word-answer">
            <p class="word-translation">{{ currentWord.translation }}</p>
          </div>
          <button v-else class="btn-reveal" @click="reveal">显示答案</button>
        </div>

        <div v-if="showAnswer" class="answer-buttons">
          <button class="btn-wrong" @click="answer(false)">😕 不认识</button>
          <button class="btn-correct" @click="answer(true)">😊 认识</button>
        </div>

        <p class="review-info">
          已复习 {{ currentWord.review_count }} 次 · 间隔 {{ currentWord.interval_days }} 天
        </p>
      </template>

      <!-- Done -->
      <template v-if="phase === 'done'">
        <div class="done-section">
          <template v-if="results.length === 0">
            <p class="done-icon">🎉</p>
            <p class="done-text">今天没有需要复习的单词！</p>
            <p class="done-sub">去录入新单词或者做个测验吧</p>
          </template>
          <template v-else>
            <p class="done-icon">✅</p>
            <p class="done-text">今日复习完成！</p>
            <p class="done-score">{{ correctCount }} / {{ results.length }} 认识</p>
            <div class="result-list">
              <div
                v-for="(r, i) in results"
                :key="i"
                :class="['result-item', r.correct ? 'correct' : 'wrong']"
              >
                <span class="result-word">{{ r.word.original }}</span>
                <span class="result-next">下次: {{ r.nextDays }}天后</span>
              </div>
            </div>
          </template>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.center-text {
  text-align: center;
  color: #888;
  padding: 40px;
}

.review-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.progress {
  color: #888;
  font-size: 14px;
  margin: 0;
}

.btn-star {
  padding: 4px 8px;
  background: none;
  border: none;
  font-size: 22px;
  cursor: pointer;
  color: #ccc;
  transition: color 0.2s;
}

.btn-star.active { color: #f59e0b; }
.btn-star:hover { color: #f59e0b; }

.word-card {
  text-align: center;
  padding: 32px 16px;
  background: #f9fafb;
  border-radius: 12px;
  margin-bottom: 20px;
}

.word-original {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0 0 20px;
  line-height: 1.5;
}

.word-answer {
  border-top: 1px solid #e5e5e5;
  padding-top: 16px;
}

.word-translation {
  font-size: 20px;
  color: #4f46e5;
  margin: 0;
  line-height: 1.5;
}

.btn-reveal {
  padding: 10px 32px;
  font-size: 15px;
  border: 2px solid #4f46e5;
  background: #fff;
  color: #4f46e5;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-reveal:hover {
  background: #4f46e5;
  color: #fff;
}

.answer-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-bottom: 16px;
}

.btn-wrong,
.btn-correct {
  padding: 12px 32px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-wrong {
  background: #fef2f2;
  color: #dc2626;
}

.btn-wrong:hover {
  background: #fee2e2;
}

.btn-correct {
  background: #f0fdf4;
  color: #16a34a;
}

.btn-correct:hover {
  background: #dcfce7;
}

.review-info {
  text-align: center;
  color: #aaa;
  font-size: 13px;
  margin: 0;
}

/* Done section */
.done-section {
  text-align: center;
  padding: 20px 0;
}

.done-icon {
  font-size: 48px;
  margin: 0 0 8px;
}

.done-text {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0 0 4px;
}

.done-sub {
  color: #888;
  font-size: 14px;
  margin: 0;
}

.done-score {
  font-size: 16px;
  color: #4f46e5;
  margin: 0 0 16px;
}

.result-list {
  max-height: 300px;
  overflow-y: auto;
  text-align: left;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-radius: 6px;
  margin-bottom: 4px;
  font-size: 14px;
}

.result-item.correct {
  background: #f0fdf4;
}

.result-item.wrong {
  background: #fef2f2;
}

.result-word {
  color: #333;
  font-weight: 500;
}

.result-next {
  color: #888;
  font-size: 12px;
}
</style>
