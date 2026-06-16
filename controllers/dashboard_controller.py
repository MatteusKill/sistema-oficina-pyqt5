from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QAbstractItemView
from views.dashboard import Ui_Form
from database.conexao import get_conexao
from database.conexao import fechar_conexao


class DashboardController(QWidget):

    def __init__(self):
        super().__init__()

        # Carrega a interface do Qt Designer
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Configura a tabela
        self.ui.tabela_ultimas_os.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tabela_ultimas_os.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tabela_ultimas_os.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Carrega os dados do dashboard
        self.carregar_dados()

    def carregar_dados(self):
        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()

        # Conta total de clientes
        cursor.execute("SELECT COUNT(*) FROM cliente")
        total_clientes = cursor.fetchone()[0]

        # Conta total de carros
        cursor.execute("SELECT COUNT(*) FROM carro")
        total_carros = cursor.fetchone()[0]

        # Conta OS abertas
        cursor.execute("SELECT COUNT(*) FROM ordem_servico WHERE status = 'aberta'")
        total_os = cursor.fetchone()[0]

        # Conta serviços ativos
        cursor.execute("SELECT COUNT(*) FROM servico WHERE ativo = 1")
        total_servicos = cursor.fetchone()[0]

        fechar_conexao(conexao, cursor)

        # Atualiza os números nos cards
        self.ui.label_total_clientes.setText(str(total_clientes))
        self.ui.label_total_carros.setText(str(total_carros))
        self.ui.label_total_os.setText(str(total_os))
        self.ui.label_total_servicos.setText(str(total_servicos))

        # Carrega últimas 5 OS na tabela
        conexao = get_conexao()

        if conexao == None:
            return

        cursor = conexao.cursor()
        cursor.execute("""
            SELECT c.nome, ca.placa, os.status, os.valor_total
            FROM ordem_servico os
            JOIN cliente c ON c.id = os.cliente_id
            JOIN carro ca ON ca.id = os.carro_id
            ORDER BY os.criado_em DESC
            LIMIT 5
        """)
        ordens = cursor.fetchall()
        fechar_conexao(conexao, cursor)

        # Limpa e preenche a tabela
        self.ui.tabela_ultimas_os.setRowCount(0)

        for ordem in ordens:
            linha = self.ui.tabela_ultimas_os.rowCount()
            self.ui.tabela_ultimas_os.insertRow(linha)

            self.ui.tabela_ultimas_os.setItem(linha, 0, QTableWidgetItem(str(ordem[0])))
            self.ui.tabela_ultimas_os.setItem(linha, 1, QTableWidgetItem(str(ordem[1])))
            self.ui.tabela_ultimas_os.setItem(linha, 2, QTableWidgetItem(str(ordem[2])))
            self.ui.tabela_ultimas_os.setItem(linha, 3, QTableWidgetItem("R$ " + str(ordem[3])))