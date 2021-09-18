#!/usr/bin/env python
"""
Модуль для преобразования стоимости в строку
"""
from math import fabs

CENTS_DIGITS = {
    1: 'одна',
    2: 'две',
    3: 'три',
    4: 'четыре',
    5: 'пять',
    6: 'шесть',
    7: 'семь',
    8: 'восемь',
    9: 'девять',
    11: 'одинадцать',
    12: 'двенадцать',
    13: 'тринадцать',
    14: 'четырнадцать',
    15: 'пятнадцать',
    16: 'шестнадцать',
    17: 'семнадцать',
    18: 'восемнадцать',
    19: 'девятнадцать',
    20: 'двадцать',
    30: 'тридцать',
    40: 'сорок',
    50: 'пятьдесят',
    60: 'шестьдесят',
    70: 'семьдесят',
    80: 'восемдесят',
    90: 'девяносто',
}


class Coast:
    """
    Дескриптор стоимости
    """

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        temp_val = float()
        if isinstance(value, str):
            try:
                temp_val = float(value)
            except ValueError:
                raise ValueError(
                    'Проверьте правильность переменной: {}'.format(value),
                )
        elif isinstance(value, int):
            temp_val = float(value)
        elif isinstance(value, float):
            temp_val = value
        instance.__dict__[self.name] = round(temp_val, 2)


class RussianCost:
    """
    Класс для преобразования стоимости в строку
    """
    coast = Coast('coast')

    def __init__(self, cost, sign_str=False, ruble_str=False, cent_srt=False):
        self._sign_str = sign_str
        self._ruble_str = ruble_str
        self._cent_str = cent_srt

        self.coast = cost

    @property
    def sign(self):
        return {
            True: lambda x: str() if x else "минус",
            False: lambda x: str() if x else "-",
        }[self._sign_str](True if self.coast > 0 else False)

    @property
    def cents(self):
        cents = int(fabs(self.coast) % 1 * 100)
        if not cents:
            return str()
        elif 11 <= cents <= 19:
            return {
                True: '{} копеек'.format(CENTS_DIGITS.get(cents)),
                False: '{} копеек'.format(cents)
            }[self._cent_str]
        units, tens = cents % 10, cents // 10
        postfix = 'копейка' if units == 1 else 'копейки' if units in (
            2, 3, 4) else 'копеек'
        return {
            True: '{} {} {}'.format(
                CENTS_DIGITS.get(tens * 10) if tens else str(),
                CENTS_DIGITS.get(units) if units else str(),
                postfix,
            ),
            False: '{} {}'.format(cents, postfix),
        }[self._cent_str]

    def __str__(self):
        return '{} {}'.format(self.sign, self.cents).strip().replace('  ', ' ')

    def __repr__(self):
        return '{} {}'.format(self.sign, self.cents).strip().replace('  ', ' ')


# print(RussianCost(0.08, sign_str=True, cent_srt=True))
# print([RussianCost(-0.38, sign_str=True), RussianCost(-0.234)])
