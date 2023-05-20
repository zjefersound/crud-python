from time import sleep
from utils.index import formatar_moeda
from validation.index import data_valida
from models import funcionarios


def exibir_cabecalho(mensagem):
    mensagem = f'Rotina de {mensagem} de dados'
    print('\n' + '-' * len(mensagem))
    print(mensagem)
    print('\n' + '-' * len(mensagem))
    id = input('ID (0 para voltar): ')
    return id


def pausa():
    input('\nPressione <ENTER> para continuar')


def mostrar_registro_conteudo(registro):
    print('ID:', registro[0])
    print('Nome:', registro[1])
    print('Data de nascimento:', registro[2])
    print('Salário:', formatar_moeda(registro[3]))


def mostrar_registro(registro):
    print('\n====================')
    print('Registro')
    print('--------')
    mostrar_registro_conteudo(registro)
    print('====================')


def listar(conexao):
    if funcionarios.tabela_vazia(conexao):
        print('\n*** TABELA VAZIA ***')
        pausa()
        return

    print('\n----------------------')
    print('Listagem dos Registros')
    print('----------------------\n')

    registros = funcionarios.buscar_todos(conexao)

    for registro in registros:
        mostrar_registro_conteudo(registro)
        print('-----')
    pausa()


def pesquisar_por_id(conexao):
    id = input('Pesquisar pelo ID: ')
    resultado = funcionarios.buscar_por_id(conexao, id)
    if not resultado:
        print('\nID não existe!')
        sleep(2)
    mostrar_registro(resultado)
    pausa()


def pesquisar_por_nome(conexao):
    nome = input('Pesquisar pelo nome: ')
    registros = funcionarios.buscar_por_nome(conexao, nome)
    print('\n----------------------')
    print('Listagem dos Registros')
    print('----------------------\n')
    for registro in registros:
        mostrar_registro_conteudo(registro)
        print('-----')
    pausa()


def pesquisar_por_data_de_nascimento(conexao):
    data_de_nascimento = input(
        'Pesquisar pela data de nascimento (AAAA-MM-DD): ')
    registros = funcionarios.buscar_por_data_de_nascimento(
        conexao, data_de_nascimento)
    print('\n----------------------')
    print('Listagem dos Registros')
    print('----------------------\n')
    for registro in registros:
        mostrar_registro_conteudo(registro)
        print('-----')
    pausa()


def pesquisar_por_salario(conexao):
    salario = input('Pesquisar por salário (0000.00): ')
    registros = funcionarios.buscar_por_salario(conexao, salario)
    print('\n----------------------')
    print('Listagem dos Registros')
    print('----------------------\n')
    for registro in registros:
        mostrar_registro_conteudo(registro)
        print('-----')
    pausa()


def pesquisar(conexao):
    if funcionarios.tabela_vazia(conexao):
        print('\n*** TABELA VAZIA ***')
        pausa()
        return
    opcao = 1
    while True:
        print('---------------------------')
        print('Pesquisar por')
        print('---------------------------')
        print('1. ID')
        print('2. Nome')
        print('3. Data de nascimento')
        print('4. Salario')

        try:
            opcao = int(input('\nOpção [1-4]: '))
        except ValueError:
            opcao = 0
        if opcao == 1:
            pesquisar_por_id(conexao)
            break
        elif opcao == 2:
            pesquisar_por_nome(conexao)
            break
        elif opcao == 3:
            pesquisar_por_data_de_nascimento(conexao)
            break
        elif opcao == 4:
            pesquisar_por_salario(conexao)
            break
        else:
            print('[!] Opção inválida, tente novamente')
            sleep(2)
        print()
    return opcao


def coletar_dados():
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
    return {"nome": nome, "data_de_nascimento": data_de_nascimento, "salario": salario}


def incluir(conexao):
    id = exibir_cabecalho('inclusão')
    if int(id) == 0:
        return
    if funcionarios.buscar_por_id(conexao, id):
        print('\nID já existe!')
        sleep(2)
    else:
        dados = coletar_dados()
        confirma = input('\nConfirma a inclusão [S/N]? ').upper()

        if confirma == 'S':
            funcionarios.inserir(conexao, id, dados['nome'],
                                 dados['data_de_nascimento'], dados['salario'])


def alterar(conexao):
    id = exibir_cabecalho('alteração')
    if int(id) == 0:
        return
    resultado = funcionarios.buscar_por_id(conexao, id)
    if not resultado:
        print('\nID não existe!')
        sleep(2)
    else:
        mostrar_registro(resultado)
        dados = coletar_dados()
        confirma = input('\nConfirma a alteração [S/N]? ').upper()
        if confirma == 'S':
            funcionarios.atualizar(conexao, id, dados['nome'],
                                   dados['data_de_nascimento'], dados['salario'])


def excluir(conexao):
    if funcionarios.tabela_vazia(conexao):
        print('\n*** TABELA VAZIA ***')
        pausa()
        return
    id = exibir_cabecalho('exclusão')
    if int(id) == 0:
        return
    resultado = funcionarios.buscar_por_id(conexao, id)
    if not resultado:
        print('\nID não existe!')
        sleep(2)
    else:
        mostrar_registro(resultado)
        confirma = input('\nConfirma a exclusão [S/N]? ').upper()

        if confirma == 'S':
            funcionarios.deletar(conexao, id)
