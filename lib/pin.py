from PyQt5.QtCore import QObject, pyqtSignal


class AnalogType(QObject):
    updated = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.sensor_value: int = 0
        self.precision: int = 3
        self.sensor_low: int = 0
        self.sensor_high: int = 20000
        self.value_low: float = 0
        self.value_high: float = 1.0

    def set_range(self,
                  sensor_low: int = 0, sensor_high: int = 20000,
                  value_low: float = 0, value_high: float = 1.0):
        self.sensor_low: int = sensor_low
        self.sensor_high: int = sensor_high
        self.value_low: float = value_low
        self.value_high: float = value_high

    @property
    def slope(self) -> float:
        return (self.value_high-self.value_low)/(self.sensor_high-self.sensor_low)

    @property
    def offset(self) -> float:
        return self.value_low-self.sensor_low*self.slope

    def get_value(self):
        return round(self.sensor_value*self.slope+self.offset, self.precision)


class AnalogIn(AnalogType):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def set_sensor_value(self, value: int):
        if value != self.sensor_value:
            self.sensor_value = value
        self.updated.emit(self.get_value())


class AnalogOut(AnalogType):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.need_update: bool = False

    def set_value(self, value: float):
        v = round((value-self.offset)/self.slope)
        if v < self.sensor_low:
            v = self.sensor_low
        if v > self.sensor_high:
            v = self.sensor_high
        self.sensor_value = v
        self.need_update = True

    def set_sensor_value(self, value: int):
        if value == self.sensor_value:
            self.need_update = False
        self.updated.emit(self.get_value())


class DiscreteType(QObject):
    updated = pyqtSignal(bool)
    on = pyqtSignal()
    off = pyqtSignal()
    rise = pyqtSignal()
    fall = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.sensor_value: bool = False

    def get_value(self) -> bool:
        return self.sensor_value

    def emit_sinals(self, old_value: bool, new_value: bool):
        if new_value:
            self.on.emit()
        else:
            self.off.emit()

        if not old_value and new_value:
            self.rise.emit()
        if old_value and not new_value:
            self.fall.emit()

        self.updated.emit(new_value)


class DiscreteIn(DiscreteType):
    def set_sensor_value(self, value: bool):
        old = self.sensor_value
        self.sensor_value = value
        self.emit_sinals(old, value)


class DiscreteOut(DiscreteType):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.need_update: bool = False

    def set_value(self, value: bool):
        self.sensor_value = value
        self.need_update = True

    def set_sensor_value(self, value: bool):
        old = self.sensor_value
        if self.sensor_value == value:
            self.need_update = False
        self.emit_sinals(old, value)
