import sqlite3
import os

class Question():
    def init(self, position: int, title: str, text: str, image: str):
        self.position = position
        self.title = title
        self.text = text
        self.image = image
        return self

    def question_to_dict(question):
        """
        Fonction qui convertit un objet Question en un dictionnaire
        """
        return {
            "position": question.position,
            "title": question.title,
            "text": question.text,
            "image": question.image
        }

    def dict_to_question(self, question_dict):
        """
        Fonction qui convertit un dictionnaire en un objet Question
        """
        return Question().init(
            position=question_dict['position'],
            title=question_dict['title'],
            text=question_dict['text'],
            image=question_dict['image']
        )

class DataBase:
    def __init__(self):
        self.path = "quiz_db.db"
        self.connection = sqlite3.connect(self.path)
        self.connection.isolation_level = None

    def __del__(self):
        self.connection.close()

    def execute(self, query, value):
        try:
            cur = self.connection.cursor()
            cur.execute("begin")
            cur.execute(query, value)
            cur.execute("commit")
            cur.close()
        except:
            cur.execute('rollback')
            cur.close()
            raise
        return cur
    
    def rebuild_db(self):
        try:
            self.connection.close()
            os.remove(self.path)
            self.connection = sqlite3.connect(self.path)
            self.connection.isolation_level = None
            self.execute("""
            CREATE TABLE question (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            position INTEGER,
            title TEXT,
            text TEXT NOT NULL,
            image TEXT
            )
            """, ())
        except Exception as e:
            print(f"Failed to remove database file: {e}")
            raise Exception("Could not remove database file")
    
    def insert_db(self, question):
        query = "INSERT INTO question (position, title, text, image) VALUES (?, ?, ?, ?)"
        value = (question.position, question.title, question.text, question.image)
        cur = self.execute(query, value)
        question_id = cur.lastrowid
        return question_id
