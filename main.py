import sys

from PyQt5.QtWidgets import QApplication

from conf.controller import Controller
from conf.model import Model
from conf.view import View

app = QApplication(sys.argv)

model = Model()
view = View(model)
controller = Controller(model, view)

sys.exit(app.exec())
