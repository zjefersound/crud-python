import sqlite3
import os

def conectarBanco():
    conexao = None
    banco = 'unoesc.db'
    print(f'SQLite versão: {sqlite3.version}\n')
    path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(path, banco)
    print(f'Banco de dados: [{full_path}]\n')
    if not os.path.isfile(full_path):
        continuar = input(
            f'Banco de dados não encontrado, deseja criá-lo? \nSe sim, então o banco de dados será criado no diretório onde o programa está sendo executado[{os.getcwd()}]! [S/N]: ')
        if continuar.upper() != 'S':
            raise sqlite3.DatabaseError('Banco de dados não selecionado!')
    conexao = sqlite3.connect(full_path)
    print('BD aberto com sucesso!')
    return conexao