import cx_Oracle

def conectar():
    try:
        conn = cx_Oracle.connect("rm561090", "fiap25", "oracle.fiap.com.br:1521/orcl")
        return conn
    except cx_Oracle.DatabaseError as e:
        print("Erro ao conectar ao banco:", e)
        return None

def inserir_usuario():
    conn = conectar()
    if conn:
        try:
            id_usuario = int(input("Digite o ID do usuário (único): ").strip())
            cpf = input("Digite o CPF do usuário: ").strip()
            senha = input("Digite a senha do usuário: ").strip()
            telefone = input("Digite o telefone do usuário: ").strip()

            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO SF_USUARIO (ID_USUARIO, CPF, SENHA, TELEFONE)
                VALUES (:1, :2, :3, :4)
            """, (id_usuario, cpf, senha, telefone))
            conn.commit()
            print("Usuário inserido com sucesso!")
        except Exception as e:
            print("Erro ao inserir:", e)
        finally:
            conn.close()

def listar_usuarios():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ID_USUARIO, CPF, SENHA, TELEFONE FROM SF_USUARIO")
            usuarios = cursor.fetchall()
            print("\n--- Lista de Usuários ---")
            for u in usuarios:
                print(f"ID: {u[0]} | CPF: {u[1]} | Senha: {u[2]} | Telefone: {u[3]}")
        except Exception as e:
            print("Erro ao listar:", e)
        finally:
            conn.close()

def menu():
    while True:
        print("\n===== Menu =====")
        print("1 - Inserir usuário")
        print("2 - Listar usuários")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()
        
        if opcao == "1":
            inserir_usuario()
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
