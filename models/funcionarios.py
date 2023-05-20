from cli.index import pausa, exibir_cabecalho
from time import sleep

from validation.index import data_valida


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
        print('ID:', registro[0])
        print('Nome:', registro[1])
        print('Data de nascimento:', registro[2])
        print('Salário:', registro[3])
        print('-----')
    pausa()

    cursor.close()


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

        salario = None
        while True:
            try:
                salario = float(input('\nSalário (0000.00): '))
                break
            except:
                print("[!] Salário inválido. Tente novamente")
        confirma = input('\nConfirma a inclusão [S/N]? ').upper()

        if confirma == 'S':
            comando = f'INSERT INTO funcionarios VALUES({id}, "{nome}", "{data_de_nascimento}", {salario})'
            print(comando)
            cursor = conexao.cursor()
            cursor.execute(comando)
            conexao.commit()
            cursor.close()


def alterar(conexao):
    id = exibir_cabecalho('alteração')
    if int(id) == 0:
        return
    resultado = verificar_registro_existe(conexao, id)
    if not resultado:
        print('\nID não existe!')
        sleep(2)
    else:
        mostrar_registro(resultado)

        # Corrigir duplicação de código desnecessária

        nome = input('\nNome: ')
        data_de_nascimento = None
        while True:
            data_de_nascimento = input('\nData de nascimento (AAAA-MM-DD): ')
            if data_valida(data_de_nascimento):
                break
            print("[!] Data inválida. Verifique a formatação")

        salario = None
        while True:
            try:
                salario = float(input('\nSalário (0000.00): '))
                break
            except:
                print("[!] Salário inválido. Tente novamente")

        confirma = input('\nConfirma a alteração [S/N]? ').upper()
        if confirma == 'S':
            cursor = conexao.cursor()
            cursor.execute('UPDATE funcionarios SET nome=?, data_de_nascimento=?, salario=? WHERE id=?',
                           (nome, data_de_nascimento, salario, id))
            conexao.commit()
            cursor.close()


def excluir(conexao):
    if tabela_vazia(conexao):
        print('\n*** TABELA VAZIA ***')
        pausa()
        return
    id = exibir_cabecalho('exclusão')
    if int(id) == 0:
        return
    resultado = verificar_registro_existe(conexao, id)
    if not resultado:
        print('\nID não existe!')
        sleep(2)
    else:
        mostrar_registro(resultado)
        confirma = input('\nConfirma a exclusão [S/N]? ').upper()

        if confirma == 'S':
            cursor = conexao.cursor()
            cursor.execute('DELETE FROM funcionarios WHERE id=?', (id,))
            conexao.commit()
            cursor.close()
