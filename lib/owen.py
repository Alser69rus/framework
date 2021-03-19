from PyQt5.QtCore import QObject
from lib.pin import AnalogIn
from typing import List


# class OwenModule(QtCore.QObject):
#     updated = QtCore.pyqtSignal()
#     warning = QtCore.pyqtSignal(str)
#     changed = QtCore.pyqtSignal()
#     active_change = QtCore.pyqtSignal(bool)
#
#     def __init__(self, port=None, dev=None, name=None, parent=None):
#         super().__init__(parent)
#         self.value = None
#         self.error = None
#         self.port = port
#         self.dev = dev
#         self.active = False
#         self.name = name
#
#     def _read_data(self, data):
#         pass
#
#     def _unpack_data(self, pack):
#         pass
#
#     def _pack_data(self, data):
#         pass
#
#     def _write_data(self, pack):
#         pass
#
#     def _emit_warning(self, data, error):
#         self.error = error
#         self.warning.emit('{} warning: {}'.format(self.name, self.error))
#         return data
#
#     @QtCore.pyqtSlot(bool)
#     def setActive(self, value=True):
#         if self.active != value:
#             self.active = value
#             self.active_change.emit(value)
#
# class OwenInputModule(OwenModule):
#     def __init__(self, port=None, dev=None, name=None, parent=None):
#         super().__init__(port=port, dev=dev, name=name, parent=parent)
#
#     def update(self):
#         if self.active:
#             Maybe(self.port)(self._read_data)(self._unpack_data)(self._emit_updated).or_else(self._emit_warning)
#
#     def _emit_updated(self, data):
#         if data != self.value:
#             self.value = data
#             self.changed.emit()
#         self.updated.emit()
#         return data
# class AI8(OwenInputModule):
#     def __init__(self, port=None, dev=None, name='AI', parent=None):
#         super().__init__(port=port, dev=dev, name=name, parent=parent)
#         self.value = [0] * 8
#         self.k = [1] * 8
#         self.off = [0] * 8
#         self.eps = [1] * 8
#
#     def _read_data(self, port):
#         return port.execute(self.dev, cst.READ_INPUT_REGISTERS, 256, 8)
#
#     def _unpack_data(self, data):
#         values = [i if i < 32768 else 655536 - i for i in data]
#         values = [values[i] * self.k[i] + self.off[i] for i in range(8)]
#         values = [i if i != 32768 else None for i in values]
#         return values
#
#     def _emit_updated(self, values):
#         if any([abs(self.value[i] - values[i]) > self.eps[i] for i in range(8)]):
#             self.value = values
#             self.changed.emit()
#         self.updated.emit()
#         return values

class MV1108AC(QObject):
    def __init__(self, port, unit: int = 16, parent=None):
        super().__init__(parent=parent)
        self.port = port
        self.unit: int = unit
        self.pin: List[AnalogIn] = [AnalogIn()] * 8

    def check(self) -> bool:
        pass

    def update(self):
        rr = self.port.read_holding_registers(0x100, 8, unit=self.unit)
        if rr.isError():
            # logging.warning(f"не удалось прочитать {self.name} с ошибкой {rr}")
            return
        for i, pin in enumerate(self.pin):
            pin.set_sensor_value(rr.registers[i])
        # self.timestamp = datetime.now()
        # self.updated.emit()
