class Question:
    def __init__(self, position: int, title: str, text: str, image: str, possible_answers):
        self.position = position
        self.title = title
        self.text = text
        self.image = image
        self.possible_answers = possible_answers

    def question_to_dict(self):
        return {
            "position": self.position,
            "title": self.title,
            "text": self.text,
            "image": self.image,
            "possibleAnswers": self.possible_answers
        }
    
class PossibleAnswer:
    def __init__(self, text: str, isCorrect: int):
        self.text = text
        self.isCorrect = isCorrect

    def possibleAnswer_to_dict(self):
        return {
            "text": self.text,
            "isCorrect": self.isCorrect
        }

class Participation:
    def __init__(self, player_name: str, score: int, date):
        self.player_name = player_name
        self.score = score
        self.date = date

    def participation_to_dict(self):
        return {
            "player_name": self.player_name,
            "score": self.score,
            "date": self.date
        }

