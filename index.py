import sqlite3
from sqlite3 import Error, OperationalError
from time import sleep
from database.db import conectarBanco

from models import funcionarios

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
            funcionarios.incluir(conexao)
        elif opcao == 2:
            funcionarios.alterar(conexao)
        elif opcao == 3:
            funcionarios.excluir(conexao)
        elif opcao == 4:
            funcionarios.listar(conexao)
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
            funcionarios.criar_tabela(conn)
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
