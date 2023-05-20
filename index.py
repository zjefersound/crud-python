import sqlite3
from sqlite3 import Error, OperationalError
import os
from time import sleep

from models.funcionarios import criar_tabela, incluir, alterar, excluir, listar


def conectarBanco():
    conexao = None
    diretorio = 'database'
    banco = 'unoesc.db'
    print(f'SQLite versão: {sqlite3.version}\n')
    path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(path, diretorio, banco)
    print(f'Banco de dados: [{full_path}]\n')
    if not os.path.isfile(full_path):
        continuar = input(
            f'Banco de dados não encontrado, deseja criá-lo? \nSe sim, então o banco de dados será criado no diretório onde o programa está sendo executado[{os.getcwd()}]! [S/N]: ')
        if continuar.upper() != 'S':
            raise sqlite3.DatabaseError('Banco de dados não selecionado!')
    conexao = sqlite3.connect(full_path)
    print('BD aberto com sucesso!')
    return conexao


def menu(conexao):
    opcao = 1
    while opcao != 5:
        print('---------------------------')
        print('PORTAL DO RH > FUNCIONÁRIOS')
        print('---------------------------')
        print('1. Incluir dados')
        print('2. Alterar dados')
        print('3. Excluir dados')
        print('4. Listar dados')
        print('5. Sair')

        try:
            opcao = int(input('\nOpção [1-5]: '))
        except ValueError:
            opcao = 0
        if opcao == 1:
            incluir(conexao)
        elif opcao == 2:
            alterar(conexao)
        elif opcao == 3:
            excluir(conexao)
        elif opcao == 4:
            listar(conexao)
        elif opcao != 5:
            print('Opção inválida, tente novamente')
            sleep(2)
        print()
    return opcao


if __name__ == '__main__':
    conn = None
    while True:
        try:
            conn = conectarBanco()
            criar_tabela(conn)
            if menu(conn) == 5:
                break
        except OperationalError as e:
            print('Erro operacional:', e)
        except sqlite3.DatabaseError as e:
            print('Erro database:', e)
            raise SystemExit()
        except Error as e:
            print('Erro SQLite3:', e)
            raise SystemExit()
        except Exception as e:
            print('Erro durante a execução do sistema!')
            print(e)
        finally:
            if conn:
                print('Liberando a conexão...')
                conn.commit()
                conn.close()
                print('Encerrando...')
