import sqlite3
from typing import Any, Dict, List, Optional

DB_PATH = "app.db"

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS elements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            details TEXT
        )
        """)
        conn.commit()

def tout_lire() -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM elements ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]

def lire_un(element_id: int) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM elements WHERE id=?", (element_id,)).fetchone()
        return dict(row) if row else None

def creer(titre: str, details: str) -> None:
    with get_conn() as conn:
        conn.execute("INSERT INTO elements (titre, details) VALUES (?, ?)", (titre, details))
        conn.commit()

def modifier(element_id: int, titre: str, details: str) -> None:
    with get_conn() as conn:
        conn.execute("UPDATE elements SET titre=?, details=? WHERE id=?", (titre, details, element_id))
        conn.commit()

def supprimer(element_id: int) -> None:
    with get_conn() as conn:
        conn.execute("DELETE FROM elements WHERE id=?", (element_id,))
        conn.commit()
