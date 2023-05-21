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


def tabela_vazia(conexao):
    cursor = conexao.cursor()
    cursor.execute('SELECT count(*) FROM funcionarios')
    resultado = cursor.fetchall()
    cursor.close()
    return resultado[0][0] == 0


def buscar_todos(conexao):
    cursor = conexao.execute('SELECT * from funcionarios')
    registros = cursor.fetchall()
    cursor.close()
    return registros


def buscar_por_id(conexao, id):
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM funcionarios WHERE id=?', (id,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado


def buscar_por_nome(conexao, nome):
    cursor = conexao.cursor()
    comando = f'SELECT * FROM funcionarios WHERE nome LIKE "%{nome}%"'
    cursor.execute(comando)
    resultado = cursor.fetchall()
    cursor.close()
    return resultado


def buscar_por_data_de_nascimento(conexao, data_de_nascimento):
    cursor = conexao.cursor()
    cursor.execute(
        'SELECT * FROM funcionarios WHERE data_de_nascimento=?', (data_de_nascimento,))
    resultado = cursor.fetchall()
    cursor.close()
    return resultado


def buscar_por_salario(conexao, salario):
    cursor = conexao.cursor()
    cursor.execute(
        'SELECT * FROM funcionarios WHERE salario=?', (salario,))
    resultado = cursor.fetchall()
    cursor.close()
    return resultado


def inserir(conexao, id, nome, data_de_nascimento, salario):
    comando = f'INSERT INTO funcionarios VALUES({id}, "{nome}", "{data_de_nascimento}", {salario})'
    print(comando)
    cursor = conexao.cursor()
    cursor.execute(comando)
    conexao.commit()
    cursor.close()


def atualizar(conexao, id, nome, data_de_nascimento, salario):
    cursor = conexao.cursor()
    cursor.execute('UPDATE funcionarios SET nome=?, data_de_nascimento=?, salario=? WHERE id=?',
                   (nome, data_de_nascimento, salario, id))
    conexao.commit()
    cursor.close()


def deletar(conexao, id):
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM funcionarios WHERE id=?', (id,))
    conexao.commit()
    cursor.close()
