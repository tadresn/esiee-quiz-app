import sqlite3
import os
import models
from datetime import datetime

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
        nbQuestion = self.count_questions()
        cur = self.connection.cursor()
        cur.execute("begin")
        # Check if the position is valid
        if question.position > nbQuestion + 1:
            raise ValueError("Invalid position for the question")

        # Shift the questions' positions if necessary
        if question.position <= nbQuestion:
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
            possible_answer = models.PossibleAnswer(None, possible_answer_dict['text'], possible_answer_dict['isCorrect'])
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
            result = models.Participation(None, playerName, score, date)
            results.append(result.participation_to_dict())
        return results
    
    def delete_all_questions(self):
        cur = self.connection.cursor()
        cur.execute("begin")
        cur.execute("DELETE FROM possible_answers")
        cur.execute("DELETE FROM questions")
        cur.execute("commit")

    def delete_all_participations(self):
        cur = self.connection.cursor()
        cur.execute("begin")
        cur.execute("DELETE FROM participations")
        cur.execute("commit")

    def get_question_and_possible_answers_by_id(self, id):
        cur = self.connection.cursor()
        cur.execute("begin")
        cur.execute("SELECT * FROM questions WHERE id = ?", (id,))
        question_row = cur.fetchone()
        if not question_row:
            return None
        question = models.Question(id=question_row[0], position=question_row[1], title=question_row[2], text=question_row[3], image=question_row[4], possible_answers = None)
        cur.execute("SELECT id, text, isCorrect FROM possible_answers WHERE question_id = ?", (id,))
        possible_answers_rows = cur.fetchall()
        possible_answers = []
        for possible_answer_row in possible_answers_rows:
            possible_answer = models.PossibleAnswer(id=possible_answer_row[0], text=possible_answer_row[1], isCorrect=bool(possible_answer_row[2]))
            possible_answers.append(possible_answer.possibleAnswer_to_dict())
        cur.execute("commit")
        question.possible_answers = possible_answers
        return question
    
    def get_question_and_possible_answers_by_position(self, position):
        cur = self.connection.cursor()
        cur.execute("begin")
        cur.execute("SELECT * FROM questions WHERE position = ?", (position,))
        question_row = cur.fetchone()
        if not question_row:
            return None
        question = models.Question(id=question_row[0], position=question_row[1], title=question_row[2], text=question_row[3], image=question_row[4], possible_answers = None)
        cur.execute("SELECT id, text, isCorrect FROM possible_answers WHERE question_id = ?", (question_row[0],))
        possible_answers_rows = cur.fetchall()
        possible_answers = []
        for possible_answer_row in possible_answers_rows:
            possible_answer = models.PossibleAnswer(id=possible_answer_row[0], text=possible_answer_row[1], isCorrect=bool(possible_answer_row[2]))
            possible_answers.append(possible_answer.possibleAnswer_to_dict())
        cur.execute("commit")
        question.possible_answers = possible_answers
        return question
    
    def put_question_and_possible_answers_by_id(self, question):
        nbQuestion = self.count_questions()
        cur = self.connection.cursor()
        cur.execute("begin")
        # Check if the position is valid
        if question.position > nbQuestion + 1:
            raise ValueError("Invalid position for the question")
        
        # Check if the new position is already taken
        cur.execute("SELECT COUNT(*) FROM questions WHERE position = ? AND id != ?", (question.position, question.id))
        count = cur.fetchone()[0]
        if count > 0:
            cur.execute("SELECT position FROM questions WHERE id = ?", (question.id,))
            position_row = cur.fetchone()
            old_position = position_row[0]
            if question.position > old_position:
                cur.execute("UPDATE questions SET position = position - 1 WHERE position <= ? AND position > ?", (question.position, old_position))
            if question.position < old_position:
                cur.execute("UPDATE questions SET position = position + 1 WHERE position >= ? AND position < ?", (question.position, old_position))

        # Update the question
        question_values = (question.position, question.title, question.text, question.image, question.id)
        cur.execute("UPDATE questions SET position = ?, title = ?, text = ?, image = ? WHERE id = ?", question_values)

        # Delete the old possible answers
        cur.execute("DELETE FROM possible_answers WHERE question_id = ?", (question.id,))

        # Insert the new possible answers
        for possible_answer_dict in question.possible_answers:
            possible_answer = models.PossibleAnswer(None, possible_answer_dict['text'], possible_answer_dict['isCorrect'])
            answer_values = (possible_answer.text, possible_answer.isCorrect, question.id)
            cur.execute("INSERT INTO possible_answers (text, isCorrect, question_id) VALUES (?, ?, ?)", answer_values)

        cur.execute("commit")

    def delete_question_by_id(self, id):
        cur = self.connection.cursor()
        cur.execute("begin")

        # Get the position of the question to delete
        cur.execute("SELECT position FROM questions WHERE id = ?", (id,))
        position = cur.fetchone()[0]

        # Delete the question
        cur.execute("DELETE FROM questions WHERE id = ?", (id,))
        cur.execute("DELETE FROM possible_answers WHERE question_id = ?", (id,))

        # Get the questions with positions greater than the deleted question
        cur.execute("SELECT id, position FROM questions WHERE position > ? ORDER BY position ASC", (position,))
        rows = cur.fetchall()

        # Update the positions of the selected questions
        for row in rows:
            question_id = row[0]
            old_position = row[1]
            new_position = old_position - 1
            cur.execute("UPDATE questions SET position = ? WHERE id = ?", (new_position, question_id))

        cur.execute("commit")

    def post_participation(self, player_name, answers):
        cur = self.connection.cursor()
        cur.execute("begin")
         # Retrieve the quiz questions
        cur.execute("SELECT * FROM questions ORDER BY position ASC")
        questions_rows = cur.fetchall()
        questions = [models.Question(row[0], row[1], row[2], row[3], row[4], None) for row in questions_rows]
        for question in questions:
            cur.execute("SELECT * FROM possible_answers WHERE question_id = ?", (question.id,))
            possible_answers_rows = cur.fetchall()
            possible_answers = []
            for possible_answer_row in possible_answers_rows:
                possible_answer = models.PossibleAnswer(id=possible_answer_row[0], text=possible_answer_row[1], isCorrect=bool(possible_answer_row[2]))
                possible_answers.append(possible_answer.possibleAnswer_to_dict())
            question.possible_answers = possible_answers
        
        for i in range(len(questions)):
            questions[i] = questions[i].question_to_dict()

        # Compute the score and the answers summaries
        score = 0
        answers_summaries = []
        for i in range(len(questions)):
            was_correct = False
            k=0
            while(not questions[i]["possibleAnswers"][k]["isCorrect"]):
                k=k+1
            correct_answer_position = k + 1
            if answers[i] == correct_answer_position:
                score += 1
                was_correct = True

            # Add the answer summary to the list
            answer_summary ={
                "correctAnswerPosition" : correct_answer_position,
                "was_correct" : was_correct
                }
            answers_summaries.append(answer_summary)

        # Insert the player in the participations table
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        cur.execute("INSERT INTO participations (player_name, score, date) VALUES (?, ?, ?)", (player_name, score, now))

        cur.execute("commit")
        return player_name, score, answers_summaries
        



    
    
