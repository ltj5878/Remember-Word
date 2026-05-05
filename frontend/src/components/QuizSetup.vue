<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  wordCount: number
  loading: boolean
}>()

const emit = defineEmits<{
  start: [num: number, mode: string, difficultOnly: boolean]
}>()

const mode = ref<'normal' | 'reverse'>('normal')
const difficultOnly = ref(false)
const numOptions = [5, 10, 20]
</script>

<template>
  <div class="quiz-setup">
    <p class="info">当前共有 <strong>{{ wordCount }}</strong> 个单词</p>
    <p v-if="wordCount < 4" class="warning">至少需要录入 4 个单词才能开始测验</p>
    <template v-else>
      <div class="mode-section">
        <p class="label">测验模式：</p>
        <div class="mode-options">
          <button
            :class="['mode-btn', { active: mode === 'normal' }]"
            @click="mode = 'normal'"
          >看原文选翻译</button>
          <button
            :class="['mode-btn', { active: mode === 'reverse' }]"
            @click="mode = 'reverse'"
          >看翻译选原文</button>
        </div>
      </div>

      <div class="filter-section">
        <label class="checkbox-label">
          <input type="checkbox" v-model="difficultOnly" />
          只测困难词
        </label>
      </div>

      <p class="label">选择题目数量：</p>
      <div class="options">
        <button
          v-for="n in numOptions"
          :key="n"
          class="option-btn"
          :disabled="n > wordCount || loading"
          @click="emit('start', n, mode, difficultOnly)"
        >
          {{ n }} 题
        </button>
      </div>
    </template>
  </div>
</template>

<style scoped>
.quiz-setup {
  text-align: center;
}

.info {
  font-size: 16px;
  color: #555;
  margin-bottom: 8px;
}

.warning {
  color: #dc2626;
  font-size: 14px;
}

.label {
  color: #666;
  margin-bottom: 12px;
}

.mode-section {
  margin-bottom: 16px;
}

.mode-options {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-bottom: 8px;
}

.mode-btn {
  padding: 8px 18px;
  font-size: 14px;
  border: 2px solid #e5e5e5;
  background: #fff;
  border-radius: 6px;
  cursor: pointer;
  color: #555;
  transition: all 0.2s;
}

.mode-btn.active {
  border-color: #4f46e5;
  background: #4f46e5;
  color: #fff;
}

.filter-section {
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
</style>
