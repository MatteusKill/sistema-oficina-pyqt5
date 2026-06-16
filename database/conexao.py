import mysql.connector

def get_conexao():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="meu_usuario",
            password="123",
            database="oficina_estacio"
        )
        return conexao
    except Exception as erro:
        print("Erro ao conectar:", erro)
        return None

def fechar_conexao(conexao, cursor=None):
    if cursor != None:
        cursor.close()
    if conexao != None:
        if conexao.is_connected():
            conexao.close()