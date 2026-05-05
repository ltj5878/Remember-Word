<script setup lang="ts">
defineProps<{
  currentPage: number
  totalPages: number
  pageSize: number
  pageSizeOptions: number[]
}>()

const emit = defineEmits<{
  changePage: [page: number]
  changePageSize: [size: number]
}>()
</script>

<template>
  <div class="pagination">
    <div class="page-size">
      <span>每页</span>
      <select :value="pageSize" @change="emit('changePageSize', Number(($event.target as HTMLSelectElement).value))">
        <option v-for="n in pageSizeOptions" :key="n" :value="n">{{ n }}</option>
      </select>
      <span>条</span>
    </div>

    <div class="page-nav">
      <button :disabled="currentPage === 1" @click="emit('changePage', currentPage - 1)">‹</button>
      <template v-for="p in totalPages" :key="p">
        <button
          v-if="totalPages <= 7 || p === 1 || p === totalPages || Math.abs(p - currentPage) <= 1"
          :class="{ active: p === currentPage }"
          @click="emit('changePage', p)"
        >{{ p }}</button>
        <span
          v-else-if="(p === currentPage - 2 && p > 2) || (p === currentPage + 2 && p < totalPages - 1)"
          class="ellipsis"
        >…</span>
      </template>
      <button :disabled="currentPage === totalPages" @click="emit('changePage', currentPage + 1)">›</button>
    </div>
  </div>
</template>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #eee;
  flex-wrap: wrap;
  gap: 8px;
}

.page-size {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #666;
}

.page-size select {
  padding: 3px 6px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
}

.page-nav {
  display: flex;
  align-items: center;
  gap: 4px;
}

.page-nav button {
  min-width: 30px;
  height: 30px;
  padding: 0 6px;
  border: 1px solid #e5e5e5;
  background: #fff;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  color: #444;
  transition: all 0.2s;
}

.page-nav button:hover:not(:disabled) {
  border-color: #4f46e5;
  color: #4f46e5;
}

.page-nav button.active {
  background: #4f46e5;
  border-color: #4f46e5;
  color: #fff;
}

.page-nav button:disabled {
  color: #ccc;
  cursor: not-allowed;
}

.ellipsis {
  font-size: 13px;
  color: #aaa;
  padding: 0 2px;
}
</style>
