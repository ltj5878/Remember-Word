const BASE_URL = 'http://localhost:8000/api'

export interface Word {
  id: number
  original: string
  translation: string
  created_at: string
  is_difficult: boolean
  review_count: number
  ease_factor: number
  interval_days: number
  next_review_at: string | null
}

export interface QuizQuestion {
  id: number
  original: string
  options: string[]
  answer_index: number
  mode: string
}

export interface ReviewResultResponse {
  word_id: number
  correct: boolean
  new_interval_days: number
  next_review_at: string
}

export function useApi() {
  async function addWord(original: string, translation: string): Promise<Word> {
    const res = await fetch(`${BASE_URL}/words`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ original, translation }),
    })
    if (!res.ok) throw new Error('录入失败')
    return res.json()
  }

  async function getWords(): Promise<Word[]> {
    const res = await fetch(`${BASE_URL}/words`)
    if (!res.ok) throw new Error('获取失败')
    return res.json()
  }

  async function getWordCount(): Promise<number> {
    const res = await fetch(`${BASE_URL}/words/count`)
    if (!res.ok) throw new Error('获取失败')
    const data = await res.json()
    return data.count
  }

  async function updateWord(id: number, original: string, translation: string): Promise<Word> {
    const res = await fetch(`${BASE_URL}/words/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ original, translation }),
    })
    if (!res.ok) throw new Error('修改失败')
    return res.json()
  }

  async function deleteWord(id: number): Promise<void> {
    const res = await fetch(`${BASE_URL}/words/${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('删除失败')
  }

  async function toggleDifficult(id: number, difficult: boolean): Promise<Word> {
    const res = await fetch(`${BASE_URL}/words/${id}/difficult?difficult=${difficult}`, {
      method: 'PUT',
    })
    if (!res.ok) throw new Error('标记失败')
    return res.json()
  }

  async function getDifficultWords(): Promise<Word[]> {
    const res = await fetch(`${BASE_URL}/words/difficult`)
    if (!res.ok) throw new Error('获取失败')
    return res.json()
  }

  async function getQuiz(num: number, mode: string = 'normal', difficultOnly: boolean = false): Promise<QuizQuestion[]> {
    const res = await fetch(`${BASE_URL}/quiz?num=${num}&mode=${mode}&difficult_only=${difficultOnly}`)
    if (!res.ok) {
      const data = await res.json()
      throw new Error(data.detail || '获取测验失败')
    }
    return res.json()
  }

  async function getTodayReview(): Promise<Word[]> {
    const res = await fetch(`${BASE_URL}/review/today`)
    if (!res.ok) throw new Error('获取失败')
    return res.json()
  }

  async function getTodayReviewCount(): Promise<number> {
    const res = await fetch(`${BASE_URL}/review/today/count`)
    if (!res.ok) throw new Error('获取失败')
    const data = await res.json()
    return data.count
  }

  async function submitReviewResult(wordId: number, correct: boolean): Promise<ReviewResultResponse> {
    const res = await fetch(`${BASE_URL}/review/result`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ word_id: wordId, correct }),
    })
    if (!res.ok) throw new Error('提交失败')
    return res.json()
  }

  async function getFlashcards(num: number = 20, difficultOnly: boolean = false): Promise<Word[]> {
    const res = await fetch(`${BASE_URL}/flashcards?num=${num}&difficult_only=${difficultOnly}`)
    if (!res.ok) throw new Error('获取失败')
    return res.json()
  }

  return {
    addWord, getWords, getWordCount, updateWord, deleteWord,
    toggleDifficult, getDifficultWords,
    getQuiz,
    getTodayReview, getTodayReviewCount, submitReviewResult,
    getFlashcards,
  }
}
