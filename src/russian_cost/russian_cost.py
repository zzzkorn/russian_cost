#!/usr/bin/env python
"""
Модуль для преобразования стоимости в строку
"""
import math
import re
from typing import Union

DIGIT_DICT = {
    "penny": {
        1: "одна",
        2: "две",
        3: "три",
    },
    "thousand": {
        1: "одна",
        2: "две",
        3: "три",
    },
    1: "один",
    2: "два",
    3: "три",
    4: "четыре",
    5: "пять",
    6: "шесть",
    7: "семь",
    8: "восемь",
    9: "девять",
    10: "десять",
    11: "одиннадцать",
    12: "двенадцать",
    13: "тринадцать",
    14: "четырнадцать",
    15: "пятнадцать",
    16: "шестнадцать",
    17: "семнадцать",
    18: "восемнадцать",
    19: "девятнадцать",
    20: "двадцать",
    30: "тридцать",
    40: "сорок",
    50: "пятьдесят",
    60: "шестьдесят",
    70: "семьдесят",
    80: "восемьдесят",
    90: "девяносто",
    100: "сто",
    200: "двести",
    300: "триста",
    400: "четыреста",
    500: "пятьсот",
    600: "шестьсот",
    700: "семьсот",
    800: "восемьсот",
    900: "девятьсот",
}


