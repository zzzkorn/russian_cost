import pytest
from src.russian_coast import RussianCost


@pytest.mark.parametrize('cost, result', [
    ('8.32', 8.32),
    ('200', 200),
    ('200.345', 200.34),
    ('3.467', 3.47),
    ('3.411', 3.41),
    (200.345, 200.34),
    (3.467, 3.47),
    (3.411, 3.41),
    (200, 200),
])
def test_init_cost(cost, result):
    try:
        rus_cost = RussianCost(cost)
        assert rus_cost.coast == result
    except ValueError:
        assert False


@pytest.mark.parametrize('cost', [
    'Lorem',
    'FAB',
    '0,312',
])
def test_init_cost_exception(cost):
    try:
        RussianCost(cost)
        assert False
    except ValueError:
        assert True


@pytest.mark.parametrize('cost, result_cost, sign_str, cent_srt', [
    (-0.11, 'минус 11 копеек', True, False),
    (0.11, '11 копеек', True, False),
    (-0.11, 'минус одинадцать копеек', True, True),
    (0.11, 'одинадцать копеек', True, True),
    (-0.11, '- 11 копеек', False, False),
    (-0.11, '- одинадцать копеек', False, True),
    (0.23, 'двадцать три копейки', True, True),
    (0.41, 'сорок одна копейка', True, True),
    (0.99, 'девяносто девять копеек', True, True),
    (0.72, 'семьдесят две копейки', True, True),
    (0.60, 'шестьдесят копеек', True, True),
    (0.08, 'восемь копеек', True, True),
])
def test_string_cents(cost, result_cost, sign_str, cent_srt):
    str_cost = RussianCost(cost, sign_str=sign_str, cent_srt=cent_srt)
    assert str(str_cost) == result_cost
