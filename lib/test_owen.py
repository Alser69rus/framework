from lib.owen import MV1108AC
import pytest


@pytest.fixture(scope='function',
                params=[
                    ([0]*8, [0]*8),
                    ([20000]*8, [1.0]*8),
                    ([10000]*8, [0.5]*8),
                    ([10]*8, [0.001]*8),
                ])
def read_ai(request):
    return request.param


class Response():
    def __init__(self, value, error):
        self.registers = value
        self.error = error

    def isError(self):
        return self.error


class PortMock():
    def __init__(self, value):
        self.response = Response(value, False)

    def read_holding_registers(self, *args, **kwargs):
        return self.response


def test_mv110_8ac(read_ai):
    rr, value = read_ai
    port = PortMock(rr)
    ai = MV1108AC(port=port)
    ai.update()
    pin = [p.get_value() for p in ai.pin]
    assert pin == value
