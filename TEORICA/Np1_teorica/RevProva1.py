import pymongo
from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.server_api import ServerApi
from neo4j import GraphDatabase

class MongoDBCollection:
    mongo_uri = "mongodb+srv://antonio:1234@clusterrev.svhjo7e.mongodb.net/?retryWrites=true&w=majority"
    collection = None

    @staticmethod
    def get_collection():
        if not MongoDBCollection.collection:
            client = MongoClient(MongoDBCollection.mongo_uri, server_api=ServerApi('1'))
            database = client.get_database('library_db')
            MongoDBCollection.collection = database.get_collection('books')
    
            MongoDBCollection.collection.delete_many({})
        return MongoDBCollection.collection
    
class Neo4jDriver:
    neo4j_host = "neo4j+s://203d04de.databases.neo4j.io"
    neo4j_user = "neo4j"
    neo4j_password = "1W37ROugatWPYM2e0pPIkedH58ZcDAMHoF3Fb3v_tG0"

    driver = None

    @staticmethod
    def get_driver():
        if not Neo4jDriver.driver:
            Neo4jDriver.driver = GraphDatabase.driver(Neo4jDriver.neo4j_host, auth=(Neo4jDriver.neo4j_user, Neo4jDriver.neo4j_password))
            
            with Neo4jDriver.driver.session() as session:
                session.run("MATCH(n) DETACH DELETE n")
        return Neo4jDriver.driver

class Book:
    def __init__(self, title, author, year, pages, category):
        self.title = title
        self.author = author
        self.year = year
        self.pages = pages
        self.category = category

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "pages": self.pages,
            "category": self.category,
        }

class Article:
    def __init__(self, title, abstract, keywords, research_area, access_requirements = []):
        self.title = title
        self.abstract = abstract
        self.keywords = keywords
        self.research_area = research_area
        self.access_requirements = access_requirements

    def to_dict(self):
        return {
            "title": self.title,
            "abstract": self.abstract,
            "keywords": self.keywords,
            "research_area": self.research_area,
            "access_requirements": self.access_requirements,
        }

class Researcher:
    def __init__(self, name, age, specialization, department, university, join_date):
        self.name = name
        self.age = age
        self.specialization = specialization
        self.department = department
        self.university = university
        self.join_date = join_date

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "specialization": self.specialization,
            "department": self.department,
            "university": self.university,
            "join_date": self.join_date
        }

class BookDAO:
    def __init__(self) -> None:
        self.mongo_collection = MongoDBCollection.get_collection()

    def add_book(self, book: Book):
        self.mongo_collection.insert_one(book.to_dict())

    def get_books_by_category(self, category: str):
        query_filter = {"category": category}
        projection = {"_id": 0, "title": 1, "year": 1}
        sort_order = [("year", DESCENDING), ("title", ASCENDING)]
        
        cursor = self.mongo_collection.find(query_filter, projection).sort(sort_order)
        return list(cursor)

class ArticleDAO:
    def __init__(self) -> None:
        self.neo4j_driver = Neo4jDriver.get_driver()

    def add_article(self, article: Article):
        with self.neo4j_driver.session() as session:
            session.run("""
                MERGE (a:Article {title: $title})
                SET a.abstract = $abstract, a.keywords = $keywords, a.research_area = $research_area
            """, article.to_dict())

            for requirement in article.access_requirements:
                session.run("""
                    MATCH (a:Article {title: $title})
                    MERGE (t:Topic {name: $requirement})
                    MERGE (a)-[:REQUIRES_ACCESS]->(t)
                """, title=article.title, requirement=requirement)

class ResearcherDAO:
    def __init__(self) -> None:
        self.neo4j_driver = Neo4jDriver.get_driver()

    def add_researcher(self, researcher: Researcher):
        with self.neo4j_driver.session() as session:
            session.run("""
                CREATE (r:Researcher {
                    name: $name, 
                    age: $age, 
                    university: $university, 
                    join_date: $join_date
                })
            """, researcher.to_dict())

            session.run("""
                MATCH (r:Researcher {name: $name})
                MERGE (t:Topic {name: $specialization})
                MERGE (r)-[:HAS_TOPIC]->(t)
            """, name=researcher.name, specialization=researcher.specialization)

            session.run("""
                MATCH (r:Researcher {name: $name})
                MERGE (t:Topic {name: $department})
                MERGE (r)-[:HAS_TOPIC]->(t)
            """, name=researcher.name, department=researcher.department)

    def get_accessible_articles(self, researcher_name: str):
        with self.neo4j_driver.session() as session:
            result = session.run("""
                MATCH (r:Researcher {name: $researcher_name})-[:HAS_TOPIC]->(topic)<-[:REQUIRES_ACCESS]-(a:Article)
                RETURN DISTINCT a.title as title, a.abstract as abstract, a.research_area as research_area
            """, researcher_name=researcher_name)
            
            return [record.data() for record in result]


