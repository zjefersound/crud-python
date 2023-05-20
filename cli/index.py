def exibir_cabecalho(mensagem):
    mensagem = f'Rotina de {mensagem} de dados'
    print('\n' + '-' * len(mensagem))
    print(mensagem)
    print('\n' + '-' * len(mensagem))
    id = input('ID (0 para voltar): ')
    return id

def pausa():
    input('\nPressione <ENTER> para continuar')