import time

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class AnalogType(QObject):
    updated = pyqtSignal(float)

    def __init__(self,
                 low: float = 0.0,
                 high: float = 1.0,
                 sensor_low: int = 0,
                 sensor_high: int = 20000,
                 precision: int = 3,
                 parent=None):
        super().__init__(parent=parent)
        self.active: bool = True
        self._sensor_value: int = sensor_low
        self.precision: int = precision
        self.low: float = low
        self.high: float = high
        self.sensor_low: int = sensor_low
        self.sensor_high: int = sensor_high
        self.timestamp = time.time()

    def get_value(self) -> float:
        s_range = self.sensor_high - self.sensor_low
        v_range = self.high - self.low
        value = self.low + (self._sensor_value - self.sensor_low) * v_range / s_range
        return round(value, self.precision)

    @property
    def sensor_value(self) -> int:
        return self._sensor_value


class AnalogIn(AnalogType):
    @pyqtSlot(int)
    def set_sensor_value(self, sensor_value: int):
        if not self.active:
            return
        self.timestamp = time.time()
        self._sensor_value = sensor_value
        self.updated.emit(self.get_value())


class AnalogOut(AnalogType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._need_update: bool = False

    @property
    def need_update(self):
        return self._need_update

    @pyqtSlot(float)
    def set_value(self, value: float):
        if not self.active:
            return

        s_range = self.sensor_high - self.sensor_low
        v_range = self.high - self.low
        sensor_value = self.sensor_low + (value - self.low) * s_range / v_range
        sensor_value = round(sensor_value)

        s_min = min(self.sensor_low, self.sensor_high)
        s_max = max(self.sensor_low, self.sensor_high)
        if sensor_value < s_min:
            sensor_value = s_min
        elif sensor_value > s_max:
            sensor_value = s_max

        self._need_update = True
        self._sensor_value = sensor_value

    @pyqtSlot(int)
    def set_sensor_value(self, sensor_value: int):
        if not self.active:
            return

        self.timestamp = time.time()
        if self._sensor_value == sensor_value:
            self._need_update = False
        self.updated.emit(self.get_value())


class DiscreteType(QObject):
    updated = pyqtSignal(bool)
    on = pyqtSignal()
    off = pyqtSignal()
    rise = pyqtSignal()
    fall = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.active: bool = True
        self._sensor_value: bool = False
        self.timestamp = time.time()

    def get_value(self) -> bool:
        return self._sensor_value

    def signals_emit(self, value):
        if self._sensor_value != value:
            if value:
                self.rise.emit()
            else:
                self.fall.emit()
        if value:
            self.on.emit()
        else:
            self.off.emit()
        self.updated.emit(value)


class DiscreteIn(DiscreteType):
    @pyqtSlot(bool)
    def set_sensor_value(self, value: bool):
        if not self.active:
            return
        self.timestamp = time.time()
        self.signals_emit(value)
        self._sensor_value = value


class DiscreteOut(DiscreteType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._need_update: bool = False

    @property
    def need_update(self) -> bool:
        return self._need_update

    def set_value(self, value: bool):
        if not self.active:
            return
        self._need_update = True
        self._sensor_value = value

    def set_sensor_value(self, value: bool):
        if not self.active:
            return
        self.timestamp = time.time()
        self.signals_emit(value)
        if self._sensor_value == value:
            self._need_update = False
