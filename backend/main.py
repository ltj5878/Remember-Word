from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from database import pool, init_db
from models import WordCreate, WordResponse, QuizQuestion, ReviewResult
from quiz import generate_quiz
from spaced_repetition import calculate_next_review

app = FastAPI(title="记单词 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WORD_COLUMNS = "id, original, translation, created_at, is_difficult, review_count, ease_factor, interval_days, next_review_at"


def row_to_word(r) -> WordResponse:
    return WordResponse(
        id=r[0], original=r[1], translation=r[2], created_at=r[3],
        is_difficult=r[4], review_count=r[5], ease_factor=r[6],
        interval_days=r[7], next_review_at=r[8],
    )


@app.on_event("startup")
def startup():
    init_db()


# ============ CRUD ============

@app.post("/api/words", response_model=WordResponse)
def create_word(word: WordCreate):
    with pool.connection() as conn:
        row = conn.execute(
            f"INSERT INTO words (original, translation) VALUES (%s, %s) RETURNING {WORD_COLUMNS}",
            (word.original, word.translation),
        ).fetchone()
        conn.commit()
    return row_to_word(row)


@app.get("/api/words", response_model=list[WordResponse])
def get_words():
    with pool.connection() as conn:
        rows = conn.execute(
            f"SELECT {WORD_COLUMNS} FROM words ORDER BY created_at DESC"
        ).fetchall()
    return [row_to_word(r) for r in rows]


@app.get("/api/words/count")
def get_word_count():
    with pool.connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM words").fetchone()[0]
    return {"count": count}


@app.put("/api/words/{word_id}", response_model=WordResponse)
def update_word(word_id: int, word: WordCreate):
    with pool.connection() as conn:
        row = conn.execute(
            f"UPDATE words SET original = %s, translation = %s WHERE id = %s RETURNING {WORD_COLUMNS}",
            (word.original, word.translation, word_id),
        ).fetchone()
        conn.commit()
        if row is None:
            raise HTTPException(status_code=404, detail="Word not found")
    return row_to_word(row)


@app.delete("/api/words/{word_id}")
def delete_word(word_id: int):
    with pool.connection() as conn:
        result = conn.execute("DELETE FROM words WHERE id = %s", (word_id,))
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Word not found")
    return {"message": "deleted"}


# ============ Difficult Words ============

@app.put("/api/words/{word_id}/difficult")
def toggle_difficult(word_id: int, difficult: bool = Query(...)):
    with pool.connection() as conn:
        row = conn.execute(
            f"UPDATE words SET is_difficult = %s WHERE id = %s RETURNING {WORD_COLUMNS}",
            (difficult, word_id),
        ).fetchone()
        conn.commit()
        if row is None:
            raise HTTPException(status_code=404, detail="Word not found")
    return row_to_word(row)


@app.get("/api/words/difficult", response_model=list[WordResponse])
def get_difficult_words():
    with pool.connection() as conn:
        rows = conn.execute(
            f"SELECT {WORD_COLUMNS} FROM words WHERE is_difficult = TRUE ORDER BY created_at DESC"
        ).fetchall()
    return [row_to_word(r) for r in rows]


# ============ Quiz ============

@app.get("/api/quiz", response_model=list[QuizQuestion])
def get_quiz(
    num: int = Query(default=10, ge=1),
    mode: str = Query(default="normal"),
    difficult_only: bool = Query(default=False),
):
    with pool.connection() as conn:
        if difficult_only:
            rows = conn.execute("SELECT id, original, translation FROM words WHERE is_difficult = TRUE").fetchall()
        else:
            rows = conn.execute("SELECT id, original, translation FROM words").fetchall()
    all_words = [{"id": r[0], "original": r[1], "translation": r[2]} for r in rows]
    if len(all_words) < 4:
        raise HTTPException(status_code=400, detail="至少需要录入4个单词才能开始测验")
    return generate_quiz(all_words, num, mode)


# ============ Spaced Repetition ============

@app.get("/api/review/today", response_model=list[WordResponse])
def get_today_review():
    """Get words due for review today."""
    with pool.connection() as conn:
        rows = conn.execute(
            f"SELECT {WORD_COLUMNS} FROM words WHERE next_review_at <= NOW() ORDER BY next_review_at ASC"
        ).fetchall()
    return [row_to_word(r) for r in rows]


@app.get("/api/review/today/count")
def get_today_review_count():
    with pool.connection() as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM words WHERE next_review_at <= NOW()"
        ).fetchone()[0]
    return {"count": count}


@app.post("/api/review/result")
def submit_review_result(result: ReviewResult):
    """Submit a review result and update spaced repetition schedule."""
    with pool.connection() as conn:
        row = conn.execute(
            "SELECT review_count, ease_factor, interval_days FROM words WHERE id = %s",
            (result.word_id,),
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Word not found")

        review_count, ease_factor, interval_days = row
        new_count, new_ease, new_interval, next_review = calculate_next_review(
            result.correct, review_count, ease_factor, interval_days
        )

        conn.execute(
            "UPDATE words SET review_count = %s, ease_factor = %s, interval_days = %s, next_review_at = %s WHERE id = %s",
            (new_count, new_ease, new_interval, next_review, result.word_id),
        )
        conn.commit()

    return {
        "word_id": result.word_id,
        "correct": result.correct,
        "new_interval_days": new_interval,
        "next_review_at": next_review.isoformat(),
    }


# ============ Flashcard ============

@app.get("/api/flashcards", response_model=list[WordResponse])
def get_flashcards(
    num: int = Query(default=20, ge=1),
    difficult_only: bool = Query(default=False),
):
    """Get random words for flashcard mode."""
    with pool.connection() as conn:
        if difficult_only:
            rows = conn.execute(
                f"SELECT {WORD_COLUMNS} FROM words WHERE is_difficult = TRUE ORDER BY RANDOM() LIMIT %s",
                (num,),
            ).fetchall()
        else:
            rows = conn.execute(
                f"SELECT {WORD_COLUMNS} FROM words ORDER BY RANDOM() LIMIT %s",
                (num,),
            ).fetchall()
    return [row_to_word(r) for r in rows]
