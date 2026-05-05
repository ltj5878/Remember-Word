<script setup lang="ts">
import { ref } from 'vue'
import type { Word } from '../composables/useApi'

defineProps<{
  words: Word[]
}>()

const emit = defineEmits<{
  delete: [id: number]
  update: [id: number, original: string, translation: string]
  toggleDifficult: [id: number, difficult: boolean]
}>()

const editingId = ref<number | null>(null)
const editOriginal = ref('')
const editTranslation = ref('')

function startEdit(word: Word) {
  editingId.value = word.id
  editOriginal.value = word.original
  editTranslation.value = word.translation
}

function cancelEdit() {
  editingId.value = null
}

function confirmEdit(id: number) {
  if (!editOriginal.value.trim() || !editTranslation.value.trim()) return
  emit('update', id, editOriginal.value.trim(), editTranslation.value.trim())
  editingId.value = null
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}
</script>

<template>
  <div class="table-wrapper">
    <table v-if="words.length > 0">
      <thead>
        <tr>
          <th>原文</th>
          <th>翻译</th>
          <th>录入时间</th>
          <th>状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="word in words" :key="word.id">
          <template v-if="editingId === word.id">
            <td class="col-original">
              <textarea v-model="editOriginal" class="edit-input" rows="2" />
            </td>
            <td class="col-translation">
              <textarea v-model="editTranslation" class="edit-input" rows="2" />
            </td>
            <td class="col-date">{{ formatDate(word.created_at) }}</td>
            <td></td>
            <td class="col-action">
              <button class="btn-confirm" @click="confirmEdit(word.id)">确认</button>
              <button class="btn-cancel" @click="cancelEdit">取消</button>
            </td>
          </template>
          <template v-else>
            <td class="col-original">{{ word.original }}</td>
            <td class="col-translation">{{ word.translation }}</td>
            <td class="col-date">{{ formatDate(word.created_at) }}</td>
            <td class="col-status">
              <span v-if="word.is_difficult" class="badge-difficult">困难</span>
              <span v-if="word.review_count > 0" class="badge-review">已复习{{ word.review_count }}次</span>
            </td>
            <td class="col-action">
              <button
                class="btn-star"
                :class="{ active: word.is_difficult }"
                @click="emit('toggleDifficult', word.id, !word.is_difficult)"
                :title="word.is_difficult ? '取消困难标记' : '标记为困难'"
              >{{ word.is_difficult ? '★' : '☆' }}</button>
              <button class="btn-edit" @click="startEdit(word)">修改</button>
              <button class="btn-delete" @click="emit('delete', word.id)">删除</button>
            </td>
          </template>
        </tr>
      </tbody>
    </table>
    <p v-else class="empty">还没有录入任何单词</p>
  </div>
</template>

<style scoped>
.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  font-size: 13px;
  color: #888;
  font-weight: 600;
}

td {
  font-size: 15px;
  color: #333;
  vertical-align: top;
}

.col-original { max-width: 220px; word-break: break-word; }
.col-translation { max-width: 220px; word-break: break-word; }
.col-date { white-space: nowrap; color: #888; font-size: 13px; }
.col-status { white-space: nowrap; }
.col-action { white-space: nowrap; }

.badge-difficult {
  display: inline-block;
  padding: 2px 6px;
  background: #fef2f2;
  color: #dc2626;
  border-radius: 4px;
  font-size: 12px;
  margin-right: 4px;
}

.badge-review {
  display: inline-block;
  padding: 2px 6px;
  background: #f0fdf4;
  color: #16a34a;
  border-radius: 4px;
  font-size: 12px;
}

.edit-input {
  width: 100%;
  padding: 6px 8px;
  border: 1px solid #4f46e5;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
}

.edit-input:focus {
  outline: none;
}

.btn-star {
  padding: 4px 8px;
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #ccc;
  transition: color 0.2s;
}

.btn-star.active {
  color: #f59e0b;
}

.btn-star:hover {
  color: #f59e0b;
}

.btn-edit,
.btn-delete,
.btn-confirm,
.btn-cancel {
  padding: 4px 10px;
  background: none;
  border: 1px solid #e5e5e5;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  margin-right: 4px;
}

.btn-edit { color: #555; }
.btn-edit:hover { border-color: #4f46e5; color: #4f46e5; }

.btn-delete { color: #999; }
.btn-delete:hover { border-color: #dc2626; color: #dc2626; }

.btn-confirm { color: #16a34a; }
.btn-confirm:hover { border-color: #16a34a; background: #f0fdf4; }

.btn-cancel { color: #999; }
.btn-cancel:hover { border-color: #888; color: #555; }

.empty {
  text-align: center;
  color: #999;
  padding: 40px;
}
</style>
