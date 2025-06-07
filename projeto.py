import cx_Oracle
import json
from datetime import datetime
import os

# Constantes para o admin
ADMIN_CPF = "00000000000"      # CPF único do admin
ADMIN_SENHA = "admin123"       # Senha única do admin
ARQUIVO_OCORRENCIAS = "ocorrencias_sos.json"  # Arquivo onde os SOS serão salvos


def conectar():
    try:
        conn = cx_Oracle.connect("rm561090", "fiap25", "oracle.fiap.com.br:1521/orcl")
        return conn
    except cx_Oracle.DatabaseError as e:
        print("Erro ao conectar ao banco:", e)
        return None

def deseja_voltar():
    while True:
        opcao = input("\nDeseja voltar para o menu principal? (S/N): ").strip().upper()
        if opcao == "S":
            return True
        elif opcao == "N":
            return False
        else:
            print("Opção inválida. Digite S ou N.")

def inserir_usuario():
    while True:
        conn = conectar()
        if conn:
            try:
                id_usuario = input("Digite o ID do usuário (único): ").strip()
                cpf = input("Digite o CPF do usuário: ").strip()
                senha = input("Digite a senha do usuário: ").strip()
                telefone = input("Digite o telefone do usuário: ").strip()

                if not id_usuario or not cpf or not senha or not telefone:
                    print("Todos os campos são obrigatórios.")
                    continue

                # Impede que se cadastre o admin via essa função
                if cpf == ADMIN_CPF:
                    print("CPF reservado para o administrador. Não pode ser usado.")
                    continue

                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO SF_USUARIO (ID_USUARIO, CPF, SENHA, TELEFONE)
                    VALUES (:1, :2, :3, :4)
                """, (int(id_usuario), cpf, senha, telefone))
                conn.commit()
                print("Usuário inserido com sucesso!")
            except Exception as e:
                print("Erro ao inserir:", e)
            finally:
                conn.close()
        if deseja_voltar():
            break

def listar_usuarios():
    while True:
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
        if deseja_voltar():
            break

def buscar_usuario_por_cpf():
    while True:
        conn = conectar()
        if conn:
            try:
                cpf = input("Digite o CPF para buscar: ").strip()
                cursor = conn.cursor()
                cursor.execute("SELECT ID_USUARIO, CPF, SENHA, TELEFONE FROM SF_USUARIO WHERE CPF = :1", (cpf,))
                usuario = cursor.fetchone()
                if usuario:
                    print(f"ID: {usuario[0]} | CPF: {usuario[1]} | Senha: {usuario[2]} | Telefone: {usuario[3]}")
                else:
                    print("Usuário não encontrado.")
            except Exception as e:
                print("Erro ao buscar:", e)
            finally:
                conn.close()
        if deseja_voltar():
            break

def atualizar_usuario():
    while True:
        conn = conectar()
        if conn:
            try:
                id_usuario = input("Digite o ID do usuário para atualizar: ").strip()
                novo_cpf = input("Novo CPF: ").strip()
                nova_senha = input("Nova senha: ").strip()
                novo_telefone = input("Novo telefone: ").strip()

                # Impede atualizar um usuário para ter o CPF admin
                if novo_cpf == ADMIN_CPF:
                    print("CPF reservado para o administrador. Não pode ser usado.")
                    continue

                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE SF_USUARIO
                    SET CPF = :1, SENHA = :2, TELEFONE = :3
                    WHERE ID_USUARIO = :4
                """, (novo_cpf, nova_senha, novo_telefone, int(id_usuario)))
                conn.commit()
                print("Usuário atualizado com sucesso.")
            except Exception as e:
                print("Erro ao atualizar:", e)
            finally:
                conn.close()
        if deseja_voltar():
            break

def deletar_usuario():
    while True:
        conn = conectar()
        if conn:
            try:
                id_usuario = input("Digite o ID do usuário para deletar: ").strip()
                cursor = conn.cursor()

                # Não permitir deletar o admin (se por acaso estiver no banco)
                cursor.execute("SELECT CPF FROM SF_USUARIO WHERE ID_USUARIO = :1", (int(id_usuario),))
                cpf_usuario = cursor.fetchone()
                if cpf_usuario and cpf_usuario[0] == ADMIN_CPF:
                    print("Não é permitido deletar o administrador.")
                    continue

                cursor.execute("DELETE FROM SF_USUARIO WHERE ID_USUARIO = :1", (int(id_usuario),))
                conn.commit()
                print("Usuário deletado com sucesso.")
            except Exception as e:
                print("Erro ao deletar:", e)
            finally:
                conn.close()
        if deseja_voltar():
            break

