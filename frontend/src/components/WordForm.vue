<script setup lang="ts">
import { ref } from 'vue'
import { useApi } from '../composables/useApi'

const emit = defineEmits<{
  added: []
}>()

const original = ref('')
const translation = ref('')
const message = ref('')
const loading = ref(false)
const { addWord } = useApi()

async function handleSubmit() {
  if (!original.value.trim() || !translation.value.trim()) {
    message.value = '请填写完整'
    return
  }
  loading.value = true
  message.value = ''
  try {
    await addWord(original.value.trim(), translation.value.trim())
    message.value = '录入成功！'
    emit('added')
    original.value = ''
    translation.value = ''
  } catch {
    message.value = '录入失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="word-form">
    <div class="form-group">
      <label>原文</label>
      <textarea
        v-model="original"
        placeholder="输入单词、短语或句子"
        rows="3"
      />
    </div>
    <div class="form-group">
      <label>翻译</label>
      <textarea
        v-model="translation"
        placeholder="输入翻译"
        rows="3"
      />
    </div>
    <button class="btn-primary" :disabled="loading" @click="handleSubmit">
      {{ loading ? '录入中...' : '录入' }}
    </button>
    <p v-if="message" :class="['message', message.includes('成功') ? 'success' : 'error']">
      {{ message }}
    </p>
  </div>
</template>

<style scoped>
.word-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: #444;
}

.form-group textarea {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 15px;
  resize: vertical;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-group textarea:focus {
  outline: none;
  border-color: #4f46e5;
}

.btn-primary {
  padding: 10px 0;
  background: #4f46e5;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #4338ca;
}

.btn-primary:disabled {
  background: #aaa;
  cursor: not-allowed;
}

.message {
  text-align: center;
  font-size: 14px;
  margin: 0;
}

.message.success { color: #16a34a; }
.message.error { color: #dc2626; }
</style>
