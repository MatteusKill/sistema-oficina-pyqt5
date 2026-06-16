from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from views.form_carro import Ui_Dialog
from database.conexao import get_conexao
from database.conexao import fechar_conexao


class FormCarroController(QDialog):

    def __init__(self, parent=None, id_carro=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.id_carro = id_carro

        if self.id_carro != None:
            self.setWindowTitle("Editar Carro")
            self.carregar_dados()
        else:
            self.setWindowTitle("Novo Carro")

        self.ui.btn_salvar.clicked.connect(self.salvar)
        self.ui.btn_cancelar.clicked.connect(self.close)

    def carregar_dados(self):
        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()
        cursor.execute(
            "SELECT placa, marca, modelo, ano, cor FROM carro WHERE id = %s",
            (self.id_carro,)
        )
        carro = cursor.fetchone()
        fechar_conexao(conexao, cursor)

        if carro != None:
            self.ui.input_placa.setText(str(carro[0]))
            self.ui.input_marca.setText(str(carro[1]))
            self.ui.input_modelo.setText(str(carro[2]))
            self.ui.input_ano.setText(str(carro[3]))
            self.ui.input_cor.setText(str(carro[4]))

    def salvar(self):
        placa = self.ui.input_placa.text()
        marca = self.ui.input_marca.text()
        modelo = self.ui.input_modelo.text()
        ano = self.ui.input_ano.text()
        cor = self.ui.input_cor.text()

        if placa == "":
            QMessageBox.warning(self, "Aviso", "O campo Placa é obrigatório.")
            return

        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()

        if self.id_carro == None:
            cursor.execute(
                "INSERT INTO carro (placa, marca, modelo, ano, cor) VALUES (%s, %s, %s, %s, %s)",
                (placa, marca, modelo, ano, cor)
            )
        else:
            cursor.execute(
                "UPDATE carro SET placa = %s, marca = %s, modelo = %s, ano = %s, cor = %s WHERE id = %s",
                (placa, marca, modelo, ano, cor, self.id_carro)
            )

        conexao.commit()
        fechar_conexao(conexao, cursor)

        QMessageBox.information(self, "Sucesso", "Carro salvo com sucesso!")

        if self.parent() != None:
            self.parent().carregar_carros()

        self.close()