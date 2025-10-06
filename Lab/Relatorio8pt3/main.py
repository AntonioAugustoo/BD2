from database import Database
from BdJogo import Game
def main():
    # Criar a conexão com o banco de dados Neo4j
    db = Database("bolt://107.23.80.166:7687", "neo4j", "till-accessory-taxis")
    db.drop_all()

    # Criar uma instância da classe Game passando a conexão com o banco de dados
    game_db = Game(db)

    while True:
        print("\n1 - Criar jogador")
        print("2 - Listar jogadores")
        print("3 - Ler jogador")
        print("4 - Atualizar jogador")
        print("5 - Deletar jogador")
        print("6 - Criar partida")
        print("7 - Listar partidas de um jogador")
        print("8 - Ler partida")
        print("9 - Sair")

        op = int(input("Digite a opção desejada: "))

        if op == 1:
            name = input("Digite o nome do jogador: ")
            game_db.create_player(name)
        elif op == 2:
            players = game_db.read_players()
            print("Jogadores:")
            for player in players:
                print(player["p"]["name"])
        elif op == 3:
            player_id = int(input("Digite o ID do jogador: "))
            player = game_db.read_player(player_id)
            print(f"Nome do jogador: {player[0]['p']['name']}")
        elif op == 4:
            player_id = int(input("Digite o ID do jogador: "))
            name = input("Digite o novo nome do jogador: ")
            game_db.update_player(player_id, name)
            print("Nome do jogador atualizado com sucesso!")
        elif op == 5:
            player_id = int(input("Digite o ID do jogador: "))
            game_db.delete_player(player_id)
            print("Jogador excluído com sucesso!")
        elif op == 6:
            players = []
            while True:
                player_id = int(input("Digite o ID de um jogador participante (ou 0 para parar): "))
                if player_id == 0:
                    break
                players.append(player_id)
            winner = int(input("Digite o ID do jogador vencedor: "))
            game_db.create_match(players, winner)
            print("Partida criada com sucesso!")
        elif op == 7:
            player_id = int(input("Digite o ID do jogador: "))
            matches = game_db.read_player_matches(player_id)
            print(f"Partidas do jogador {player_id}:")
            for match in matches:
                print(match["m"]["winner"])
        elif op == 8:
            match_id = int(input("Digite o ID da partida: "))
            match = game_db.read_match(match_id)
            print(f"Vencedor da partida {match_id}: {match[0]['m']['winner']}")
        elif op == 9:
            db.close()
            break
        else:
            print("Opção inválida")


if __name__ == "__main__":
    main()
