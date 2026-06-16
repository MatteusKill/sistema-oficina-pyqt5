from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from views.form_os import Ui_Dialog
from database.conexao import get_conexao
from database.conexao import fechar_conexao


class FormOsController(QDialog):

    def __init__(self, parent=None, id_ordem=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.id_ordem = id_ordem

        self.carregar_clientes()
        self.carregar_carros()

        self.ui.combo_status.addItem("aberta")
        self.ui.combo_status.addItem("em_andamento")
        self.ui.combo_status.addItem("concluida")
        self.ui.combo_status.addItem("cancelada")

        if self.id_ordem != None:
            self.setWindowTitle("Editar Ordem de Serviço")
            self.carregar_dados()
        else:
            self.setWindowTitle("Nova Ordem de Serviço")

        self.ui.btn_salvar.clicked.connect(self.salvar)
        self.ui.btn_cancelar.clicked.connect(self.close)

    def carregar_clientes(self):
        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome FROM cliente")
        clientes = cursor.fetchall()
        fechar_conexao(conexao, cursor)

        self.ids_clientes = []

        for cliente in clientes:
            self.ui.combo_cliente.addItem(cliente[1])
            self.ids_clientes.append(cliente[0])

    def carregar_carros(self):
        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()
        cursor.execute("SELECT id, placa, modelo FROM carro")
        carros = cursor.fetchall()
        fechar_conexao(conexao, cursor)

        self.ids_carros = []

        for carro in carros:
            self.ui.combo_carro.addItem(carro[1] + " - " + carro[2])
            self.ids_carros.append(carro[0])

    def carregar_dados(self):
        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()
        cursor.execute(
            "SELECT cliente_id, carro_id, status, observacoes FROM ordem_servico WHERE id = %s",
            (self.id_ordem,)
        )
        ordem = cursor.fetchone()
        fechar_conexao(conexao, cursor)

        if ordem != None:
            if ordem[0] in self.ids_clientes:
                index_cliente = self.ids_clientes.index(ordem[0])
                self.ui.combo_cliente.setCurrentIndex(index_cliente)

            if ordem[1] in self.ids_carros:
                index_carro = self.ids_carros.index(ordem[1])
                self.ui.combo_carro.setCurrentIndex(index_carro)

            status_opcoes = ["aberta", "em_andamento", "concluida", "cancelada"]
            if ordem[2] in status_opcoes:
                self.ui.combo_status.setCurrentIndex(status_opcoes.index(ordem[2]))

            self.ui.input_observacoes.setText(str(ordem[3]))

    def salvar(self):
        if len(self.ids_clientes) == 0:
            QMessageBox.warning(self, "Aviso", "Cadastre um cliente antes de criar uma OS.")
            return

        if len(self.ids_carros) == 0:
            QMessageBox.warning(self, "Aviso", "Cadastre um carro antes de criar uma OS.")
            return

        index_cliente = self.ui.combo_cliente.currentIndex()
        index_carro = self.ui.combo_carro.currentIndex()
        status = self.ui.combo_status.currentText()
        observacoes = self.ui.input_observacoes.text()

        cliente_id = self.ids_clientes[index_cliente]
        carro_id = self.ids_carros[index_carro]

        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()

        if self.id_ordem == None:
            cursor.execute(
                "INSERT INTO ordem_servico (cliente_id, carro_id, status, observacoes) VALUES (%s, %s, %s, %s)",
                (cliente_id, carro_id, status, observacoes)
            )
        else:
            cursor.execute(
                "UPDATE ordem_servico SET cliente_id = %s, carro_id = %s, status = %s, observacoes = %s WHERE id = %s",
                (cliente_id, carro_id, status, observacoes, self.id_ordem)
            )

        conexao.commit()
        fechar_conexao(conexao, cursor)

        QMessageBox.information(self, "Sucesso", "Ordem de Serviço salva com sucesso!")

        if self.parent() != None:
            self.parent().carregar_ordens()

        self.close()