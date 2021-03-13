from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from collections import namedtuple
import time


class AnalogIn(QObject):
    updated = pyqtSignal(float)
    changed = pyqtSignal(float)
    out_of_range = pyqtSignal()

    def __init__(self,
                 low: float = 0.0,
                 high: float = 1.0,
                 sensor_low: float = 0,
                 sensor_high: float = 20000,
                 precision: int = 3,
                 parent=None):
        super().__init__(parent=parent)
        self.active: bool = True
        self.value: float = low
        self.sensor_value: float = sensor_low
        self.precision: int = precision
        Range = namedtuple('Range', 'low high')
        self.sensor_range = Range(sensor_low, sensor_high)
        self.value_range = Range(low, high)
        self.description: str = ''
        self.eu = ''
        self.timestamp = time.time()

    @pyqtSlot(float)
    def set_sensor_value(self, sensor_value: float):
        if not self.active:
            return

        s_min = min(self.sensor_range.low, self.sensor_range.high)
        s_max = max(self.sensor_range.low, self.sensor_range.high)
        if not s_min <= sensor_value <= s_max:
            self.out_of_range.emit()
            return

        sr = self.sensor_range.high - self.sensor_range.low
        vr = self.value_range.high - self.value_range.low
        value = self.value_range.low + (sensor_value - self.sensor_range.low) * vr / sr
        value = round(value, self.precision)

        self.sensor_value = sensor_value
        if self.value != value:
            self.value = value
            self.changed.emit(self.value)
        self.timestamp = time.time()
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
