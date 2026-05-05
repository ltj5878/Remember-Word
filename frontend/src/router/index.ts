import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ReviewView from '../views/ReviewView.vue'
import QuizView from '../views/QuizView.vue'
import SpacedReviewView from '../views/SpacedReviewView.vue'
import FlashcardView from '../views/FlashcardView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/review', component: ReviewView },
    { path: '/quiz', component: QuizView },
    { path: '/spaced', component: SpacedReviewView },
    { path: '/flashcard', component: FlashcardView },
  ],
})

export default router
