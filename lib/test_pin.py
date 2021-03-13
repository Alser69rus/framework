import pytest
from lib.pin import AnalogIn


@pytest.fixture(scope='function',
                params=[(0, 1, 0, 20000, 0, 0),
                        (0, 1, 0, 20000, 10000, 0.5),
                        (0, 1, 0, 20000, 20000, 1.0),
                        (0, 1, 0, 20000, 21000, 0),
                        (0, 1, 0, 20000, -1, 0),
                        (-1, 1, 0, 20000, 0, -1),
                        (-1, 1, 0, 20000, 10000, 0),
                        (-1, 1, 0, 20000, 20000, 1),
                        (1, 0, 0, 20000, 0, 1),
                        (1, 0, 0, 20000, 20000, 0),
                        (0, 1, 10, 0, 0, 1),
                        (0, 1, 10, 0, 10, 0),
                        ])
def ai_init_param(request):
    return request.param


def test_ai_default():
    ai = AnalogIn()
    assert ai.value == 0
    assert ai.sensor_range.low == 0
    assert ai.sensor_range.high == 20000
    assert ai.value_range.low == 0
    assert ai.value_range.high == 1.0
    assert ai.precision == 3
    assert ai.get_value() == 0


def test_ai(ai_init_param):
    low, high, s_low, s_high, s_value, value = ai_init_param

    ai = AnalogIn(low, high, s_low, s_high)
    ai.set_sensor_value(s_value)
    assert ai.get_value() == value
