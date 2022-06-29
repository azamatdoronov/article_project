from random import shuffle

from .messages import LEN_ERROR_MESSAGE, INIQUE_ERROR_MESSAGE, WIN_MESSAGE, \
    RANGE_ERROR_MESSAGE, NOT_INT_ERROR_MESSAGE, RESULT_MESSAGE, MISSED_MESSAGE


def generate_numbers(n):
    data = list(range(1, 10))
    shuffle(data)
    return data[:n]


class Game:
    stat_list = []
    secret_numbers = generate_numbers(4)

    def __init__(self) -> None:
        self.numbers = None

    def validation(self, numbers_str):
        try:
            numbers = [int(s) for s in numbers_str]
            if len(numbers) != 4:
                return LEN_ERROR_MESSAGE
            if len(numbers) != len(set(numbers)):
                return INIQUE_ERROR_MESSAGE
            for i in numbers:
                if i > 9 or i < 1:
                    return RANGE_ERROR_MESSAGE
            self.numbers = numbers
        except ValueError:
            return NOT_INT_ERROR_MESSAGE

    def get_result(self):
        bulls = 0
        cows = 0
        for i in range(len(self.numbers)):
            if self.numbers[i] == self.secret_numbers[i]:
                bulls += 1
            elif self.numbers[i] in self.secret_numbers:
                cows += 1

        if bulls == 4:
            Game.secret_numbers = generate_numbers(4)
            Game.stat_list.clear()
            return WIN_MESSAGE
        elif bulls or cows:
            return RESULT_MESSAGE.format(bulls=bulls, cows=cows)
        else:
            return MISSED_MESSAGE
