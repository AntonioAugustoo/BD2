"""
Models (entidades) do CineGraph.
Representa filmes, pessoas, gêneros e características.
"""

class Filme:
    """Representa um filme com título, ano, sinopse, gêneros e características."""
    
    def __init__(self, titulo, ano, sinopse, generos=None, caracteristicas=None):
        self.titulo = titulo
        self.ano = ano
        self.sinopse = sinopse
        self.generos = generos or []
        self.caracteristicas = caracteristicas or []

    def to_dict(self):
        """Retorna dicionário com os atributos básicos do filme."""
        return {"titulo": self.titulo, "ano": self.ano, "sinopse": self.sinopse}


class Pessoa:
    """Representa uma pessoa (ator/atriz) e os filmes em que atuou."""
    
    def __init__(self, nome, filmes_atuados=None):
        self.nome = nome
        self.filmes_atuados = filmes_atuados or []

    def to_dict(self):
        """Retorna dicionário com o nome da pessoa."""
        return {"nome": self.nome}


class Genero:
    """Representa um gênero cinematográfico."""
    
    def __init__(self, nome):
        self.nome = nome

    def to_dict(self):
        """Retorna dicionário com o nome do gênero."""
        return {"nome": self.nome}


class Caracteristica:
    """Representa uma característica de filme (ex: 'cult', 'blockbuster')."""
    
    def __init__(self, nome):
        self.nome = nome

    def to_dict(self):
        """Retorna dicionário com o nome da característica."""
        return {"nome": self.nome}
