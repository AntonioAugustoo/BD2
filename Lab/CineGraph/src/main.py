"""
CineGraph - Sistema CLI para gerenciar filmes, pessoas, gêneros e características.
Aplicação CRUD com Neo4j usando orientação a objetos.
"""
from models import Filme, Pessoa, Genero, Caracteristica
from dao import FilmeDAO, PessoaDAO, GeneroDAO, CaracteristicaDAO

# ------------------- MENUS -------------------

def menu_filmes():
    """Menu de CRUD para filmes."""
    dao = FilmeDAO()

    while True:
        print("""
===== FILMES =====
1 - Cadastrar filme
2 - Listar filmes
3 - Atualizar filme
4 - Remover filme
0 - Voltar
""")
        op = input("Opção: ")

        if op == "1":
            titulo = input("Título: ")
            ano = int(input("Ano: "))
            sinopse = input("Sinopse: ")

            # Gêneros separados por vírgula
            generos = input("Gêneros (vírgula): ").split(",")
            generos = [g.strip() for g in generos if g.strip()]

            # Características separadas por vírgula
            carac = input("Características (vírgula): ").split(",")
            carac = [c.strip() for c in carac if c.strip()]

            filme = Filme(titulo, ano, sinopse, generos, carac)
            dao.add_filme(filme)

        elif op == "2":
            for f in dao.list_filmes():
                print(f)

        elif op == "3":
            titulo = input("Filme a atualizar: ")
            novo = input("Novo título: ") or None
            ano = input("Novo ano: ")
            ano = int(ano) if ano else None
            sinopse = input("Nova sinopse: ") or None

            dao.update_filme(titulo, novo, ano, sinopse)

        elif op == "4":
            titulo = input("Título do filme: ")
            dao.delete_filme(titulo)

        elif op == "0":
            break


def menu_pessoas():
    """Menu de CRUD para pessoas (atores/atrizes)."""
    dao = PessoaDAO()

    while True:
        print("""
===== PESSOAS =====
1 - Cadastrar pessoa
2 - Listar pessoas
3 - Atualizar pessoa
4 - Remover pessoa
0 - Voltar
""")
        op = input("Opção: ")

        if op == "1":
            nome = input("Nome: ")
            filmes = input("Filmes atuados (vírgula): ").split(",")
            filmes = [f.strip() for f in filmes if f.strip()]
            pessoa = Pessoa(nome, filmes)
            dao.add_pessoa(pessoa)

        elif op == "2":
            for p in dao.list_pessoas():
                print(p)

        elif op == "3":
            nome = input("Nome atual: ")
            novo = input("Novo nome: ")
            dao.update_pessoa(nome, novo)

        elif op == "4":
            nome = input("Nome: ")
            dao.delete_pessoa(nome)

        elif op == "0":
            break


def menu_generos():
    """Menu de CRUD para gêneros."""
    dao = GeneroDAO()

    while True:
        print("""
===== GÊNEROS =====
1 - Cadastrar gênero
2 - Listar gêneros
3 - Atualizar gênero
4 - Remover gênero
0 - Voltar
""")
        op = input("Opção: ")

        if op == "1":
            nome = input("Nome: ")
            dao.add_genero(Genero(nome))

        elif op == "2":
            for g in dao.list_generos():
                print(g)

        elif op == "3":
            atual = input("Nome atual: ")
            novo = input("Novo nome: ")
            dao.update_genero(atual, novo)

        elif op == "4":
            nome = input("Nome: ")
            dao.delete_genero(nome)

        elif op == "0":
            break


def menu_caracteristicas():
    """Menu de CRUD para características de filmes."""
    dao = CaracteristicaDAO()

    while True:
        print("""
===== CARACTERÍSTICAS =====
1 - Cadastrar característica
2 - Listar características
3 - Atualizar característica
4 - Remover característica
0 - Voltar
""")
        op = input("Opção: ")

        if op == "1":
            nome = input("Nome: ")
            dao.add_caracteristica(Caracteristica(nome))

        elif op == "2":
            for c in dao.list_caracteristicas():
                print(c)

        elif op == "3":
            atual = input("Nome atual: ")
            novo = input("Novo nome: ")
            dao.update_caracteristica(atual, novo)

        elif op == "4":
            nome = input("Nome: ")
            dao.delete_caracteristica(nome)

        elif op == "0":
            break


# ------------------- MAIN -------------------

def main():
    """Menu principal do sistema CineGraph."""
    while True:
        print("""
===== CINEGRAPH — MENU PRINCIPAL =====
1 - CRUD Filmes
2 - CRUD Pessoas
3 - CRUD Gêneros
4 - CRUD Características
0 - Sair
""")
        op = input("Opção: ")

        if op == "1":
            menu_filmes()
        elif op == "2":
            menu_pessoas()
        elif op == "3":
            menu_generos()
        elif op == "4":
            menu_caracteristicas()
        elif op == "0":
            print("Saindo...")
            break


if __name__ == "__main__":
    main()
