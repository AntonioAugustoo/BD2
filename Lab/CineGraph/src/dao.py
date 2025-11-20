"""
Camada DAO (Data Access Object) para CRUD no Neo4j.
Gerencia operações de Filme, Pessoa, Genero e Caracteristica.
"""
from config import Neo4jDriver
from models import Filme, Pessoa, Genero, Caracteristica

class FilmeDAO:
    """DAO para operações CRUD de filmes."""
    
    def __init__(self):
        self.driver = Neo4jDriver.get_driver()

    def add_filme(self, filme: Filme):
        """Adiciona um filme ao banco, incluindo gêneros e características."""
        with self.driver.session() as session:
            # Cria/atualiza o nó Filme
            session.run("""
                MERGE (f:Filme {titulo: $titulo})
                SET f.ano = $ano, f.sinopse = $sinopse
            """, **filme.to_dict())

            # Cria relacionamento com gêneros
            for genero in filme.generos:
                session.run("""
                    MATCH (f:Filme {titulo: $titulo})
                    MERGE (g:Genero {nome: $g})
                    MERGE (f)-[:TEM_GENERO]->(g)
                """, titulo=filme.titulo, g=genero)

            # Cria relacionamento com características
            for car in filme.caracteristicas:
                session.run("""
                    MATCH (f:Filme {titulo: $titulo})
                    MERGE (c:Caracteristica {nome: $c})
                    MERGE (f)-[:TEM_CARAC]->(c)
                """, titulo=filme.titulo, c=car)

    def list_filmes(self):
        """Retorna lista de todos os filmes (título e ano)."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (f:Filme)
                RETURN f.titulo AS titulo, f.ano AS ano
            """)
            return [r.data() for r in result]

    def update_filme(self, titulo, novo_titulo=None, ano=None, sinopse=None):
        """Atualiza dados de um filme existente."""
        with self.driver.session() as session:
            session.run("""
                MATCH (f:Filme {titulo: $titulo})
                SET f.titulo = COALESCE($novo_titulo, f.titulo),
                    f.ano = COALESCE($ano, f.ano),
                    f.sinopse = COALESCE($sinopse, f.sinopse)
            """, titulo=titulo, novo_titulo=novo_titulo, ano=ano, sinopse=sinopse)

    def delete_filme(self, titulo):
        """Remove um filme e seus relacionamentos."""
        with self.driver.session() as session:
            session.run("""
                MATCH (f:Filme {titulo: $titulo})
                DETACH DELETE f
            """, titulo=titulo)


class PessoaDAO:
    """DAO para operações CRUD de pessoas (atores/atrizes)."""
    
    def __init__(self):
        self.driver = Neo4jDriver.get_driver()

    def add_pessoa(self, pessoa: Pessoa):
        """Adiciona uma pessoa e seus relacionamentos com filmes."""
        with self.driver.session() as session:
            session.run("MERGE (p:Pessoa {nome: $nome})", **pessoa.to_dict())

            # Cria relacionamento ATUOU_EM com os filmes
            for filme in pessoa.filmes_atuados:
                session.run("""
                    MATCH (p:Pessoa {nome: $p})
                    MATCH (f:Filme {titulo: $f})
                    MERGE (p)-[:ATUOU_EM]->(f)
                """, p=pessoa.nome, f=filme)

    def list_pessoas(self):
        """Retorna lista de todas as pessoas."""
        with self.driver.session() as session:
            result = session.run("MATCH (p:Pessoa) RETURN p.nome AS nome")
            return [r.data() for r in result]

    def update_pessoa(self, nome, novo_nome):
        """Atualiza o nome de uma pessoa."""
        with self.driver.session() as session:
            session.run("""
                MATCH (p:Pessoa {nome: $nome})
                SET p.nome = $novo_nome
            """, nome=nome, novo_nome=novo_nome)

    def delete_pessoa(self, nome):
        """Remove uma pessoa e seus relacionamentos."""
        with self.driver.session() as session:
            session.run("""
                MATCH (p:Pessoa {nome: $nome})
                DETACH DELETE p
            """, nome=nome)


class GeneroDAO:
    """DAO para operações CRUD de gêneros."""
    
    def __init__(self):
        self.driver = Neo4jDriver.get_driver()

    def add_genero(self, genero: Genero):
        """Adiciona um gênero ao banco."""
        self.driver.execute_query("""
            MERGE (g:Genero {nome: $nome})
        """, **genero.to_dict())

    def list_generos(self):
        """Retorna lista de todos os gêneros ordenados por nome."""
        with self.driver.session() as session:
            result = session.run("MATCH (g:Genero) RETURN g.nome AS nome ORDER BY nome")
            return [r.data() for r in result]

    def update_genero(self, nome, novo_nome):
        """Atualiza o nome de um gênero."""
        with self.driver.session() as session:
            session.run("""
                MATCH (g:Genero {nome: $nome})
                SET g.nome = $novo_nome
            """, nome=nome, novo_nome=novo_nome)

    def delete_genero(self, nome):
        """Remove um gênero e seus relacionamentos."""
        with self.driver.session() as session:
            session.run("""
                MATCH (g:Genero {nome: $nome})
                DETACH DELETE g
            """, nome=nome)


class CaracteristicaDAO:
    """DAO para operações CRUD de características de filmes."""
    
    def __init__(self):
        self.driver = Neo4jDriver.get_driver()

    def add_caracteristica(self, caracteristica: Caracteristica):
        """Adiciona uma característica ao banco."""
        self.driver.execute_query("""
            MERGE (c:Caracteristica {nome: $nome})
        """, **caracteristica.to_dict())

    def list_caracteristicas(self):
        """Retorna lista de todas as características ordenadas por nome."""
        with self.driver.session() as session:
            result = session.run("MATCH (c:Caracteristica) RETURN c.nome AS nome ORDER BY nome")
            return [r.data() for r in result]

    def update_caracteristica(self, nome, novo_nome):
        """Atualiza o nome de uma característica."""
        with self.driver.session() as session:
            session.run("""
                MATCH (c:Caracteristica {nome: $nome})
                SET c.nome = $novo_nome
            """, nome=nome, novo_nome=novo_nome)

    def delete_caracteristica(self, nome):
        """Remove uma característica e seus relacionamentos."""
        with self.driver.session() as session:
            session.run("""
                MATCH (c:Caracteristica {nome: $nome})
                DETACH DELETE c
            """, nome=nome)
