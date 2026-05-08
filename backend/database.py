from psycopg_pool import ConnectionPool

pool = ConnectionPool(
    conninfo="dbname=remember_word",
    min_size=2,
    max_size=10,
)

def init_db():
    with pool.connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS words (
                id              SERIAL PRIMARY KEY,
                original        TEXT NOT NULL,
                translation     TEXT NOT NULL,
                created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_difficult    BOOLEAN DEFAULT FALSE,
                review_count    INTEGER DEFAULT 0,
                ease_factor     REAL DEFAULT 2.5,
                interval_days   INTEGER DEFAULT 0,
                next_review_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Add columns if they don't exist (for existing databases)
        for col, definition in [
            ("is_difficult", "BOOLEAN DEFAULT FALSE"),
            ("review_count", "INTEGER DEFAULT 0"),
            ("ease_factor", "REAL DEFAULT 2.5"),
            ("interval_days", "INTEGER DEFAULT 0"),
            ("next_review_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ]:
            conn.execute(f"""
                DO $$
                BEGIN
                    ALTER TABLE words ADD COLUMN IF NOT EXISTS {col} {definition};
                END $$;
            """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS review_logs (
                id                  SERIAL PRIMARY KEY,
                word_id             INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
                reviewed_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                correct             BOOLEAN NOT NULL,
                review_count_before INTEGER NOT NULL,
                interval_days_before INTEGER NOT NULL,
                ease_factor_before  REAL NOT NULL,
                scheduled_at        TIMESTAMP,
                overdue_days        REAL
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_review_logs_word_id ON review_logs(word_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_review_logs_reviewed_at ON review_logs(reviewed_at)")
        conn.commit()
