from database import Database

class Query:
    def __init__(self, database):
        self.db = database
    def result(self, data):
        """Print query results (list of dicts)."""
        if data:
            for d in data:
                print(d)
        else:
            print("Nenhum resultado encontrado!")

    def find_Renzo(self): # Questão 1 - a. ------------------------------
        query = "MATCH (t:Teacher {name: $name}) RETURN t.ano_nasc AS ano_nasc, t.cpf AS cpf"
        parameters = {"name": "Renzo"}
        self.result(self.db.execute_query(query, parameters))

    def find_teacher_M(self): # Questão 1 - b. ------------------------------
        query = "MATCH (t:Teacher) WHERE t.name STARTS WITH $prefix RETURN t.name AS name, t.cpf AS cpf"
        params = {"prefix": "M"}
        self.result(self.db.execute_query(query, params))

    def find_all_cities(self): # Questão 1 - c. ------------------------------
        query = "MATCH (c:City) RETURN c.name AS name"
        self.result(self.db.execute_query(query))
    
    def find_number_school(self): # Questão 1 - d. ------------------------------
        query = "MATCH (s:School) WHERE s.number >= $min AND s.number <= $max RETURN s.name AS name, s.address AS address, s.number AS number"
        params = {"min": 150, "max": 550}
        self.result(self.db.execute_query(query, params))

    def find_youngest_date(self): # Questão 2 - a. ------------------------------
        # retorna ano de nascimento do mais velho (MIN) e do mais jovem (MAX)
        query = "MATCH (t:Teacher) RETURN MIN(t.ano_nasc) AS ano_mais_velho, MAX(t.ano_nasc) AS ano_mais_jovem"
        self.result(self.db.execute_query(query))

    def find_AVG(self): # Questão 2 - b. ------------------------------
        query = "MATCH (c:City) RETURN AVG(c.population) AS media_population"
        self.result(self.db.execute_query(query))

    def find_CEP(self): # Questão 2 - c. ------------------------------
        # substitui 'a' por 'A' no nome (case-sensitive replace)
        query = "MATCH (c:City) WHERE c.cep = $cep RETURN replace(c.name, 'a', 'A') AS name_replaced"
        params = {"cep": "37540-000"}
        self.result(self.db.execute_query(query, params))

    def teachers_third_letter(self): # Questão 2 - d. ------------------------------
        # retorna um caractere iniciando a partir da 3ª letra (index 2)
        query = "MATCH (t:Teacher) RETURN substring(t.name, 2, 1) AS third_char"
        self.result(self.db.execute_query(query))

    def show_results(self):
        self.find_Renzo()
        self.find_teacher_M()
        self.find_all_cities()
        self.find_number_school() 
        self.find_youngest_date()
        self.find_AVG()
        self.find_CEP()
        self.teachers_third_letter()
        self.db.close()