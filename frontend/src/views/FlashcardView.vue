<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApi, type Word } from '../composables/useApi'

const { getFlashcards, getWordCount, toggleDifficult } = useApi()

type Phase = 'setup' | 'playing' | 'done'
const phase = ref<Phase>('setup')
const cards = ref<Word[]>([])
const currentIndex = ref(0)
const flipped = ref(false)
const wordCount = ref(0)
const difficultOnly = ref(false)
const knownCount = ref(0)
const unknownCount = ref(0)

const currentCard = computed(() => cards.value[currentIndex.value])
const animating = ref(false)

async function loadCount() {
  wordCount.value = await getWordCount()
}

async function startFlashcards(num: number) {
  cards.value = await getFlashcards(num, difficultOnly.value)
  if (cards.value.length === 0) return
  currentIndex.value = 0
  flipped.value = false
  animating.value = false
  knownCount.value = 0
  unknownCount.value = 0
  phase.value = 'playing'
}

function flip() {
  flipped.value = true
}

function next(known: boolean) {
  if (known) knownCount.value++
  else unknownCount.value++

  if (currentIndex.value + 1 < cards.value.length) {
    // Disable transition, reset to front, then re-enable transition
    animating.value = true
    flipped.value = false
    currentIndex.value++
    // Wait a frame for the DOM to update without animation
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        animating.value = false
      })
    })
  } else {
    phase.value = 'done'
  }
}

async function handleToggleDifficult() {
  const card = currentCard.value
  const updated = await toggleDifficult(card.id, !card.is_difficult)
  cards.value[currentIndex.value] = updated
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
      <!-- Setup -->
      <template v-if="phase === 'setup'">
        <h2>闪卡模式</h2>
        <p class="info">当前共有 <strong>{{ wordCount }}</strong> 个单词</p>
        <p v-if="wordCount === 0" class="warning">还没有录入单词</p>
        <template v-else>
          <div class="filter-section">
            <label class="checkbox-label">
              <input type="checkbox" v-model="difficultOnly" />
              只看困难词
            </label>
          </div>
          <p class="label">选择卡片数量：</p>
          <div class="options">
            <button
              v-for="n in [10, 20, 50]"
              :key="n"
              class="option-btn"
              :disabled="n > wordCount"
              @click="startFlashcards(n)"
            >{{ n }} 张</button>
          </div>
        </template>
      </template>

      <!-- Playing -->
      <template v-if="phase === 'playing'">
        <div class="flashcard-header">
          <p class="progress">{{ currentIndex + 1 }} / {{ cards.length }}</p>
          <button
            class="btn-star"
            :class="{ active: currentCard.is_difficult }"
            @click="handleToggleDifficult"
          >{{ currentCard.is_difficult ? '★' : '☆' }}</button>
        </div>

        <div class="flashcard" :class="{ flipped, 'no-transition': animating }" @click="flip">
          <div class="flashcard-inner">
            <div class="flashcard-front">
              <p class="flashcard-text">{{ currentCard.original }}</p>
              <p class="tap-hint">点击翻转</p>
            </div>
            <div class="flashcard-back">
              <p class="flashcard-text back-text">{{ currentCard.translation }}</p>
            </div>
          </div>
        </div>

        <div v-if="flipped" class="answer-buttons">
          <button class="btn-unknown" @click="next(false)">😕 不认识</button>
          <button class="btn-known" @click="next(true)">😊 认识</button>
        </div>
      </template>

      <!-- Done -->
      <template v-if="phase === 'done'">
        <div class="done-section">
          <p class="done-icon">🎴</p>
          <p class="done-text">闪卡练习完成！</p>
          <p class="done-score">
            认识 <span class="known">{{ knownCount }}</span> · 不认识 <span class="unknown">{{ unknownCount }}</span>
          </p>
          <div class="done-actions">
            <button class="btn-primary" @click="retry">再来一次</button>
            <RouterLink to="/spaced" class="btn-secondary">去今日复习</RouterLink>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
h2 {
  margin: 0 0 16px;
  font-size: 18px;
  color: #333;
  text-align: center;
}

.info {
  text-align: center;
  font-size: 16px;
  color: #555;
  margin-bottom: 8px;
}

.warning {
  text-align: center;
  color: #dc2626;
  font-size: 14px;
}

.filter-section {
  text-align: center;
  margin-bottom: 16px;
}

.checkbox-label {
  font-size: 14px;
  color: #555;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.checkbox-label input {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.label {
  text-align: center;
  color: #666;
  margin-bottom: 12px;
}

.options {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.option-btn {
  padding: 12px 28px;
  font-size: 16px;
  border: 2px solid #4f46e5;
  background: #fff;
  color: #4f46e5;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.option-btn:hover:not(:disabled) {
  background: #4f46e5;
  color: #fff;
}

.option-btn:disabled {
  border-color: #ddd;
  color: #ccc;
  cursor: not-allowed;
}

/* Flashcard */
.flashcard-header {
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
}

.btn-star.active { color: #f59e0b; }
.btn-star:hover { color: #f59e0b; }

.flashcard {
  perspective: 1000px;
  cursor: pointer;
  margin-bottom: 20px;
}

.flashcard-inner {
  position: relative;
  width: 100%;
  min-height: 200px;
  transition: transform 0.5s;
  transform-style: preserve-3d;
}

.flashcard.no-transition .flashcard-inner {
  transition: none;
}

.flashcard.flipped .flashcard-inner {
  transform: rotateY(180deg);
}

.flashcard-front,
.flashcard-back {
  position: absolute;
  width: 100%;
  min-height: 200px;
  backface-visibility: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  padding: 32px;
  box-sizing: border-box;
}

.flashcard-front {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.flashcard-back {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  transform: rotateY(180deg);
}

.flashcard-text {
  font-size: 22px;
  font-weight: 600;
  color: #fff;
  margin: 0;
  text-align: center;
  line-height: 1.5;
  word-break: break-word;
}

.tap-hint {
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
  margin: 12px 0 0;
}

.answer-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-unknown,
.btn-known {
  padding: 12px 32px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-unknown {
  background: #fef2f2;
  color: #dc2626;
}

.btn-unknown:hover { background: #fee2e2; }

.btn-known {
  background: #f0fdf4;
  color: #16a34a;
}

.btn-known:hover { background: #dcfce7; }

/* Done */
.done-section {
  text-align: center;
  padding: 20px 0;
}

.done-icon { font-size: 48px; margin: 0 0 8px; }
.done-text { font-size: 20px; font-weight: 600; color: #333; margin: 0 0 8px; }
.done-score { font-size: 16px; color: #555; margin: 0 0 20px; }
.done-score .known { color: #16a34a; font-weight: 600; }
.done-score .unknown { color: #dc2626; font-weight: 600; }

.done-actions {
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
}

.btn-primary:hover { background: #4338ca; }

.btn-secondary {
  padding: 10px 24px;
  border: 2px solid #e5e5e5;
  border-radius: 8px;
  font-size: 15px;
  color: #555;
  text-decoration: none;
}

.btn-secondary:hover {
  border-color: #4f46e5;
  color: #4f46e5;
}
</style>
