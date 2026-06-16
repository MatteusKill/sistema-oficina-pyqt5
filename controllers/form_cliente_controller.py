from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from views.form_cliente import Ui_Dialog
from database.conexao import get_conexao
from database.conexao import fechar_conexao


class FormClienteController(QDialog):

    def __init__(self, parent=None, id_cliente=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.id_cliente = id_cliente

        if self.id_cliente != None:
            self.setWindowTitle("Editar Cliente")
            self.carregar_dados()
        else:
            self.setWindowTitle("Novo Cliente")

        self.ui.btn_salvar.clicked.connect(self.salvar)
        self.ui.btn_cancelar.clicked.connect(self.close)

    def carregar_dados(self):
        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()
        cursor.execute(
            "SELECT nome, cpf, telefone, email, endereco FROM cliente WHERE id = %s",
            (self.id_cliente,)
        )
        cliente = cursor.fetchone()
        fechar_conexao(conexao, cursor)

        if cliente != None:
            self.ui.input_nome.setText(str(cliente[0]))
            self.ui.input_cpf.setText(str(cliente[1]))
            self.ui.input_telefone.setText(str(cliente[2]))
            self.ui.input_email.setText(str(cliente[3]))
            self.ui.input_endereco.setText(str(cliente[4]))

    def salvar(self):
        nome = self.ui.input_nome.text()
        cpf = self.ui.input_cpf.text()
        telefone = self.ui.input_telefone.text()
        email = self.ui.input_email.text()
        endereco = self.ui.input_endereco.text()

        if nome == "":
            QMessageBox.warning(self, "Aviso", "O campo Nome é obrigatório.")
            return

        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()

        if self.id_cliente == None:
            cursor.execute(
                "INSERT INTO cliente (nome, cpf, telefone, email, endereco) VALUES (%s, %s, %s, %s, %s)",
                (nome, cpf, telefone, email, endereco)
            )
        else:
            cursor.execute(
                "UPDATE cliente SET nome = %s, cpf = %s, telefone = %s, email = %s, endereco = %s WHERE id = %s",
                (nome, cpf, telefone, email, endereco, self.id_cliente)
            )

        conexao.commit()
        fechar_conexao(conexao, cursor)

        QMessageBox.information(self, "Sucesso", "Cliente salvo com sucesso!")

        if self.parent() != None:
            self.parent().carregar_clientes()

        self.close()