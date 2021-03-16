import pytest
from lib.pin import AnalogIn, AnalogOut, DiscreteIn, DiscreteOut


@pytest.fixture(scope='function',
                params=[
                    (0, 1.0, 0, 20000, 0, 0),
                    (0, 1.0, 0, 20000, 10000, 0.5),
                    (0, 1.0, 0, 20000, 20000, 1.0),
                    (1.0, 0, 0, 20000, 20000, 0),
                    (1.0, 0, 0, 20000, 0, 1.0),
                    (-1, 1, 0, 20000, 0, -1),
                    (-1, 1, 0, 20000, 10000, 0),
                    (-1, 1, 0, 20000, 20000, 1),
                    (0, 1.6, 4000, 20000, 0, -0.4),
                    (0, 1.6, 4000, 20000, 4000, 0),
                    (0, 1.6, 4000, 20000, 12000, 0.8),
                    (0, 1.6, 4000, 20000, 20000, 1.6),
                    (0, 1.6, 4000, 20000, 5123, 0.112),
                    (0, 1.6, 4000, 20000, 5686, 0.169),
                ])
def ai_param(request):
    return request.param


def test_ai(ai_param):
    low, high, s_low, s_high, sensor, value = ai_param
    ai = AnalogIn(low=low, high=high, sensor_low=s_low, sensor_high=s_high)
    ai.set_sensor_value(sensor)
    assert ai.get_value() == value


@pytest.fixture(scope='function',
                params=[
                    (0, 1.0, 0, 1000, 0, 0),
                    (0, 1.0, 0, 1000, 0.5, 500),
                    (0, 1.0, 0, 1000, 1.0, 1000),
                    (0, 1.0, 0, 1000, 1.1, 1000),
                    (0, 1.0, 0, 1000, -1, 0),
                    (0, 1.0, 0, 1000, 0.1004, 100),
                ])
def ao_param(request):
    return request.param


def test_ao(ao_param):
    low, high, s_low, s_high, value, sensor_value = ao_param
    ao = AnalogOut(low=low, high=high, sensor_low=s_low, sensor_high=s_high)
    assert not ao.need_update
    ao.set_value(value)
    assert ao.need_update
    assert sensor_value == ao.sensor_value
    ao.set_sensor_value(sensor_value)
    assert not ao.need_update


def test_di():
    di = DiscreteIn()
    assert not di.get_value()
    di.set_sensor_value(True)
    assert di.get_value()
    di.set_sensor_value(False)
    assert not di.get_value()


def test_do():
    do = DiscreteOut()
    assert not do.need_update
    assert not do.get_value()

    do.set_value(True)
    assert do.need_update
    assert do.get_value()
    do.set_sensor_value(True)
    assert not do.need_update
    assert do.get_value()

    do.set_value(False)
    assert do.need_update
    assert not do.get_value()
    do.set_sensor_value(False)
    assert not do.need_update
    assert not do.get_value()
