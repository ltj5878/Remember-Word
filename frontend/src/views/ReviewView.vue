<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApi, type Word } from '../composables/useApi'
import WordTable from '../components/WordTable.vue'
import Pagination from '../components/Pagination.vue'

const { getWords, updateWord, deleteWord, toggleDifficult } = useApi()
const words = ref<Word[]>([])
const loading = ref(true)

const PAGE_SIZE_OPTIONS = [10, 20, 50]
const pageSize = ref(10)
const currentPage = ref(1)

const totalPages = computed(() => Math.max(1, Math.ceil(words.value.length / pageSize.value)))

const pagedWords = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return words.value.slice(start, start + pageSize.value)
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

onMounted(loadWords)
</script>

<template>
  <div class="page">
    <div class="card">
      <h2>复习单词 <span class="count">（共 {{ words.length }} 个）</span></h2>
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
</style>
