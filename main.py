# main.py
import sqlite3
import database
from new_classes import MembroUniversidade


def menu():
    print("Sistema simples de membros da universidade")
    print("Escolha uma opcao e siga as instrucoes.")

    while True:
        print("\n1 - Cadastrar membro")
        print("2 - Ver um membro")
        print("3 - Atualizar membro")
        print("4 - Deletar membro")
        print("5 - Sair")

        opcao = input("Opcao: ").strip()

        if opcao == "1":
            nome = input("Nome: ").strip()
            email = input("Email: ").strip()
            matricula = input("Matricula: ").strip()
            if not nome or not email or not matricula:
                print("Preencha todos os campos.")
                continue
            try:
                database.criar_membro(nome, email, matricula)
                print("Membro salvo com sucesso.")
            except sqlite3.IntegrityError:
                print("Ja existe um membro com essa matricula.")

        elif opcao == "2":
            matricula = input("Matricula do membro: ").strip()
            if not matricula:
                print("Matricula nao pode ser vazia.")
                continue
            dados = database.buscar_membro(matricula)
            if not dados:
                print("Nenhum membro encontrado.")
            else:
                membro = MembroUniversidade.from_tuple(dados)
                membro.exibir_dados()

        elif opcao == "3":
            matricula = input("Matricula do membro: ").strip()
            if not matricula:
                print("Matricula nao pode ser vazia.")
                continue
            atual = database.buscar_membro(matricula)
            if not atual:
                print("Nenhum membro encontrado.")
                continue
            nome = input("Novo nome: ").strip()
            email = input("Novo email: ").strip()
            if not nome or not email:
                print("Nome e email nao podem ser vazios.")
                continue
            linhas = database.atualizar_membro(nome, email, matricula)
            if linhas:
                print("Dados atualizados.")
            else:
                print("Nada foi atualizado.")

        elif opcao == "4":
            matricula = input("Matricula do membro: ").strip()
            if not matricula:
                print("Matricula nao pode ser vazia.")
                continue
            linhas = database.deletar_membro(matricula)
            if linhas:
                print("Membro removido.")
            else:
                print("Nenhum membro encontrado.")

        elif opcao == "5":
            print("Saindo...")
            break

        else:
            print("Opcao invalida, tente de novo.")


if __name__ == "__main__":
    menu()
