from random import randint

from nim_game.common.models import NimStateChange

STONE_AMOUNT_MIN = 1  # минимальное начальное число камней в кучке
STONE_AMOUNT_MAX = 10  # максимальное начальное число камней в кучке


class EnvironmentNim:
    """
    Класс для хранения и взаимодействия с кучками
    """

    _heaps: list[int]  # кучки

    def __init__(self, heaps_amount: int) -> None:
        if 2 <= heaps_amount <= 10:
            self._heaps = list()
            for i in range(heaps_amount):
                self._heaps.append(randint(STONE_AMOUNT_MIN, STONE_AMOUNT_MAX))
        else:
            raise ValueError

    def get_state(self) -> list[int]:
        """
        Получение текущего состояния кучек
        :return: копия списка с кучек
        """
        return self._heaps

    def change_state(self, state_change: NimStateChange) -> None:
        """
        Изменения текущего состояния кучек

        :param state_change: структура описывающая изменение состояния
        """
        if state_change.heap_id < 1 or state_change.heap_id > len(self._heaps):
            raise ValueError
        if state_change.decrease < 1 or state_change.decrease > self._heaps[state_change.heap_id-1]:
            raise ValueError

        self._heaps[state_change.heap_id - 1] -= state_change.decrease
