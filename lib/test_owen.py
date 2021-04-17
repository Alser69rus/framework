from lib.owen import MV1108AC
import pytest


def test_mv110_8ac():
    ai = MV1108AC('12')
    assert not any([pin.get_value() for pin in ai.pin])


