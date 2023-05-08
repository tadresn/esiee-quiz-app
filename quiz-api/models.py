class Question:
    def __init__(self, id: int, position: int, title: str, text: str, image: str, possible_answers):
        self.id = id
        self.position = position
        self.title = title
        self.text = text
        self.image = image
        self.possible_answers = possible_answers

    def question_to_dict(self):
        return {
            "id": self.id,
            "position": self.position,
            "title": self.title,
            "text": self.text,
            "image": self.image,
            "possibleAnswers": self.possible_answers
        }
    
class PossibleAnswer:
    def __init__(self, id: int, text: str, isCorrect: int):
        self.id = id
        self.text = text
        self.isCorrect = isCorrect

    def possibleAnswer_to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "isCorrect": self.isCorrect
        }

class Participation:
    def __init__(self, id: int, player_name: str, score: int, date):
        self.id = id
        self.player_name = player_name
        self.score = score
        self.date = date

    def participation_to_dict(self):
        return {
            "id": self.id,
            "playerName": self.player_name,
            "score": self.score,
            "date": self.date
        }

