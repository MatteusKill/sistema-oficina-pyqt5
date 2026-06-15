from database.conexao import get_conexao, fechar_conexao

conexao = get_conexao()

if conexao:
    print("Conexão bem sucedida!")
    fechar_conexao(conexao)
else:
    print("Falha na conexão.")