<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApi, type Word } from '../composables/useApi'
import WordForm from '../components/WordForm.vue'

const { getWords, updateWord } = useApi()

const searchQuery = ref('')
const allWords = ref<Word[]>([])

const editingId = ref<number | null>(null)
const editOriginal = ref('')
const editTranslation = ref('')

const filteredWords = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return []
  return allWords.value.filter(w =>
    w.original.toLowerCase().includes(q) || w.translation.toLowerCase().includes(q)
  )
})

async function loadWords() {
  allWords.value = await getWords()
}

function onWordAdded() {
  loadWords()
}

function startEdit(word: Word) {
  editingId.value = word.id
  editOriginal.value = word.original
  editTranslation.value = word.translation
}

function cancelEdit() {
  editingId.value = null
}

async function confirmEdit(id: number) {
  if (!editOriginal.value.trim() || !editTranslation.value.trim()) return
  const updated = await updateWord(id, editOriginal.value.trim(), editTranslation.value.trim())
  const idx = allWords.value.findIndex(w => w.id === id)
  if (idx !== -1) allWords.value[idx] = updated
  editingId.value = null
}

onMounted(loadWords)
</script>

<template>
  <div class="page-wide">
    <div class="two-col">
      <div class="card">
        <h2>录入新单词</h2>
        <WordForm @added="onWordAdded" />
      </div>

      <div class="card">
        <h2>搜索</h2>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="输入单词或翻译，实时搜索..."
          class="search-input"
        />
        <template v-if="searchQuery.trim()">
          <p v-if="filteredWords.length === 0" class="no-result">未找到相关记录，可以放心录入 ✅</p>
          <template v-else>
            <p class="found-count">找到 {{ filteredWords.length }} 条相关记录：</p>
            <div class="result-list">
              <div v-for="w in filteredWords" :key="w.id" class="result-item">
                <template v-if="editingId === w.id">
                  <div class="edit-fields">
                    <textarea v-model="editOriginal" class="edit-input" rows="2" />
                    <textarea v-model="editTranslation" class="edit-input" rows="2" />
                  </div>
                  <div class="edit-actions">
                    <button class="btn-confirm" @click="confirmEdit(w.id)">确认</button>
                    <button class="btn-cancel" @click="cancelEdit">取消</button>
                  </div>
                </template>
                <template v-else>
                  <span class="result-original">{{ w.original }}</span>
                  <span class="result-sep">→</span>
                  <span class="result-translation">{{ w.translation }}</span>
                  <button class="btn-edit" @click="startEdit(w)">修改</button>
                </template>
              </div>
            </div>
          </template>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
h2 {
  margin: 0 0 20px;
  font-size: 18px;
  color: #333;
}

.page-wide {
  max-width: 960px;
  margin: 0 auto;
  padding: 32px 16px;
}

.two-col {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.two-col > .card {
  flex: 1;
  min-width: 0;
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

@media (max-width: 720px) {
  .two-col {
    flex-direction: column;
  }
}

.search-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 15px;
  font-family: inherit;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.search-input:focus {
  outline: none;
  border-color: #4f46e5;
}

.no-result {
  text-align: center;
  color: #16a34a;
  font-size: 15px;
  margin: 12px 0 0;
  padding: 12px 0;
}

.found-count {
  font-size: 14px;
  color: #f59e0b;
  margin: 12px 0 8px;
}

.result-list {
  max-height: 300px;
  overflow-y: auto;
}

.result-item {
  display: flex;
  align-items: baseline;
  gap: 8px;
  padding: 8px 12px;
  background: #f9fafb;
  border-radius: 6px;
  margin-bottom: 4px;
  font-size: 14px;
  flex-wrap: wrap;
}

.result-original {
  color: #333;
  font-weight: 500;
}

.result-sep {
  color: #ccc;
}

.result-translation {
  color: #666;
  flex: 1;
}

.btn-edit {
  padding: 2px 10px;
  background: none;
  border: 1px solid #e5e5e5;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  color: #555;
  transition: all 0.2s;
  flex-shrink: 0;
}

.btn-edit:hover {
  border-color: #4f46e5;
  color: #4f46e5;
}

.edit-fields {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
  min-width: 0;
}

.edit-input {
  width: 100%;
  padding: 6px 8px;
  border: 1px solid #4f46e5;
  border-radius: 6px;
  font-size: 13px;
  font-family: inherit;
  resize: vertical;
  box-sizing: border-box;
}

.edit-input:focus {
  outline: none;
}

.edit-actions {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
  align-self: flex-start;
}

.btn-confirm,
.btn-cancel {
  padding: 4px 10px;
  background: none;
  border: 1px solid #e5e5e5;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-confirm { color: #16a34a; }
.btn-confirm:hover { border-color: #16a34a; background: #f0fdf4; }

.btn-cancel { color: #999; }
.btn-cancel:hover { border-color: #888; color: #555; }
</style>
