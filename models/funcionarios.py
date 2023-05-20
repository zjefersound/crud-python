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