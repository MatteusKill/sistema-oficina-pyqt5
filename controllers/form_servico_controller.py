from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from views.form_servico import Ui_Dialog
from database.conexao import get_conexao
from database.conexao import fechar_conexao


class FormServicoController(QDialog):

    def __init__(self, parent=None, id_servico=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.id_servico = id_servico

        if self.id_servico != None:
            self.setWindowTitle("Editar Serviço")
            self.carregar_dados()
        else:
            self.setWindowTitle("Novo Serviço")

        self.ui.btn_salvar.clicked.connect(self.salvar)
        self.ui.btn_cancelar.clicked.connect(self.close)

    def carregar_dados(self):
        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()
        cursor.execute(
            "SELECT nome, descricao, preco FROM servico WHERE id = %s",
            (self.id_servico,)
        )
        servico = cursor.fetchone()
        fechar_conexao(conexao, cursor)

        if servico != None:
            self.ui.input_nome.setText(str(servico[0]))
            self.ui.input_descricao.setText(str(servico[1]))
            self.ui.input_preco.setText(str(servico[2]))

    def salvar(self):
        nome = self.ui.input_nome.text()
        descricao = self.ui.input_descricao.text()
        preco = self.ui.input_preco.text()

        if nome == "":
            QMessageBox.warning(self, "Aviso", "O campo Nome é obrigatório.")
            return

        if preco == "":
            QMessageBox.warning(self, "Aviso", "O campo Preço é obrigatório.")
            return

        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()

        if self.id_servico == None:
            cursor.execute(
                "INSERT INTO servico (nome, descricao, preco) VALUES (%s, %s, %s)",
                (nome, descricao, preco)
            )
        else:
            cursor.execute(
                "UPDATE servico SET nome = %s, descricao = %s, preco = %s WHERE id = %s",
                (nome, descricao, preco, self.id_servico)
            )

        conexao.commit()
        fechar_conexao(conexao, cursor)

        QMessageBox.information(self, "Sucesso", "Serviço salvo com sucesso!")

        if self.parent() != None:
            self.parent().carregar_servicos()

        self.close()