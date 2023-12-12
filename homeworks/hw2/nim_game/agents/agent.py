from random import randint

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """

    _level: AgentLevels  # уровень сложности

    def __init__(self, level: str) -> None:
        if level == 'easy':
            self._level = AgentLevels.EASY
        elif level == 'normal':
            self._level = AgentLevels.NORMAL
        elif level == 'hard':
            self._level = AgentLevels.HARD
        else:
            raise ValueError

    def easy_step(self, state_curr: list[int]):
        heap_id = 0
        decrease = 0
        while state_curr[heap_id] == 0:
            heap_id += 1
        decrease = randint(1, state_curr[heap_id])
        return heap_id, decrease

    def hard_step(self, state_curr: list[int]):
        heap_id = 0
        decrease = 0
        fl = True
        for i in range(len(state_curr)):
            if fl and state_curr[i] > 0:
                for j in range(1, state_curr[i]):
                    hor = 0
                    for k in range(len(state_curr)):
                        if k == i:
                            hor ^= state_curr[i] - j
                        else:
                            hor ^= state_curr[k]
                    if hor == 0:
                        fl = False
                        heap_id = i
                        decrease = j
        if fl:
            for i in range(len(state_curr)):
                if state_curr[i] > 0:
                    heap_id = i
                    decrease = 1
        return heap_id, decrease

    def make_step(self, state_curr: list[int]) -> NimStateChange:
        """
        Сделать шаг, соотвутствующий уровню сложности

        :param state_curr: список целых чисел - состояние кучек
        :return: стуктуру NimStateChange - описание хода
        """
        heap_id = 0
        decrease = 0
        if self._level == AgentLevels.EASY:
            heap_id, decrease = self.easy_step(state_curr)
        elif self._level == AgentLevels.NORMAL:
            r = randint(1, 2)
            if r == 1:
                heap_id, decrease = self.easy_step(state_curr)
            else:
                heap_id, decrease = self.hard_step(state_curr)
        elif self._level == AgentLevels.HARD:
            heap_id, decrease = self.hard_step(state_curr)

        return NimStateChange(heap_id=heap_id, decrease=decrease)
