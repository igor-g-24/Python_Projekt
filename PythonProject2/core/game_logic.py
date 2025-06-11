class HangmanGame:
    def __init__(self, word: str, max_lives: int = 10):
        self.word_to_guess = word.upper()
        self.max_lives = max_lives
        self.guessed_letters = set()
        self.hidden_word = ['_'] * len(self.word_to_guess)

        for i, char in enumerate(self.word_to_guess):
            if not char.isalpha():
                self.hidden_word[i] = char

    def guess(self, letter: str):
        letter = letter.upper()
        if letter in self.guessed_letters or not letter.isalpha():
            return "already_guessed"

        self.guessed_letters.add(letter)

        if letter in self.word_to_guess:
            for i, char in enumerate(self.word_to_guess):
                if char == letter:
                    self.hidden_word[i] = letter
            return "correct"
        else:
            return "incorrect"

    def get_display_word(self) -> str:
        return " ".join(self.hidden_word)

    def is_won(self) -> bool:
        return '_' not in self.hidden_word


class SinglePlayer:
    def __init__(self, word: str, user_id: int):
        self.game = HangmanGame(word)
        self.lives = self.game.max_lives
        self.user_id = user_id

    def make_guess(self, letter: str) -> str:
        result = self.game.guess(letter)
        if result == "incorrect":
            self.lives -= 1
        return result

    def is_game_over(self) -> bool:
        return self.game.is_won() or self.lives <= 0


class TwoPlayer:
    def __init__(self, word: str, user1_id: int, user2_id: int):
        self.game = HangmanGame(word)
        self.players = {
            1: {'id': user1_id, 'lives': self.game.max_lives // 2},
            2: {'id': user2_id, 'lives': self.game.max_lives // 2}
        }
        self.current_player = 1
        self.winner = None

    def make_guess(self, letter: str) -> str:
        result = self.game.guess(letter)
        if result == "incorrect":
            self.players[self.current_player]['lives'] -= 1
            self.switch_player()
        return result

    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def is_game_over(self) -> bool:
        if self.game.is_won():
            self.winner = self.players[self.current_player]['id']
            return True
        if self.players[1]['lives'] <= 0 and self.players[2]['lives'] <= 0:
            self.winner = None
            return True

        if self.players[self.current_player]['lives'] <= 0:
            self.switch_player()

        return False