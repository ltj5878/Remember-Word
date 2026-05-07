<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useApi, type Word } from '../composables/useApi'
import WordTable from '../components/WordTable.vue'
import Pagination from '../components/Pagination.vue'

const { getWords, updateWord, deleteWord, toggleDifficult } = useApi()
const words = ref<Word[]>([])
const loading = ref(true)
const searchQuery = ref('')

const PAGE_SIZE_OPTIONS = [10, 20, 50]
const pageSize = ref(10)
const currentPage = ref(1)

const filteredWords = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return words.value
  return words.value.filter(w =>
    w.original.toLowerCase().includes(q) || w.translation.toLowerCase().includes(q)
  )
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredWords.value.length / pageSize.value)))

const pagedWords = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredWords.value.slice(start, start + pageSize.value)
})

function handlePageSizeChange(size: number) {
  pageSize.value = size
  currentPage.value = 1
}

function handlePageChange(page: number) {
  currentPage.value = page
}

async function loadWords() {
  loading.value = true
  try {
    words.value = await getWords()
  } finally {
    loading.value = false
  }
}

async function handleUpdate(id: number, original: string, translation: string) {
  const updated = await updateWord(id, original, translation)
  const idx = words.value.findIndex(w => w.id === id)
  if (idx !== -1) words.value[idx] = updated
}

async function handleToggleDifficult(id: number, difficult: boolean) {
  const updated = await toggleDifficult(id, difficult)
  const idx = words.value.findIndex(w => w.id === id)
  if (idx !== -1) words.value[idx] = updated
}

async function handleDelete(id: number) {
  await deleteWord(id)
  words.value = words.value.filter(w => w.id !== id)
  if (currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value
  }
}

watch(searchQuery, () => { currentPage.value = 1 })

onMounted(loadWords)
</script>

<template>
  <div class="page">
    <div class="card">
      <h2>复习单词 <span class="count">（共 {{ words.length }} 个）</span></h2>
      <div class="search-bar" v-if="words.length > 0">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索单词或翻译..."
          class="search-input"
        />
        <span v-if="searchQuery.trim()" class="search-count">
          找到 {{ filteredWords.length }} 个结果
        </span>
      </div>
      <p v-if="loading" class="loading">加载中...</p>
      <template v-else>
        <WordTable
          :words="pagedWords"
          @update="handleUpdate"
          @delete="handleDelete"
          @toggle-difficult="handleToggleDifficult"
        />
        <Pagination
          v-if="words.length > 0"
          :current-page="currentPage"
          :total-pages="totalPages"
          :page-size="pageSize"
          :page-size-options="PAGE_SIZE_OPTIONS"
          @change-page="handlePageChange"
          @change-page-size="handlePageSizeChange"
        />
      </template>
    </div>
  </div>
</template>

<style scoped>
h2 {
  margin: 0 0 20px;
  font-size: 18px;
  color: #333;
}

.count {
  font-weight: 400;
  color: #888;
  font-size: 14px;
}

.loading {
  text-align: center;
  color: #888;
  padding: 40px;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.search-input {
  flex: 1;
  max-width: 320px;
  padding: 8px 12px;
  border: 1px solid #e5e5e5;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  transition: border-color 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #4f46e5;
}

.search-count {
  font-size: 13px;
  color: #888;
}
</style>
