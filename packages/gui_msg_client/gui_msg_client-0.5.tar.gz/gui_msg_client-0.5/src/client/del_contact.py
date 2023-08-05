from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QApplication
from PyQt5.QtCore import Qt


class DelContactDialog(QDialog):
    """Client class representing a window for removing a contact from the contact list."""

    def __init__(self, database):
        """DelContactDialog window initialization and description method.

        :type db: `client.client_database.ClientBase`"""

        super().__init__()
        self.db = database

        self.setFixedSize(350, 120)
        self.setWindowTitle('Delete a contact')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Select a contact for removing:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_ok = QPushButton('Delete', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Cancel', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        self.selector.addItems(sorted(self.db.get_contacts()))


if __name__ == '__main__':
    app = QApplication([])
    window = DelContactDialog(None)
    window.show()
    app.exec_()
