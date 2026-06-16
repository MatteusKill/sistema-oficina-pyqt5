import sys
from PyQt5.QtWidgets import QApplication
from controllers.login_controller import LoginController


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("assets/style/style.qss", "r") as arquivo:
        estilo = arquivo.read()
    app.setStyleSheet(estilo)

    window = LoginController()
    window.show()
    sys.exit(app.exec_())