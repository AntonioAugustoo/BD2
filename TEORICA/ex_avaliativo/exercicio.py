from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

class FamilyGraphClient:
   
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            print("Conexão com o banco de dados estabelecida com sucesso!")
        except ServiceUnavailable as e:
            print(f"Erro de conexão com o banco de dados: {e}")
            raise

    def close(self):
        self.driver.close()
        print("\nConexão com o banco de dados fechada.")

    

    def get_engineers(self):
        """Pergunta: Quem da família é Engenheiro?"""
        with self.driver.session() as session:
            return session.execute_read(self._find_people_by_profession, "Engenheiro")

    @staticmethod
    def _find_people_by_profession(tx, profession):
        query = """
            MATCH (p:Pessoa)
            WHERE $profession IN LABELS(p)
            RETURN p.nome AS nome
        """
        result = tx.run(query, profession=profession)
        return [record["nome"] for record in result]

    def get_children_of(self, parent_name):
        """Pergunta: 'Fulano de tal' é pai/mãe de quem?"""
        with self.driver.session() as session:
            return session.execute_read(self._find_children, parent_name)

    @staticmethod
    def _find_children(tx, name):
        query = """
            MATCH (parent:Pessoa {nome: $name})-[:PAI_DE]->(child:Pessoa)
            RETURN child.nome AS nome_filho
        """
        result = tx.run(query, name=name)
        return [record["nome_filho"] for record in result]

    def get_partner_info(self, person_name):
        """Pergunta: 'Sicrana de tal' é esposa de quem desde quando?"""
        with self.driver.session() as session:
            return session.execute_read(self._find_partner, person_name)

    @staticmethod
    def _find_partner(tx, name):
 
        query = """
            MATCH (p1:Pessoa {nome: $name})-[r:ESPOSO_DE]-(p2:Pessoa)
            RETURN p2.nome AS nome_parceiro, r.casados_desde AS data
        """
        result = tx.run(query, name=name)
        return result.single() 


def main():

    
    URI = "neo4j+s://2c6fa8ce.databases.neo4j.io"
    USER = "neo4j"
    PASSWORD = "x4ONBz2tWNxA6SXajm_Ji3JWrFlc9FNx3tHQTxfpIYQ"
    
    
    try:
        client = FamilyGraphClient(URI, USER, PASSWORD)

    
        while True:
            print("\n--- MENU DE CONSULTA DA FAMÍLIA ---")
            print("1. Quem da família é Engenheiro?")
            print("2. Descobrir os filhos de uma pessoa.")
            print("3. Ver com quem uma pessoa é casada e desde quando.")
            print("4. Sair")
            
            choice = input("Escolha uma opção: ")

            if choice == '1':
                engineers = client.get_engineers()
                if engineers:
                    print("\nResultado: As seguintes pessoas são engenheiras:")
                    for engineer in engineers:
                        print(f"- {engineer}")
                else:
                    print("\nResultado: Ninguém da família é engenheiro.")

            elif choice == '2':
                parent_name = input("Digite o nome do pai ou mãe que você quer consultar: ")
                children = client.get_children_of(parent_name)
                if children:
                    print(f"\nResultado: Os filhos de {parent_name} são:")
                    for child in children:
                        print(f"- {child}")
                else:
                    print(f"\nResultado: {parent_name} não foi encontrado ou não possui filhos cadastrados.")

            elif choice == '3':
                person_name = input("Digite o nome da pessoa que você quer consultar o cônjuge: ")
                partner_info = client.get_partner_info(person_name)
                if partner_info:
                    partner = partner_info["nome_parceiro"]
                    since = partner_info["data"]
                    print(f"\nResultado: {person_name} é cônjuge de {partner} desde {since}.")
                else:
                    print(f"\nResultado: {person_name} não foi encontrado ou não possui cônjuge cadastrado.")

            elif choice == '4':
                break
            
            else:
                print("\nOpção inválida. Por favor, tente novamente.")

    except Exception as e:
        print(f"\nOcorreu um erro durante a execução: {e}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    main()