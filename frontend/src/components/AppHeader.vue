<script setup lang="ts">
</script>

<template>
  <header class="app-header">
    <h1 class="app-title">📖 记单词</h1>
    <nav class="app-nav">
      <RouterLink to="/" class="nav-link">录入</RouterLink>
      <RouterLink to="/review" class="nav-link">复习</RouterLink>
      <RouterLink to="/spaced" class="nav-link">今日复习</RouterLink>
      <RouterLink to="/quiz" class="nav-link">测验</RouterLink>
      <RouterLink to="/flashcard" class="nav-link">闪卡</RouterLink>
    </nav>
  </header>
</template>

<style scoped>
.app-header {
  background: #fff;
  padding: 16px 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  gap: 32px;
}

.app-title {
  font-size: 20px;
  margin: 0;
  color: #333;
}

.app-nav {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.nav-link {
  padding: 6px 14px;
  border-radius: 6px;
  text-decoration: none;
  color: #555;
  font-size: 15px;
  transition: all 0.2s;
}

.nav-link:hover {
  background: #f0f0f0;
}

.nav-link.router-link-exact-active {
  background: #4f46e5;
  color: #fff;
}
</style>
