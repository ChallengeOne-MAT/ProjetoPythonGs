import re

usuarios = {}
autoridades = {
    '1': 'Bombeiros',
    '2': 'Polícia',
    '3': 'SAMU',
    '4': 'Controle de Zoonoses',
    '5': 'Defesa Civil',
    '6': 'Guarda Municipal',
    '7': 'Equipes de Resgate Voluntário',
    '8': 'Força Nacional'
}

def validar_cpf(cpf: str) -> bool:
    return bool(re.fullmatch(r'\d{11}', cpf))

def validar_telefone(tel: str) -> bool:
    return bool(re.fullmatch(r'\d{11}', tel))

def salvar_usuario(cpf, nome, telefone):
    try:
        if cpf in usuarios:
            raise Exception("Usuário já cadastrado.")
        usuarios[cpf] = {'nome': nome, 'telefone': telefone}
        print(f"Usuário {nome} cadastrado com sucesso.")
        return True
    except Exception as e:
        print(f"Erro ao salvar usuário: {e}")
        return False

def listar_autoridades():
    print("\nAutoridades disponíveis:")
    for chave, nome in autoridades.items():
        print(f"{chave}. {nome}")

def acionar_sos(cpf):
    try:
        if cpf not in usuarios:
            raise Exception("Usuário não encontrado. Cadastre-se antes.")
        print(f"\nALERTA! Usuário {usuarios[cpf]['nome']} acionou o botão SOS.")
        print("Notificando contatos de emergência e compartilhando localização...\n")
        return True
    except Exception as e:
        print(f"Erro no acionamento do SOS: {e}")
        return False

def menu():
    while True:
        print("\n--- SafeCall Sistema ---")
        print("1 - Cadastrar Usuário")
        print("2 - Listar Autoridades")
        print("3 - Acionar Botão SOS")
        print("4 - Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            nome = input("Nome completo: ").strip()
            cpf = input("CPF (11 dígitos): ").strip()
            telefone = input("Telefone (11 dígitos, ex: 11999999999): ").strip()

            if not validar_cpf(cpf):
                print("CPF inválido.")
                continue
            if not validar_telefone(telefone):
                print("Telefone inválido.")
                continue

            salvar_usuario(cpf, nome, telefone)

        elif escolha == '2':
            listar_autoridades()

        elif escolha == '3':
            cpf = input("Informe seu CPF para acionamento: ").strip()
            acionar_sos(cpf)

        elif escolha == '4':
            print("Saindo do sistema SafeCall. Até mais!")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
import re

usuarios = {}
autoridades = {
    '1': 'Bombeiros',
    '2': 'Polícia',
    '3': 'SAMU',
    '4': 'Controle de Zoonoses',
    '5': 'Defesa Civil',
    '6': 'Guarda Municipal',
    '7': 'Equipes de Resgate Voluntário',
    '8': 'Força Nacional'
}

def validar_cpf(cpf: str) -> bool:
    return bool(re.fullmatch(r'\d{11}', cpf))

def validar_telefone(tel: str) -> bool:
    return bool(re.fullmatch(r'\d{11}', tel))

def salvar_usuario(cpf, nome, telefone):
    try:
        if cpf in usuarios:
            raise Exception("Usuário já cadastrado.")
        usuarios[cpf] = {'nome': nome, 'telefone': telefone}
        print(f"Usuário {nome} cadastrado com sucesso.")
        return True
    except Exception as e:
        print(f"Erro ao salvar usuário: {e}")
        return False

def listar_autoridades():
    print("\nAutoridades disponíveis:")
    for chave, nome in autoridades.items():
        print(f"{chave}. {nome}")

def acionar_sos(cpf):
    try:
        if cpf not in usuarios:
            raise Exception("Usuário não encontrado. Cadastre-se antes.")
        print(f"\nALERTA! Usuário {usuarios[cpf]['nome']} acionou o botão SOS.")
        print("Notificando contatos de emergência e compartilhando localização...\n")
        return True
    except Exception as e:
        print(f"Erro no acionamento do SOS: {e}")
        return False

def menu():
    while True:
        print("\n--- SafeCall Sistema ---")
        print("1 - Cadastrar Usuário")
        print("2 - Listar Autoridades")
        print("3 - Acionar Botão SOS")
        print("4 - Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            nome = input("Nome completo: ").strip()
            cpf = input("CPF (11 dígitos): ").strip()
            telefone = input("Telefone (11 dígitos, ex: 11999999999): ").strip()

            if not validar_cpf(cpf):
                print("CPF inválido.")
                continue
            if not validar_telefone(telefone):
                print("Telefone inválido.")
                continue

            salvar_usuario(cpf, nome, telefone)

        elif escolha == '2':
            listar_autoridades()

        elif escolha == '3':
            cpf = input("Informe seu CPF para acionamento: ").strip()
            acionar_sos(cpf)

        elif escolha == '4':
            print("Saindo do sistema SafeCall. Até mais!")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
