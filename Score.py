Instance = None
class Score:
    def __init__(self):
        self.current_score = 0
        self.count = 0

    def Update(self):
        self.count += 1
        if self.count == 20:
            self.current_score += 1
            self.count = 0
