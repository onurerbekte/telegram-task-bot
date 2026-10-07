from contextlib import contextmanager
from pathlib import Path
import sqlite3


class TaskStore:
    def __init__(self,path):
        self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.db() as db:
            db.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,title TEXT NOT NULL,done INTEGER NOT NULL DEFAULT 0)")
            db.execute("CREATE TABLE IF NOT EXISTS preferences(user_id INTEGER PRIMARY KEY,language TEXT NOT NULL)")

    @contextmanager
    def db(self):
        db=sqlite3.connect(self.path,timeout=10);db.row_factory=sqlite3.Row
        try:
            with db:yield db
        finally:db.close()

    def language(self,user):
        with self.db() as db:
            row=db.execute("SELECT language FROM preferences WHERE user_id=?",(user,)).fetchone()
            return row["language"] if row else "tr"

    def set_language(self,user,language):
        if language not in ("tr","en"):raise ValueError("Invalid language")
        with self.db() as db:
            db.execute("INSERT INTO preferences(user_id,language) VALUES(?,?) ON CONFLICT(user_id) DO UPDATE SET language=excluded.language",(user,language))

    def add(self,user,title):
        title=title.strip()
        if not title or len(title)>200:raise ValueError("Invalid task")
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            count=db.execute("SELECT COUNT(*) FROM tasks WHERE user_id=?",(user,)).fetchone()[0]
            if count>=100:raise ValueError("Task limit")
            return db.execute("INSERT INTO tasks(user_id,title) VALUES(?,?)",(user,title)).lastrowid

    def list(self,user):
        with self.db() as db:
            return [dict(row) for row in db.execute("SELECT id,title,done FROM tasks WHERE user_id=? ORDER BY id DESC LIMIT 10",(user,))]

    def change(self,user,task_id,delete=False):
        with self.db() as db:
            sql="DELETE FROM tasks WHERE user_id=? AND id=?" if delete else "UPDATE tasks SET done=1 WHERE user_id=? AND id=? AND done=0"
            return bool(db.execute(sql,(user,task_id)).rowcount)
