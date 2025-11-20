"""
Configuração de conexão com o banco de dados Neo4j.
Implementa padrão Singleton para o driver.
"""
from neo4j import GraphDatabase

class Neo4jDriver:
    """Gerencia a conexão única (singleton) com o banco Neo4j."""

    # Credenciais e endpoint do banco
    neo4j_host = "bolt://3.85.29.90:7687"
    neo4j_user = "neo4j"
    neo4j_password = "entrances-leader-ax"

    driver = None

    @staticmethod
    def get_driver():
        """Retorna a instância única do driver Neo4j."""
        if not Neo4jDriver.driver:
            Neo4jDriver.driver = GraphDatabase.driver(
                Neo4jDriver.neo4j_host,
                auth=(Neo4jDriver.neo4j_user, Neo4jDriver.neo4j_password)
            )
        return Neo4jDriver.driver
    