from PyQt5.QtWidgets import QWidget
class View:
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.form=QWidget()
        self.form.show()
