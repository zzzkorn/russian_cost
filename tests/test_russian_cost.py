#!/usr/bin/env python

import pytest
from russian_coast import RussianCost


@pytest.mark.parametrize(
    "cost, result",
    [
        ("8.32", 8.32),
        ("200", 200),
        ("200.345", 200.34),
        ("3.467", 3.47),
        ("3.411", 3.41),
        (200.345, 200.34),
        (3.467, 3.47),
        (3.411, 3.41),
        (200, 200),
    ],
)
def test_init_cost(cost, result):
    rus_cost = RussianCost(cost)
    assert rus_cost.coast == result


@pytest.mark.parametrize(
    "cost",
    [
        "Lorem",
        "FAB",
        "0,312",
    ],
)
def test_init_cost_exception(cost):
    with pytest.raises(ValueError):
        RussianCost(cost)


@pytest.mark.parametrize(
    "out_format",
    [
        "%C %r %p",
        "%s %U %p",
        "%s %r %dsd",
    ],
)
def test_init_format_exception(out_format):
    with pytest.raises(ValueError):
        RussianCost(3.3, out_format)


@pytest.mark.parametrize(
    "float_coast, result_cost, cost_format",
    [
        # Копейки
        (0.056, "6 копеек", "%s %r %p"),
        (0.01, "1 копейка", "%s %r %p"),
        (0.32, "32 копейки", "%s %r %p"),
        (0.99, "99 копеек", "%s %r %p"),
        (0.20, "20 копеек", "%s %r %p"),
        (-0.11, "минус 11 копеек", "%S %r %p"),
        (0.11, "11 копеек", "%S %r %p"),
        (-0.11, "минус одиннадцать копеек", "%S %R %P"),
        (0.11, "одиннадцать копеек", "%S %R %P"),
        (-0.11, "- 11 копеек", "%s %r %p"),
        (-0.11, "- одиннадцать копеек", "%s %R %P"),
        (0.23, "двадцать три копейки", "%s %R %P"),
        (0.41, "сорок одна копейка", "%s %R %P"),
        (0.99, "девяносто девять копеек", "%s %R %P"),
        (0.72, "семьдесят две копейки", "%s %R %P"),
        (0.60, "шестьдесят копеек", "%s %R %P"),
        (0.08, "восемь копеек", "%s %R %P"),
        # Рубли
        (1, "один рубль", "%s %R %P"),
        (8, "восемь рублей", "%S %R %P"),
        (99, "девяносто девять рублей", "%s %R %P"),
        (23, "двадцать три рубля", "%s %R %P"),
        (999, "девятьсот девяносто девять рублей", "%s %R %P"),
        (323, "триста двадцать три рубля", "%s %R %P"),
        (401, "четыреста один рубль", "%s %R %P"),
        (701401, "семьсот одна тысяча четыреста один рубль", "%s %R %P"),
        (999001, "девятьсот девяносто девять тысяч один рубль", "%s %R %P"),
        (100020, "сто тысяч двадцать рублей", "%s %R %P"),
        (100000, "сто тысяч рублей", "%s %R %P"),
        # Копейки + Рубли
        (1.12, "один рубль 12 копеек", "%s %R %p"),
        (8.73, "восемь рублей 73 копейки", "%s %R %p"),
        (23.12, "двадцать три рубля 12 копеек", "%s %R %p"),
        (100020.197, "сто тысяч двадцать рублей 20 копеек", "%s %R %p"),
    ],
)
def test_str_coast(float_coast, result_cost, cost_format):
    cost = RussianCost(float_coast, cost_format)
    assert str(cost) == result_cost
