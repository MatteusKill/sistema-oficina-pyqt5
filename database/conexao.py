import mysql.connector
from mysql.connector import Error

def get_conexao():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="meu_usuario",        # troca se criou outro usuário
            password="123",        # troca pela sua senha
            database="oficina_estacio"
        )
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None


def fechar_conexao(conexao, cursor=None):
    if cursor:
        cursor.close()
    if conexao and conexao.is_connected():
        conexao.close()