from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtCore import QEasingCurve
from views.main import Ui_MainWindow
import qtawesome as qta


class MainController(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("GMA Auto Gestão")
        self.setMinimumSize(1000, 600)

        self.sidebar_aberta = True

        self.ui.btn_dashboard.setIcon(qta.icon('fa5s.home', color='#c9d8eb'))
        self.ui.btn_clientes.setIcon(qta.icon('fa5s.users', color='#c9d8eb'))
        self.ui.btn_carros.setIcon(qta.icon('fa5s.car', color='#c9d8eb'))
        self.ui.btn_servicos.setIcon(qta.icon('fa5s.wrench', color='#c9d8eb'))
        self.ui.btn_ordens.setIcon(qta.icon('fa5s.clipboard-list', color='#c9d8eb'))
        self.ui.btn_sair.setIcon(qta.icon('fa5s.sign-out-alt', color='#e74c3c'))
        self.ui.btn_toggle.setIcon(qta.icon('fa5s.bars', color='#c9d8eb'))
        self.ui.btn_toggle.setText("")

        from controllers.clientes_controller import ClientesController
        self.tela_clientes = ClientesController()
        self.ui.stackedWidget.addWidget(self.tela_clientes)

        from controllers.carros_controller import CarrosController
        self.tela_carros = CarrosController()
        self.ui.stackedWidget.addWidget(self.tela_carros)

        from controllers.servicos_controller import ServicosController
        self.tela_servicos = ServicosController()
        self.ui.stackedWidget.addWidget(self.tela_servicos)

        from controllers.ordens_controller import OrdensController
        self.tela_ordens = OrdensController()
        self.ui.stackedWidget.addWidget(self.tela_ordens)

        self.ui.btn_toggle.clicked.connect(self.toggle_sidebar)
        self.ui.btn_dashboard.clicked.connect(self.abrir_dashboard)
        self.ui.btn_clientes.clicked.connect(self.abrir_clientes)
        self.ui.btn_carros.clicked.connect(self.abrir_carros)
        self.ui.btn_servicos.clicked.connect(self.abrir_servicos)
        self.ui.btn_ordens.clicked.connect(self.abrir_ordens)
        self.ui.btn_sair.clicked.connect(self.sair)
        self.ui.btn_logout.clicked.connect(self.sair)

        self.ui.btn_dashboard.setToolTip("Dashboard")
        self.ui.btn_clientes.setToolTip("Clientes")
        self.ui.btn_carros.setToolTip("Carros")
        self.ui.btn_servicos.setToolTip("Serviços")
        self.ui.btn_ordens.setToolTip("Ordens de Serviço")
        self.ui.btn_sair.setToolTip("Sair")
        self.ui.btn_toggle.setToolTip("Abrir/Fechar menu")

    def toggle_sidebar(self):
        if self.sidebar_aberta == True:
            largura_alvo = 55
        else:
            largura_alvo = 220

        self.animacao_max = QPropertyAnimation(self.ui.sidebar, b"maximumWidth")
        self.animacao_max.setDuration(250)
        self.animacao_max.setStartValue(self.ui.sidebar.width())
        self.animacao_max.setEndValue(largura_alvo)
        self.animacao_max.setEasingCurve(QEasingCurve.InOutQuart)

        self.animacao_min = QPropertyAnimation(self.ui.sidebar, b"minimumWidth")
        self.animacao_min.setDuration(250)
        self.animacao_min.setStartValue(self.ui.sidebar.width())
        self.animacao_min.setEndValue(largura_alvo)
        self.animacao_min.setEasingCurve(QEasingCurve.InOutQuart)

        self.animacao_max.start()
        self.animacao_min.start()

        if self.sidebar_aberta == True:
            self.sidebar_aberta = False

            self.ui.btn_dashboard.setText("")
            self.ui.btn_clientes.setText("")
            self.ui.btn_carros.setText("")
            self.ui.btn_servicos.setText("")
            self.ui.btn_ordens.setText("")
            self.ui.btn_sair.setText("")
        else:
            self.sidebar_aberta = True

            self.ui.btn_dashboard.setText("Dashboard")
            self.ui.btn_clientes.setText("Clientes")
            self.ui.btn_carros.setText("Carros")
            self.ui.btn_servicos.setText("Serviços")
            self.ui.btn_ordens.setText("Ordens de Serviço")
            self.ui.btn_sair.setText("Sair")

    def abrir_dashboard(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def abrir_clientes(self):
        self.ui.stackedWidget.setCurrentWidget(self.tela_clientes)

    def abrir_carros(self):
        self.ui.stackedWidget.setCurrentWidget(self.tela_carros)

    def abrir_servicos(self):
        self.ui.stackedWidget.setCurrentWidget(self.tela_servicos)

    def abrir_ordens(self):
        self.ui.stackedWidget.setCurrentWidget(self.tela_ordens)

    def sair(self):
        from controllers.login_controller import LoginController
        self.tela_login = LoginController()
        self.tela_login.show()
        self.close()