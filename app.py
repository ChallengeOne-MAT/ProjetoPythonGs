import cx_Oracle
import json

# Conexão com o banco Oracle
def conectar():
    try:
        conn = cx_Oracle.connect("usuario", "senha", "host:porta/sid")
        return conn
    except cx_Oracle.Error as e:
        print("Erro ao conectar ao banco:", e)
        return None

# Inserir usuário
def inserir_usuario(conn):
    try:
        nome = input("Nome: ")
        email = input("Email: ")
        telefone = input("Telefone: ")
        endereco = input("Endereço: ")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO SF_Usuario (id_usuario, nome, email, telefone, endereco)
            VALUES (SF_USUARIO_SEQ.NEXTVAL, :1, :2, :3, :4)
        """, (nome, email, telefone, endereco))
        conn.commit()
        print("Usuário inserido com sucesso!")
    except Exception as e:
        print("Erro ao inserir usuário:", e)

# Listar usuários
def listar_usuarios(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SF_Usuario")
        for row in cursor.fetchall():
            print(row)
    except Exception as e:
        print("Erro ao listar usuários:", e)

# Atualizar usuário
def atualizar_usuario(conn):
    try:
        id_usuario = input("ID do usuário a atualizar: ")
        novo_nome = input("Novo nome: ")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE SF_Usuario SET nome = :1 WHERE id_usuario = :2
        """, (novo_nome, id_usuario))
        conn.commit()
        print("Usuário atualizado!")
    except Exception as e:
        print("Erro ao atualizar:", e)

# Excluir usuário
def excluir_usuario(conn):
    try:
        id_usuario = input("ID do usuário a excluir: ")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM SF_Usuario WHERE id_usuario = :1", (id_usuario,))
        conn.commit()
        print("Usuário excluído.")
    except Exception as e:
        print("Erro ao excluir:", e)

# Consulta com filtro e exportação JSON
def exportar_ocorrencias_por_status(conn):
    try:
        status = input("Status da ocorrência (pendente, em andamento, concluída): ")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SF_Ocorrencia WHERE status = :1", (status,))
        rows = cursor.fetchall()
        colunas = [col[0] for col in cursor.description]
        resultados = [dict(zip(colunas, row)) for row in rows]
        with open(f"ocorrencias_{status}.json", "w", encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=4)
        print("Exportado com sucesso!")
    except Exception as e:
        print("Erro ao exportar:", e)

def exportar_autoridades_por_especialidade(conn):
    try:
        especialidade = input("Especialidade da autoridade: ")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SF_Autoridade WHERE especialidade = :1", (especialidade,))
        rows = cursor.fetchall()
        colunas = [col[0] for col in cursor.description]
        resultados = [dict(zip(colunas, row)) for row in rows]
        with open("autoridades.json", "w", encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=4)
        print("Exportado com sucesso!")
    except Exception as e:
        print("Erro:", e)

def exportar_mensagens_por_remetente(conn):
    try:
        remetente = input("Remetente: ")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SF_Mensagem WHERE remetente = :1", (remetente,))
        rows = cursor.fetchall()
        colunas = [col[0] for col in cursor.description]
        resultados = [dict(zip(colunas, row)) for row in rows]
        with open("mensagens.json", "w", encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=4)
        print("Exportado com sucesso!")
    except Exception as e:
        print("Erro:", e)

# Menu principal
def menu():
    conn = conectar()
    if conn is None:
        return

    while True:
        print("\n--- MENU ---")
        print("1. Inserir usuário")
        print("2. Listar usuários")
        print("3. Atualizar usuário")
        print("4. Excluir usuário")
        print("5. Exportar ocorrências por status (JSON)")
        print("6. Exportar autoridades por especialidade (JSON)")
        print("7. Exportar mensagens por remetente (JSON)")
        print("0. Sair")
        
        opcao = input("Escolha: ")

        if opcao == '1':
            inserir_usuario(conn)
        elif opcao == '2':
            listar_usuarios(conn)
        elif opcao == '3':
            atualizar_usuario(conn)
        elif opcao == '4':
            excluir_usuario(conn)
        elif opcao == '5':
            exportar_ocorrencias_por_status(conn)
        elif opcao == '6':
            exportar_autoridades_por_especialidade(conn)
        elif opcao == '7':
            exportar_mensagens_por_remetente(conn)
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

    conn.close()

# Executar o programa
if __name__ == "__main__":
    menu()
