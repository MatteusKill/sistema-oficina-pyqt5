from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QAbstractItemView
from views.ordens import Ui_Form
from database.conexao import get_conexao
from database.conexao import fechar_conexao


class OrdensController(QWidget):

    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.tabela_ordens.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tabela_ordens.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tabela_ordens.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.carregar_ordens()

        self.ui.btn_buscar.clicked.connect(self.buscar_ordem)
        self.ui.btn_novo.clicked.connect(self.nova_ordem)
        self.ui.btn_editar.clicked.connect(self.editar_ordem)
        self.ui.btn_excluir.clicked.connect(self.excluir_ordem)

    def carregar_ordens(self):
        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()
        cursor.execute("""
            SELECT os.id, c.nome, ca.placa, os.status, os.valor_total
            FROM ordem_servico os
            JOIN cliente c ON c.id = os.cliente_id
            JOIN carro ca ON ca.id = os.carro_id
        """)
        ordens = cursor.fetchall()
        fechar_conexao(conexao, cursor)

        self.ui.tabela_ordens.setRowCount(0)

        for ordem in ordens:
            linha = self.ui.tabela_ordens.rowCount()
            self.ui.tabela_ordens.insertRow(linha)

            self.ui.tabela_ordens.setItem(linha, 0, QTableWidgetItem(str(ordem[0])))
            self.ui.tabela_ordens.setItem(linha, 1, QTableWidgetItem(str(ordem[1])))
            self.ui.tabela_ordens.setItem(linha, 2, QTableWidgetItem(str(ordem[2])))
            self.ui.tabela_ordens.setItem(linha, 3, QTableWidgetItem(str(ordem[3])))
            self.ui.tabela_ordens.setItem(linha, 4, QTableWidgetItem("R$ " + str(ordem[4])))

    def buscar_ordem(self):
        texto = self.ui.input_busca.text()

        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()
        cursor.execute("""
            SELECT os.id, c.nome, ca.placa, os.status, os.valor_total
            FROM ordem_servico os
            JOIN cliente c ON c.id = os.cliente_id
            JOIN carro ca ON ca.id = os.carro_id
            WHERE c.nome LIKE %s OR ca.placa LIKE %s OR os.status LIKE %s
        """, ("%" + texto + "%", "%" + texto + "%", "%" + texto + "%"))
        ordens = cursor.fetchall()
        fechar_conexao(conexao, cursor)

        self.ui.tabela_ordens.setRowCount(0)

        for ordem in ordens:
            linha = self.ui.tabela_ordens.rowCount()
            self.ui.tabela_ordens.insertRow(linha)

            self.ui.tabela_ordens.setItem(linha, 0, QTableWidgetItem(str(ordem[0])))
            self.ui.tabela_ordens.setItem(linha, 1, QTableWidgetItem(str(ordem[1])))
            self.ui.tabela_ordens.setItem(linha, 2, QTableWidgetItem(str(ordem[2])))
            self.ui.tabela_ordens.setItem(linha, 3, QTableWidgetItem(str(ordem[3])))
            self.ui.tabela_ordens.setItem(linha, 4, QTableWidgetItem("R$ " + str(ordem[4])))

    def nova_ordem(self):
        from controllers.form_os_controller import FormOsController
        self.form = FormOsController(self)
        self.form.show()

    def editar_ordem(self):
        linha = self.ui.tabela_ordens.currentRow()

        if linha == -1:
            QMessageBox.warning(self, "Aviso", "Selecione uma ordem para editar.")
            return

        id_ordem = self.ui.tabela_ordens.item(linha, 0).text()

        from controllers.form_os_controller import FormOsController
        self.form = FormOsController(self, id_ordem=id_ordem)
        self.form.show()

    def excluir_ordem(self):
        linha = self.ui.tabela_ordens.currentRow()

        if linha == -1:
            QMessageBox.warning(self, "Aviso", "Selecione uma ordem para excluir.")
            return

        id_ordem = self.ui.tabela_ordens.item(linha, 0).text()
        cliente_ordem = self.ui.tabela_ordens.item(linha, 1).text()

        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            "Deseja excluir a OS do cliente " + cliente_ordem + "?",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            conexao = get_conexao()

            if conexao == None:
                return

            cursor = conexao.cursor()
            cursor.execute("DELETE FROM ordem_servico WHERE id = %s", (id_ordem,))
            conexao.commit()
            fechar_conexao(conexao, cursor)

            self.carregar_ordens()