# ----- Função 6 modificada: Botão SOS (armazena em JSON) -----
def exportar_ocorrencias_por_status():
    autoridades = [
        { "id": 1, "nome": "Bombeiros", "telefone": "193", "eventos": ["Incêndio", "Resgate", "Alagamento"] },
        { "id": 2, "nome": "Polícia", "telefone": "190", "eventos": ["Assalto", "Violência", "Perturbação"] },
        { "id": 3, "nome": "Controle de Zoonoses", "telefone": "0800-000-000", "eventos": ["Animal perdido", "Animal agressivo"] },
        { "id": 4, "nome": "SAMU", "telefone": "192", "eventos": ["Desmaio", "Acidente", "Dor intensa"] },
    ]

    print("\n*** Botão SOS acionado! Você precisa passar pela autoridade responsável. ***")
    print("Autoridades disponíveis:")
    for auth in autoridades:
        print(f"{auth['id']} - {auth['nome']} (Telefone: {auth['telefone']}) - Eventos: {', '.join(auth['eventos'])}")

    while True:
        try:
            id_auth = int(input("Escolha a autoridade pelo ID: ").strip())
            autoridade = next((a for a in autoridades if a["id"] == id_auth), None)
            if autoridade is None:
                print("ID inválido, tente novamente.")
                continue
            break
        except ValueError:
            print("Digite um número válido para o ID.")

    print(f"\nVocê escolheu a autoridade: {autoridade['nome']}")
    print("Eventos disponíveis para essa autoridade:")
    for i, ev in enumerate(autoridade["eventos"], start=1):
        print(f"{i} - {ev}")

    while True:
        try:
            escolha_evento = int(input("Escolha o evento pelo número: ").strip())
            if 1 <= escolha_evento <= len(autoridade["eventos"]):
                evento_selecionado = autoridade["eventos"][escolha_evento - 1]
                break
            else:
                print("Número inválido, tente novamente.")
        except ValueError:
            print("Digite um número válido.")

    confirma = input(f"Deseja confirmar o SOS para '{evento_selecionado}' com a autoridade '{autoridade['nome']}'? (S/N): ").strip().upper()
    if confirma == "S":
        resposta = {
            "status": "SOS confirmado",
            "autoridade": autoridade["nome"],
            "telefone": autoridade["telefone"],
            "evento": evento_selecionado,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        print("\nSOS confirmado com sucesso! Dados:")
        print(json.dumps(resposta, indent=4, ensure_ascii=False))

        # Salvar no arquivo JSON
        dados_anteriores = []
        if os.path.exists(ARQUIVO_OCORRENCIAS):
            with open(ARQUIVO_OCORRENCIAS, "r", encoding="utf-8") as f:
                try:
                    dados_anteriores = json.load(f)
                except json.JSONDecodeError:
                    dados_anteriores = []

        dados_anteriores.append(resposta)

        with open(ARQUIVO_OCORRENCIAS, "w", encoding="utf-8") as f:
            json.dump(dados_anteriores, f, ensure_ascii=False, indent=4)

        return resposta
    else:
        print("\nSOS cancelado. Retornando ao menu principal.")
        return None

# ----- Função 7 modificada: Painel de administração (acesso só para admin, mostra SOS do JSON) -----
def exportar_autoridades_por_especialidade():
    print("\n*** Painel de Administração - Login Necessário ***")
    cpf = input("Digite seu CPF: ").strip()
    senha = input("Digite sua senha: ").strip()

    # Verifica se é o admin pelo CPF e senha únicos
    if cpf != ADMIN_CPF or senha != ADMIN_SENHA:
        print("Acesso negado. CPF ou senha incorretos.")
        return None

    print(f"\nAdmin autenticado com sucesso. Mostrando ocorrências SOS armazenadas...")

    if not os.path.exists(ARQUIVO_OCORRENCIAS):
        print("Nenhuma ocorrência SOS registrada até o momento.")
        return None

    try:
        with open(ARQUIVO_OCORRENCIAS, "r", encoding="utf-8") as f:
            ocorrencias = json.load(f)
        if not ocorrencias:
            print("Nenhuma ocorrência SOS registrada até o momento.")
            return None

        print("\n--- Ocorrências SOS registradas ---")
        for i, ocorr in enumerate(ocorrencias, start=1):
            print(f"{i}. Status: {ocorr['status']}")
            print(f"   Autoridade: {ocorr['autoridade']} | Telefone: {ocorr['telefone']}")
            print(f"   Evento: {ocorr['evento']}")
            print(f"   Data/Hora: {ocorr['timestamp']}\n")
        return ocorrencias
    except Exception as e:
        print("Erro ao ler o arquivo de ocorrências:", e)
        return None


# Função menu principal que chama as funções
def main():
    while True:
        print("""
Escolha uma opção:
1 - Inserir usuário
2 - Listar usuários
3 - Buscar usuário por CPF
4 - Atualizar usuário
5 - Deletar usuário
6 - Botão SOS
7 - Painel de administração (admin)
0 - Sair
""")
        escolha = input("Opção: ").strip()
        if escolha == "1":
            inserir_usuario()
        elif escolha == "2":
            listar_usuarios()
        elif escolha == "3":
            buscar_usuario_por_cpf()
        elif escolha == "4":
            atualizar_usuario()
        elif escolha == "5":
            deletar_usuario()
        elif escolha == "6":
            exportar_ocorrencias_por_status()
        elif escolha == "7":
            exportar_autoridades_por_especialidade()
        elif escolha == "0":
            print("Encerrando o programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
