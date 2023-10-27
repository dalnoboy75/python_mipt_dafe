"""
В этом модуле хранятся функции для применения МНК
"""

from typing import Optional
from numbers import Real  # раскомментируйте при необходимости

from ..event_logger.event_logger import EventLogger

from ..lsm.enumerations import MismatchStrategies
from ..lsm.models import (
    LSMDescription,
    LSMStatistics,
    LSMLines,
)

PRECISION = 3  # константа для точности вывода
event_logger = EventLogger()  # для логирования


def get_lsm_description(
        abscissa: list[float], ordinates: list[float],
        mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> LSMDescription:
    """
    Функции для получения описания рассчитаной зависимости

    :param: abscissa - значения абсцисс
    :param: ordinates - значение ординат
    :param: mismatch_strategy - стратегия обработки несовпадения

    :return: структура типа LSMDescription
    """

    global event_logger

    # ваш код
    # эту строчку можно менять
    abscissa = list(abscissa)
    ordinates = list(ordinates)

    _is_valid_measurments(abscissa)
    _is_valid_measurments(ordinates)

    if len(abscissa) != len(ordinates):
        if mismatch_strategy == MismatchStrategies.FALL:
            raise RuntimeError
        elif mismatch_strategy == MismatchStrategies.CUT:
            abscissa, ordinates = _process_mismatch(abscissa, ordinates)
        else:
            raise ValueError

    return _get_lsm_description(abscissa, ordinates)


def get_lsm_lines(
        abscissa: list[float], ordinates: list[float],
        lsm_description: Optional[LSMDescription] = None
) -> LSMLines:
    """
    Функция для расчета значений функций с помощью результатов МНК

    :param: abscissa - значения абсцисс
    :param: ordinates - значение ординат
    :param: lsm_description - описание МНК

    :return: структура типа LSMLines
    """

    # ваш код
    # эту строчку можно менять
    if lsm_description is None:
        lsm_description = get_lsm_description(abscissa, ordinates)
    if type(lsm_description) is not LSMDescription:
        raise TypeError

    a = lsm_description.incline
    b = lsm_description.shift
    da = lsm_description.incline_error
    db = lsm_description.shift_error
    line_predicted = [a * i + b for i in abscissa]
    line_above = [(a + da) * i + b + db for i in abscissa]
    line_under = [(a - da) * i + b - db for i in abscissa]
    return LSMLines(abscissa, ordinates, line_predicted, line_above, line_under)


def get_report(
        lsm_description: LSMDescription, path_to_save: str = ''
) -> str:
    """
    Функция для формирования отчета о результатах МНК

    :param: lsm_description - описание МНК
    :param: path_to_save - путь к файлу для сохранения отчета

    :return: строка - отчет определенного формата
    """
    global PRECISION

    report = '\n'.join([
        "=" * 40 + "LSM computing result" + "=" * 40 + "\n",
        "[INFO]: incline: " + f'{lsm_description.incline:.{PRECISION}f}' + ";",
        "[INFO]: shift: " + f'{lsm_description.shift:.{PRECISION}f}' + ";",
        "[INFO]: incline error: " + f'{lsm_description.incline_error:.{PRECISION}f}' + ";",
        "[INFO]: shift error: " + f'{lsm_description.shift_error:.{PRECISION}f}' + ";",
        "\n" + "=" * 100
    ])
    if path_to_save != "":
        with open(path_to_save, 'w', encoding='utf-8') as f:
            f.write(report)
    return report


# служебная функция для валидации
def _is_valid_measurments(measurments: list[float]):
    # ваш код
    # эту строчку можно менять
    if type(measurments) is not list:
        raise TypeError

    if len(measurments) < 3:
        raise ValueError

    if not all(isinstance(i, Real) for i in measurments):
        raise ValueError


# служебная функция для обработки несоответствия размеров
def _process_mismatch(
        abscissa: list[float], ordinates: list[float],
        mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
) -> tuple[list[float], list[float]]:
    global event_logger

    # ваш код
    # эту строчку можно менять
    if len(abscissa) > len(ordinates):
        abscissa = abscissa[:len(ordinates)]
    else:
        ordinates = ordinates[:len(abscissa)]
    return abscissa, ordinates


# служебная функция для получения статистик
def _get_lsm_statistics(
        abscissa: list[float], ordinates: list[float]
) -> LSMStatistics:
    global event_logger, PRECISION

    # ваш код
    # эту строчку можно менять

    return LSMStatistics(
        abscissa_mean=0,
        ordinate_mean=0,
        product_mean=0,
        abs_squared_mean=0
    )


# служебная функция для получения описания МНК
def _get_lsm_description(
        abscissa: list[float], ordinates: list[float]
) -> LSMDescription:
    global event_logger, PRECISION

    # ваш код
    # эту строчку можно менять
    n = len(abscissa)
    xy = 0
    x = 0
    y = 0
    x2 = 0
    for i in range(n):
        xy += abscissa[i] * ordinates[i]
    xy /= n
    x = sum(abscissa) / n
    y = sum(ordinates) / n
    for i in abscissa:
        x2 += i ** 2
    x2 /= n
    a = (xy - x * y) / (x2 - x ** 2)
    b = y - a * x
    dy2 = 0
    for i in range(n):
        dy2 += (ordinates[i] - a * abscissa[i] - b) ** 2
    dy2 *= 1 / (n - 2)
    da = (dy2 / (n * (x2 - x ** 2))) ** 0.5
    db = (dy2 * x2 / (n * (x2 - x ** 2))) ** 0.5
    return LSMDescription(a, b, da, db)
