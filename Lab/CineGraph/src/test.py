from neo4j import GraphDatabase

uri = "bolt://3.85.29.90:7687"
user = "neo4j"
password = "entrances-leader-ax"

driver = GraphDatabase.driver(uri, auth=(user, password))

with driver.session() as session:
    result = session.run("RETURN 'Conectou!' AS msg")
    print(result.single()["msg"])

driver.close()
