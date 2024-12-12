import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('scores.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY,
                name TEXT,
                score INTEGER
            )''')
        self.conn.commit()

    def insert_score(self, name, score):
        self.cursor.execute('INSERT INTO scores (name, score) VALUES (?, ?)', (name, score))
        self.conn.commit()

    def get_top_scores(self):
        # Получаем уникальные имена и максимальные баллы
        self.cursor.execute('''
            SELECT name, MAX(score) FROM scores GROUP BY name ORDER BY MAX(score) DESC LIMIT 5''')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()