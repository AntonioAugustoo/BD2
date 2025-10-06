class Game:
    def __init__(self, database):
        self.db = database

    def create_player(self, name):
        query = "CREATE (p:Player {name: $name}) RETURN p"
        return self.db.execute_query(query, {"name": name})

    def read_players(self):  # lista de jogadores
        query = "MATCH (p:Player) RETURN p"
        return self.db.execute_query(query)

    def read_player(self, player_id):
        query = "MATCH (p:Player) WHERE id(p) = $player_id RETURN p"
        return self.db.execute_query(query, {"player_id": player_id})

    def update_player(self, player_id, name):
        query = "MATCH (p:Player) WHERE id(p) = $player_id SET p.name = $name RETURN p"
        return self.db.execute_query(query, {"player_id": player_id, "name": name})

    def delete_player(self, player_id):
        query = "MATCH (p:Player) WHERE id(p) = $player_id DETACH DELETE p"
        return self.db.execute_query(query, {"player_id": player_id})

    def create_match(self, players, winner):
        query = "MATCH (p:Player) WHERE id(p) IN $players CREATE (m:Match {winner: $winner}) WITH m, p UNWIND $players AS player_id MATCH (p:Player) WHERE id(p) = player_id CREATE (p)-[:PARTICIPANT]->(m) RETURN m"
        return self.db.execute_query(query, {"players": players, "winner": winner})

    def read_matches(self):
        query = "MATCH (m:Match) RETURN m"
        return self.db.execute_query(query)

    def read_match(self, match_id):  # informações sobre uma partida específica
        query = "MATCH (m:Match) WHERE id(m) = $match_id RETURN m"
        return self.db.execute_query(query, {"match_id": match_id})

    def read_player_matches(self, player_id):  # histórico de partidas de um jogador
        query = "MATCH (p:Player)-[:PARTICIPANT]-(m:Match) WHERE id(p) = $player_id RETURN m"
        return self.db.execute_query(query, {"player_id": player_id})

    def delete_match(self, match_id):
        query = "MATCH (m:Match) WHERE id(m) = $match_id DETACH DELETE m"
        return self.db.execute_query(query, {"match_id": match_id})

    def delete_all(self):
        self.db.drop_all()