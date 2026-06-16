from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QAbstractItemView
from views.servicos import Ui_Form
from database.conexao import get_conexao
from database.conexao import fechar_conexao


class ServicosController(QWidget):

    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.tabela_servicos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tabela_servicos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tabela_servicos.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.carregar_servicos()

        self.ui.btn_buscar.clicked.connect(self.buscar_servico)
        self.ui.btn_novo.clicked.connect(self.novo_servico)
        self.ui.btn_editar.clicked.connect(self.editar_servico)
        self.ui.btn_excluir.clicked.connect(self.excluir_servico)

    def carregar_servicos(self):
        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, preco, ativo FROM servico")
        servicos = cursor.fetchall()
        fechar_conexao(conexao, cursor)

        self.ui.tabela_servicos.setRowCount(0)

        for servico in servicos:
            linha = self.ui.tabela_servicos.rowCount()
            self.ui.tabela_servicos.insertRow(linha)

            self.ui.tabela_servicos.setItem(linha, 0, QTableWidgetItem(str(servico[0])))
            self.ui.tabela_servicos.setItem(linha, 1, QTableWidgetItem(str(servico[1])))
            self.ui.tabela_servicos.setItem(linha, 2, QTableWidgetItem("R$ " + str(servico[2])))

            if servico[3] == 1:
                status = "Ativo"
            else:
                status = "Inativo"

            self.ui.tabela_servicos.setItem(linha, 3, QTableWidgetItem(status))

    def buscar_servico(self):
        texto = self.ui.input_busca.text()

        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id, nome, preco, ativo FROM servico WHERE nome LIKE %s",
            ("%" + texto + "%",)
        )
        servicos = cursor.fetchall()
        fechar_conexao(conexao, cursor)

        self.ui.tabela_servicos.setRowCount(0)

        for servico in servicos:
            linha = self.ui.tabela_servicos.rowCount()
            self.ui.tabela_servicos.insertRow(linha)

            self.ui.tabela_servicos.setItem(linha, 0, QTableWidgetItem(str(servico[0])))
            self.ui.tabela_servicos.setItem(linha, 1, QTableWidgetItem(str(servico[1])))
            self.ui.tabela_servicos.setItem(linha, 2, QTableWidgetItem("R$ " + str(servico[2])))

            if servico[3] == 1:
                status = "Ativo"
            else:
                status = "Inativo"

            self.ui.tabela_servicos.setItem(linha, 3, QTableWidgetItem(status))

    def novo_servico(self):
        from controllers.form_servico_controller import FormServicoController
        self.form = FormServicoController(self)
        self.form.show()

    def editar_servico(self):
        linha = self.ui.tabela_servicos.currentRow()

        if linha == -1:
            QMessageBox.warning(self, "Aviso", "Selecione um serviço para editar.")
            return

        id_servico = self.ui.tabela_servicos.item(linha, 0).text()

        from controllers.form_servico_controller import FormServicoController
        self.form = FormServicoController(self, id_servico=id_servico)
        self.form.show()

    def excluir_servico(self):
        linha = self.ui.tabela_servicos.currentRow()

        if linha == -1:
            QMessageBox.warning(self, "Aviso", "Selecione um serviço para excluir.")
            return

        id_servico = self.ui.tabela_servicos.item(linha, 0).text()
        nome_servico = self.ui.tabela_servicos.item(linha, 1).text()

        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            "Deseja excluir o serviço " + nome_servico + "?",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            conexao = get_conexao()

            if conexao == None:
                return

            cursor = conexao.cursor()
            cursor.execute("DELETE FROM servico WHERE id = %s", (id_servico,))
            conexao.commit()
            fechar_conexao(conexao, cursor)

            self.carregar_servicos()