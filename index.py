import sqlite3
from sqlite3 import Error, OperationalError
import os
from time import sleep

from validation.index import data_valida

def exibir_cabecalho(mensagem):
    mensagem = f'Rotina de {mensagem} de dados'
    print('\n' + '-' * len(mensagem))
    print(mensagem)
    print('\n' + '-' * len(mensagem))
    id = input('ID (0 para voltar): ')
    return id


def mostrar_registro(registro):
    print('\n====================')
    print('Registro')
    print('--------')
    print('ID:', registro[0])
    print('Nome:', registro[1])
    print('Data de nascimento:', registro[2])
    print('Salário:', registro[3])
    print('====================')


def tabela_vazia(conexao):
    print(conexao)
    cursor = conexao.cursor()
    cursor.execute('SELECT count(*) FROM funcionarios')
    resultado = cursor.fetchall()
    cursor.close()
    return resultado[0][0] == 0


def verificar_registro_existe(conexao, id):
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM funcionarios WHERE id=?', (id,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado


def pausa():
    input('\nPressione <ENTER> para continuar')


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


def criar_tabela(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY,
            nome INTEGER,
            data_de_nascimento TEXT,
            salario REAL
        )
        """)
    conexao.commit()
    if cursor:
        cursor.close()


def listar(conexao):
    if tabela_vazia(conexao):
        print('\n*** TABELA VAZIA ***')
        pausa()
        return

    

    print('\n----------------------')
    print('Listagem dos Registros')
    print('----------------------\n')

    cursor = conexao.execute('SELECT * from funcionarios')
    registros = cursor.fetchall()

    for registro in registros:
        print('ID..:', registro[0])
        print('Nome:', registro[1])
        print('Data de nascimento:', registro[2])
        print('Salário:', registro[3])
        print('-----')
    pausa()

    cursor.close()

# add missing methods
def incluir(conexao):
    id = exibir_cabecalho('inclusão')
    if int(id) == 0:
        return  
    if verificar_registro_existe(conexao, id):
        print('\nID já existe!')
        sleep(2)
    else:
        nome = input('\nNome: ')
        data_de_nascimento = None
        while True:
            data_de_nascimento = input('\nData de nascimento (AAAA-MM-DD): ')
            if data_valida(data_de_nascimento):
                break
            print("[!] Data inválida. Verifique a formatação")
        salario = float(input('\nSalario: '))
        confirma = input('\nConfirma a inclusão [S/N]? ').upper()
        
        if confirma == 'S':
            comando = f'INSERT INTO funcionarios VALUES({id}, "{nome}", "{data_de_nascimento}", {salario})'
            print(comando)
            cursor = conexao.cursor()
            cursor.execute(comando)
            conexao.commit()
            cursor.close()


def alterar(conexao):
    print('alterar')

def excluir(conexao):
    print('excluir')

def menu(conexao):
    opcao = 1
    while opcao != 5:
        print('--------------')
        print('MENU DE OPÇÕES')
        print('--------------')
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
            # Não mostra o traceback
            raise SystemExit()
        except Error as e:
            print('Erro SQLite3:', e)
            # Não mostra o traceback
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
