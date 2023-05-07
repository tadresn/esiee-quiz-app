import sqlite3
import os
import models

class DataBase:
    def __init__(self):
        self.path = "quiz_db.db"
        self.connection = sqlite3.connect(self.path)
        self.connection.isolation_level = None
        cur = self.connection.cursor()
        cur.execute("begin")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            position INTEGER NOT NULL,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            image TEXT NOT NULL
            );
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS possible_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            isCorrect INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            FOREIGN KEY (question_id) REFERENCES question (id)
            );
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS participations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            date DATE NOT NULL
            );
            """)
        cur.execute("commit")

    def __del__(self):
        self.connection.close()
    
    def rebuild_db(self):
        try:
            self.connection.close()
            os.remove(self.path)
            self.__init__()
        except Exception as e:
            print(f"Failed to remove database file: {e}")
            raise Exception("Could not remove database file")
    
    def insert_question(self, question):
        cur = self.connection.cursor()
        cur.execute("begin")
        # Check if the position is valid
        if question.position > 10:
            raise ValueError("Invalid position for the question")

        # Shift the questions' positions if necessary
        if question.position <= 10:
            # Get the questions with positions greater or equal to the new position
            cur.execute("SELECT id, position FROM questions WHERE position >= ? ORDER BY position DESC", (question.position,))
            rows = cur.fetchall()

            # Update the positions of the selected questions
            for row in rows:
                question_id = row[0]
                old_position = row[1]
                new_position = old_position + 1
                cur.execute("UPDATE questions SET position = ? WHERE id = ?", (new_position, question_id))

        # Insert the new question
        question_values = (question.position, question.title, question.text, question.image)
        cur.execute("INSERT INTO questions (position, title, text, image) VALUES (?, ?, ?, ?)", question_values)
        question_id = cur.lastrowid

        # Insert the possible answers
        for possible_answer_dict in question.possible_answers:
            possible_answer = models.PossibleAnswer(possible_answer_dict['text'], possible_answer_dict['isCorrect'])
            answer_values = (possible_answer.text, possible_answer.isCorrect, question_id)
            cur.execute("INSERT INTO possible_answers (text, isCorrect, question_id) VALUES (?, ?, ?)", answer_values)

        cur.execute("commit")
        return question_id

    
    def count_questions(self):
        cur = self.connection.cursor()
        cur.execute("begin")
        cur.execute("SELECT COUNT(*) FROM questions")
        count = cur.fetchone()[0]
        cur.execute("commit")
        return count
    
    def get_participation_results(self):
        cur = self.connection.cursor()
        cur.execute("begin")
        cur.execute("SELECT player_name, score, date FROM participations ORDER BY score DESC")
        rows = cur.fetchall()
        cur.execute("commit")
        results = []
        for row in rows:
            playerName = row[0]
            score = row[1]
            date = row[2]
            result = models.Participation(playerName, score, date)
            results.append(result)
        return results
    
