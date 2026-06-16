from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QAbstractItemView
from views.carros import Ui_Form
from database.conexao import get_conexao
from database.conexao import fechar_conexao


class CarrosController(QWidget):

    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.tabela_carros.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tabela_carros.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tabela_carros.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.carregar_carros()

        self.ui.btn_buscar.clicked.connect(self.buscar_carro)
        self.ui.btn_novo.clicked.connect(self.novo_carro)
        self.ui.btn_editar.clicked.connect(self.editar_carro)
        self.ui.btn_excluir.clicked.connect(self.excluir_carro)

    def carregar_carros(self):
        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()
        cursor.execute("SELECT id, placa, marca, modelo, ano FROM carro")
        carros = cursor.fetchall()
        fechar_conexao(conexao, cursor)

        self.ui.tabela_carros.setRowCount(0)

        for carro in carros:
            linha = self.ui.tabela_carros.rowCount()
            self.ui.tabela_carros.insertRow(linha)

            self.ui.tabela_carros.setItem(linha, 0, QTableWidgetItem(str(carro[0])))
            self.ui.tabela_carros.setItem(linha, 1, QTableWidgetItem(str(carro[1])))
            self.ui.tabela_carros.setItem(linha, 2, QTableWidgetItem(str(carro[2])))
            self.ui.tabela_carros.setItem(linha, 3, QTableWidgetItem(str(carro[3])))
            self.ui.tabela_carros.setItem(linha, 4, QTableWidgetItem(str(carro[4])))

    def buscar_carro(self):
        texto = self.ui.input_busca.text()

        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id, placa, marca, modelo, ano FROM carro WHERE placa LIKE %s OR modelo LIKE %s OR marca LIKE %s",
            ("%" + texto + "%", "%" + texto + "%", "%" + texto + "%")
        )
        carros = cursor.fetchall()
        fechar_conexao(conexao, cursor)

        self.ui.tabela_carros.setRowCount(0)

        for carro in carros:
            linha = self.ui.tabela_carros.rowCount()
            self.ui.tabela_carros.insertRow(linha)

            self.ui.tabela_carros.setItem(linha, 0, QTableWidgetItem(str(carro[0])))
            self.ui.tabela_carros.setItem(linha, 1, QTableWidgetItem(str(carro[1])))
            self.ui.tabela_carros.setItem(linha, 2, QTableWidgetItem(str(carro[2])))
            self.ui.tabela_carros.setItem(linha, 3, QTableWidgetItem(str(carro[3])))
            self.ui.tabela_carros.setItem(linha, 4, QTableWidgetItem(str(carro[4])))

    def novo_carro(self):
        from controllers.form_carro_controller import FormCarroController
        self.form = FormCarroController(self)
        self.form.show()

    def editar_carro(self):
        linha = self.ui.tabela_carros.currentRow()

        if linha == -1:
            QMessageBox.warning(self, "Aviso", "Selecione um carro para editar.")
            return

        id_carro = self.ui.tabela_carros.item(linha, 0).text()

        from controllers.form_carro_controller import FormCarroController
        self.form = FormCarroController(self, id_carro=id_carro)
        self.form.show()

    def excluir_carro(self):
        linha = self.ui.tabela_carros.currentRow()

        if linha == -1:
            QMessageBox.warning(self, "Aviso", "Selecione um carro para excluir.")
            return

        id_carro = self.ui.tabela_carros.item(linha, 0).text()
        placa_carro = self.ui.tabela_carros.item(linha, 1).text()

        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            "Deseja excluir o carro de placa " + placa_carro + "?",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            conexao = get_conexao()

            if conexao == None:
                return

            cursor = conexao.cursor()
            cursor.execute("DELETE FROM carro WHERE id = %s", (id_carro,))
            conexao.commit()
            fechar_conexao(conexao, cursor)

            self.carregar_carros()