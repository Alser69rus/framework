from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from collections import namedtuple


class AnalogIn(QObject):
    updated = pyqtSignal(float)
    changed = pyqtSignal(float)
    out_of_range = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.active: bool = True
        self.value: float = 0.0
        self.sensor_value: float = 0
        self.precision: int = 4
        Range = namedtuple('Range', 'low high')
        self.sensor_range = Range(0, 20000)
        self.value_range = Range(0, 1.0)
        self.eu = ''

    @pyqtSlot(float)
    def set_value(self, sensor_value: float):
        if not self.active:
            return
        if sensor_value < self.sensor_range.low or sensor_value > self.sensor_range.high:
            self.out_of_range.emit()
            return
        sr = self.sensor_range.high - self.sensor_range.low
        vr = self.value_range.high - self.value_range.low
        value = self.value_range.low + (sensor_value - self.sensor_value.low) * vr / sr
        value = round(value, self.precision)
        self.sensor_value = sensor_value
        if self.value != value:
            self.value = value
            self.changed.emit(self.value)
        self.updated.emit(self.value)

    def get_value(self) -> float:
        return self.value


class AnalogOut:
    pass


class DiscreteIn:
    pass


class DiscreteOut:
    pass


class MultiStateIn:
    pass


class MultiStateOut:
    pass