class RussianCost:
    """
    Класс для преобразования стоимости в строку
    """

    def __init__(
        self,
        cost: Union[int, float, str],
        out_format: str = "%S %R %P",
    ):
        self._cost = None
        self._rubles = None
        self._penny = None
        self._out_format = None

        self.cost = cost
        self.out_format = out_format

    def __str__(self):
        return self.strfcost(self.out_format)

    def __repr__(self):
        return self.strfcost(self.out_format)

    def __call__(self):
        return self.strfcost(self.out_format)

    def _get_rubles_str(
        self,
        rubles,
        index=1,
        rubles_str=str(),
        unit=True,
    ) -> str:
        if not rubles:
            return re.sub(" +", " ", rubles_str.strip())
        if unit:
            ten = int(rubles % 100)
            rubles_str = {
                True: lambda x: "{} {} {}".format(
                    self.cost_digits_str(x, index),
                    self.unit_str(index, x),
                    rubles_str,
                ),
                False: lambda x: "{} {} {} {}".format(
                    (
                        self.cost_digits_str(
                            x - x % 10,
                            index,
                        )
                        if x - x % 10
                        else str()
                    ),
                    self.cost_digits_str(x % 10, index) if x % 10 else str(),
                    self.unit_str(index, x),
                    rubles_str,
                ),
            }[10 < ten < 19](ten)
            index, rubles, unit = index * 100, rubles // 100, False
        else:
            hundreds = int((rubles % 10) * 100)
            rubles_str = "{} {}".format(
                self.cost_digits_str(hundreds, index) if hundreds else str(),
                rubles_str,
            )
            index, rubles, unit = index * 10, rubles // 10, True
        return self._get_rubles_str(rubles, index, rubles_str, unit)

    def _get_sign(self, is_string=True) -> str:
        return {
            True: lambda x: str() if x else "минус",
            False: lambda x: str() if x else "-",
        }[is_string](True if self.cost > 0 else False)

    def _get_penny(self, is_string=True) -> str:
        if not self._penny:
            return str()
        unit = self.unit_str(0, self._penny)
        if 11 <= self._penny <= 19:
            return {
                True: "{} {}".format(
                    self.cost_digits_str(self._penny, 0),
                    unit,
                ),
                False: "{} {}".format(self._penny, unit),
            }[is_string]
        units, tens = self._penny % 10, self._penny // 10
        return {
            True: "{} {} {}".format(
                self.cost_digits_str(tens * 10, 0) if tens else str(),
                self.cost_digits_str(units, 0) if units else str(),
                unit,
            ),
            False: "{} {}".format(self._penny, unit),
        }[is_string]

    def _get_rubles(self, is_string=True) -> str:
        if not self._rubles:
            return str()
        if not is_string:
            unit = self.unit_str(1, self._rubles)
            return "{} {}".format(self._rubles, unit)
        return self._get_rubles_str(self._rubles)

    @staticmethod
    def prepare_out_format(out_format: str) -> str:
        if not isinstance(out_format, str):
            raise ValueError(
                "Формат вывода стоимости должен передаваться в виде строки"
            )
        i, n = 0, len(out_format)
        while i < n:
            ch, i = out_format[i], i + 1
            if ch == "%" and i < n:
                ch, i = out_format[i], i + 1
                if ch not in {"s", "S", "r", "R", "p", "P"}:
                    err_msg = "Формат вывода не поддерживает: {}".format(ch)
                    raise ValueError(err_msg)
        return re.sub(" +", " ", out_format.strip())

    @staticmethod
    def prepare_cost(cost: Union[int, float, str]) -> float:
        try:
            temp_val = float(cost)
        except ValueError:
            raise ValueError(
                "Проверьте правильность переменной: {}".format(cost),
            )
        return round(temp_val, 2)

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        self._cost = self.prepare_cost(value)
        penny, rubles = math.modf(math.fabs(self._cost))
        self._rubles = int(rubles)
        self._penny = int(round(penny, 2) * 100)

    @property
    def out_format(self):
        return self._out_format

    @out_format.setter
    def out_format(self, value):
        self._out_format = self.prepare_out_format(value)

    @staticmethod
    def unit_str(index, value):
        limit = value % 10
        return {
            0: (
                "копеек"
                if 11 <= value <= 20 or not limit or 5 <= limit <= 9
                else ("копейка" if limit == 1 else "копейки")
            ),
            1: (
                "рублей"
                if 11 <= value <= 20 or not limit or 5 <= limit <= 9
                else ("рубль" if limit == 1 else "рубля")
            ),
            1000: (
                "тысяч"
                if 11 <= value <= 20 or not limit or 5 <= limit <= 9
                else ("тысяча" if limit == 1 else "тысячи")
            ),
            pow(10, 6): (
                "миллионов"
                if 11 <= value <= 20 or not limit or 5 <= limit <= 9
                else ("миллион" if limit == 1 else "миллиона")
            ),
            pow(10, 9): (
                "миллиардов"
                if 11 <= value <= 20 or not limit or 5 <= limit <= 9
                else ("миллиард" if limit == 1 else "миллиарда")
            ),
            pow(10, 12): (
                "триллионов"
                if 11 <= value <= 20 or not limit or 5 <= limit <= 9
                else ("триллион" if limit == 1 else "триллиона")
            ),
            pow(10, 15): (
                "квадриллионов"
                if 11 <= value <= 20 or not limit or 5 <= limit <= 9
                else ("квадриллион" if limit == 1 else "квадриллиона")
            ),
            pow(10, 18): (
                "квинтиллионов"
                if 11 <= value <= 20 or not limit or 5 <= limit <= 9
                else ("квинтиллион" if limit == 1 else "квинтиллиона")
            ),
        }.get(index)

    @staticmethod
    def cost_digits_str(cost, index):
        cost_digits_str = None
        if index == 0:
            cost_digits_str = DIGIT_DICT["penny"].get(cost)
        if index == 1000:
            cost_digits_str = DIGIT_DICT["thousand"].get(cost)
        if not cost_digits_str:
            cost_digits_str = DIGIT_DICT.get(cost)
        return cost_digits_str

    def strfcost(self, out_format: str) -> str:
        data = []
        i, n = 0, len(out_format)
        while i < n:
            ch, i = out_format[i], i + 1
            if ch == "%" and i < n:
                ch, i = out_format[i], i + 1
                if ch == "s":
                    data.append(self._get_sign(is_string=False))
                elif ch == "S":
                    data.append(self._get_sign(is_string=True))
                elif ch == "r":
                    data.append(self._get_rubles(is_string=False))
                elif ch == "R":
                    data.append(self._get_rubles(is_string=True))
                elif ch == "p":
                    data.append(self._get_penny(is_string=False))
                elif ch == "P":
                    data.append(self._get_penny(is_string=True))
            else:
                data.append(ch)
        return re.sub(" +", " ", "".join(data).strip())


def strfcost(
    cost: Union[int, float, str],
    out_format: str = "%S %R %P",
) -> str:
    return RussianCost(cost, out_format)()