book_dao = BookDAO()
article_dao = ArticleDAO()
researcher_dao = ResearcherDAO()

# Questão 1
def test_questao_1():
    print("Executando teste da Questão 1...")
    
    books_data = [
        {"title": "Algoritmos e Estruturas de Dados", "author": "Thomas Cormen", "year": 2020, "pages": 1200, "category": "Técnico"},
        {"title": "Clean Code", "author": "Robert Martin", "year": 2008, "pages": 464, "category": "Técnico"},
        {"title": "1984", "author": "George Orwell", "year": 1949, "pages": 328, "category": "Ficção"}, 
        {"title": "Design Patterns", "author": "Gang of Four", "year": 1994, "pages": 395, "category": "Técnico"},
        {"title": "Deep Learning", "author": "Ian Goodfellow", "year": 2016, "pages": 800, "category": "Técnico"},
        {"title": "Inteligência Artificial: Uma Abordagem Moderna", "author": "Stuart Russell", "year": 2020, "pages": 1136, "category": "Técnico"}
    ]
    input_category = "Técnico"
    
    expected = [
        {"title": "Algoritmos e Estruturas de Dados", "year": 2020},
        {"title": "Inteligência Artificial: Uma Abordagem Moderna", "year": 2020},
        {"title": "Deep Learning", "year": 2016},
        {"title": "Clean Code", "year": 2008},
        {"title": "Design Patterns", "year": 1994}
    ]
    for book_data in books_data:
        book = Book(**book_data)
        book_dao.add_book(book=book)
    
    output = book_dao.get_books_by_category(category=input_category)
    assert expected == output
    print("Teste da Questão 1 passou! ✅")

# Questão 2
def test_questao_2():
    print("Executando teste da Questão 2...")
    
    articles_data = [
        { "title": "Quantum Computing Algorithms for Optimization Problems", "abstract": "This paper explores quantum algorithms...", "keywords": [], "research_area": "Computer Science", "access_requirements": ["Ciência da Computação"] },
        { "title": "Machine Learning Applications in Medical Diagnosis", "abstract": "A comprehensive study on how machine learning...", "keywords": [], "research_area": "Medical AI", "access_requirements": ["Machine Learning", "Ciência da Computação"] },
        { "title": "Computer Vision for Autonomous Vehicles", "abstract": "Advanced computer vision techniques...", "keywords": [], "research_area": "Autonomous Systems", "access_requirements": ["Computer Vision", "Engenharia"] }, # Apenas para o Prof. João
        { "title": "Mathematical Foundations of Machine Learning", "abstract": "Theoretical mathematical principles...", "keywords": [], "research_area": "Mathematical ML", "access_requirements": ["Machine Learning", "Matemática"] }
    ]
    researchers_data = [
        {"name": "Dr. Maria Silva", "age": 35, "specialization": "Machine Learning", "department": "Ciência da Computação", "university": "TechNova", "join_date": "2020-03-15"},
        {"name": "Prof. João Santos", "age": 42, "specialization": "Computer Vision", "department": "Engenharia", "university": "TechNova", "join_date": "2018-08-20"}
    ]
    
    input_researcher_name = "Dr. Maria Silva"
    
    expected = [
        {'title': 'Quantum Computing Algorithms for Optimization Problems', 'abstract': 'This paper explores quantum algorithms...', 'research_area': 'Computer Science'},
        {'title': 'Machine Learning Applications in Medical Diagnosis', 'abstract': 'A comprehensive study on how machine learning...', 'research_area': 'Medical AI'},
        {'title': 'Mathematical Foundations of Machine Learning', 'abstract': 'Theoretical mathematical principles...', 'research_area': 'Mathematical ML'}
    ]

    for article_data in articles_data:
        article_dao.add_article(Article(**article_data))

    for researcher_data in researchers_data:
        researcher_dao.add_researcher(Researcher(**researcher_data))

    output = researcher_dao.get_accessible_articles(researcher_name=input_researcher_name)

    assert sorted(expected, key=lambda d: d['title']) == sorted(output, key=lambda d: d['title'])
    print("Teste da Questão 2 passou! ✅")


if __name__ == "__main__":
    test_questao_1()
    test_questao_2()
    print("\nTodos os testes foram concluídos com sucesso!")