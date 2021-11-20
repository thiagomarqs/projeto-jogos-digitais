class Scoreboard(object):
    def __init__(self, initial_score):
        self.current_score = initial_score
        self.highscores = {
            "first":0,
            "second":0,
            "third":0
            }

    def is_highscore(self):
        print("\n\nis_highscore()")
        print("highscores: ")
        print(self.highscores)
        if self.current_score > self.highscores['first']:
            print("current: " + str(self.current_score))
            return True
        return False

    def set_new_highscore(self):
        score = self.current_score
        print("\n\nset_new_highscore()")
        print("current: " + str(score))
        if score > self.highscores['first']:
            self.highscores['third'] = self.highscores['second']
            self.highscores['second'] = self.highscores['first']
            self.highscores['first'] = score
        elif score > self.highscores['second']:
            self.highscores['third'] = self.highscores['second']
            self.highscores['second'] = score
        elif score > self.highscores['third']:
            self.highscores['third'] = score
        print("highscores: ")
        print(self.highscores)