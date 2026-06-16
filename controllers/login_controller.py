from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from database.conexao import get_conexao
from database.conexao import fechar_conexao


class LoginController(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("GMA Auto Gestão")
        self.setMinimumSize(900, 600)
        self.setStyleSheet("background-color: #0d1b2e;")

        central = QWidget()
        self.setCentralWidget(central)

        layout_principal = QHBoxLayout(central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        self.painel_esquerdo = QWidget()
        self.painel_esquerdo.setStyleSheet("background-color: #f0f2f5;")
        self.painel_esquerdo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout_esquerdo = QVBoxLayout(self.painel_esquerdo)
        layout_esquerdo.setAlignment(Qt.AlignCenter)

        self.label_imagem = QLabel()
        self.label_imagem.setAlignment(Qt.AlignCenter)

        pixmap = QPixmap("assets/img/oficina.png")

        if pixmap.isNull() == False:
            self.label_imagem.setPixmap(
                pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            self.label_imagem.setText("GMA")
            self.label_imagem.setStyleSheet("font-size: 80px;")

        layout_esquerdo.addWidget(self.label_imagem)

        self.painel_direito = QWidget()
        self.painel_direito.setStyleSheet("background-color: #1a3a6b;")
        self.painel_direito.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout_direito = QVBoxLayout(self.painel_direito)
        layout_direito.setAlignment(Qt.AlignCenter)
        layout_direito.setContentsMargins(50, 50, 50, 50)
        layout_direito.setSpacing(12)

        label_titulo = QLabel("GMA Auto Gestão")
        label_titulo.setAlignment(Qt.AlignCenter)
        label_titulo.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold; background: transparent;")

        label_subtitulo = QLabel("Sistema de Oficina & Serviços")
        label_subtitulo.setAlignment(Qt.AlignCenter)
        label_subtitulo.setStyleSheet("color: #c9d8eb; font-size: 13px; background: transparent;")

        label_usuario = QLabel("Usuário")
        label_usuario.setStyleSheet("color: #c9d8eb; font-size: 13px; background: transparent;")

        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Digite seu e-mail")
        self.input_usuario.setMaximumWidth(400)
        self.input_usuario.setStyleSheet("""
            QLineEdit {
                background-color: #0d1b2e;
                color: #ffffff;
                border: 1px solid #1e6db5;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #4ab3e8;
            }
        """)

        label_senha = QLabel("Senha")
        label_senha.setStyleSheet("color: #c9d8eb; font-size: 13px; background: transparent;")

        self.input_senha = QLineEdit()
        self.input_senha.setPlaceholderText("Digite sua senha")
        self.input_senha.setEchoMode(QLineEdit.Password)
        self.input_senha.setMaximumWidth(400)
        self.input_senha.setStyleSheet("""
            QLineEdit {
                background-color: #0d1b2e;
                color: #ffffff;
                border: 1px solid #1e6db5;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #4ab3e8;
            }
        """)

        self.btn_entrar = QPushButton("ENTRAR")
        self.btn_entrar.setMaximumWidth(400)
        self.btn_entrar.setStyleSheet("""
            QPushButton {
                background-color: #1e6db5;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #4ab3e8;
            }
        """)
        self.btn_entrar.clicked.connect(self.fazer_login)

        self.label_erro = QLabel("")
        self.label_erro.setAlignment(Qt.AlignCenter)
        self.label_erro.setStyleSheet("color: #e74c3c; font-size: 12px; background: transparent;")

        layout_direito.addWidget(label_titulo)
        layout_direito.addWidget(label_subtitulo)
        layout_direito.addWidget(label_usuario)
        layout_direito.addWidget(self.input_usuario)
        layout_direito.addWidget(label_senha)
        layout_direito.addWidget(self.input_senha)
        layout_direito.addWidget(self.btn_entrar)
        layout_direito.addWidget(self.label_erro)

        layout_principal.addWidget(self.painel_esquerdo, 1)
        layout_principal.addWidget(self.painel_direito, 1)

    def fazer_login(self):
        usuario = self.input_usuario.text()
        senha = self.input_senha.text()

        if usuario == "" or senha == "":
            self.label_erro.setText("Preencher os campos.")
            return

        conexao = get_conexao()

        if conexao == None:
            self.label_erro.setText("Erro ao tentar se conectar ao banco.")
            return

        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id FROM usuario WHERE email = %s AND senha = %s",
            (usuario, senha)
        )
        resultado = cursor.fetchone()
        fechar_conexao(conexao, cursor)

        if resultado != None:
            self.label_erro.setStyleSheet("color: #27ae60; font-size: 12px; background: transparent;")
            self.label_erro.setText("Login realizado com sucesso!")

            from controllers.main_controller import MainController
            self.tela_principal = MainController()
            self.tela_principal.show()
            self.close()
        else:
            self.label_erro.setStyleSheet("color: #e74c3c; font-size: 12px; background: transparent;")
            self.label_erro.setText("Usuário ou senha inválidos.")