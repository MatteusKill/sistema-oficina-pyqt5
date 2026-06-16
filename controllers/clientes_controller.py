from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QHeaderView
from views.clientes import Ui_Form
from database.conexao import get_conexao
from database.conexao import fechar_conexao
from PyQt5.QtWidgets import QAbstractItemView


class ClientesController(QWidget):

    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.tabela_clientes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tabela_clientes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tabela_clientes.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.carregar_clientes()

        self.ui.btn_buscar.clicked.connect(self.buscar_cliente)
        self.ui.btn_novo.clicked.connect(self.novo_cliente)
        self.ui.btn_editar.clicked.connect(self.editar_cliente)
        self.ui.btn_excluir.clicked.connect(self.excluir_cliente)

    def carregar_clientes(self):
        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, cpf, telefone, email FROM cliente")
        clientes = cursor.fetchall()
        fechar_conexao(conexao, cursor)

        self.ui.tabela_clientes.setRowCount(0)

        for cliente in clientes:
            linha = self.ui.tabela_clientes.rowCount()
            self.ui.tabela_clientes.insertRow(linha)

            self.ui.tabela_clientes.setItem(linha, 0, QTableWidgetItem(str(cliente[0])))
            self.ui.tabela_clientes.setItem(linha, 1, QTableWidgetItem(str(cliente[1])))
            self.ui.tabela_clientes.setItem(linha, 2, QTableWidgetItem(str(cliente[2])))
            self.ui.tabela_clientes.setItem(linha, 3, QTableWidgetItem(str(cliente[3])))
            self.ui.tabela_clientes.setItem(linha, 4, QTableWidgetItem(str(cliente[4])))

    def buscar_cliente(self):
        texto = self.ui.input_busca.text()

        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id, nome, cpf, telefone, email FROM cliente WHERE nome LIKE %s OR cpf LIKE %s",
            ("%" + texto + "%", "%" + texto + "%")
        )
        clientes = cursor.fetchall()
        fechar_conexao(conexao, cursor)

        self.ui.tabela_clientes.setRowCount(0)

        for cliente in clientes:
            linha = self.ui.tabela_clientes.rowCount()
            self.ui.tabela_clientes.insertRow(linha)

            self.ui.tabela_clientes.setItem(linha, 0, QTableWidgetItem(str(cliente[0])))
            self.ui.tabela_clientes.setItem(linha, 1, QTableWidgetItem(str(cliente[1])))
            self.ui.tabela_clientes.setItem(linha, 2, QTableWidgetItem(str(cliente[2])))
            self.ui.tabela_clientes.setItem(linha, 3, QTableWidgetItem(str(cliente[3])))
            self.ui.tabela_clientes.setItem(linha, 4, QTableWidgetItem(str(cliente[4])))

    def novo_cliente(self):
        from controllers.form_cliente_controller import FormClienteController
        self.form = FormClienteController(self)
        self.form.show()

    def editar_cliente(self):
        linha = self.ui.tabela_clientes.currentRow()

        if linha == -1:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para editar.")
            return

        id_cliente = self.ui.tabela_clientes.item(linha, 0).text()

        from controllers.form_cliente_controller import FormClienteController
        self.form = FormClienteController(self, id_cliente=id_cliente)
        self.form.show()

    def excluir_cliente(self):
        linha = self.ui.tabela_clientes.currentRow()

        if linha == -1:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para excluir.")
            return

        id_cliente = self.ui.tabela_clientes.item(linha, 0).text()
        nome_cliente = self.ui.tabela_clientes.item(linha, 1).text()

        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            "Deseja excluir o cliente " + nome_cliente + "?",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            conexao = get_conexao()

            if conexao == None:
                return

            cursor = conexao.cursor()
            cursor.execute("DELETE FROM cliente WHERE id = %s", (id_cliente,))
            conexao.commit()
            fechar_conexao(conexao, cursor)

            self.carregar_clientes()