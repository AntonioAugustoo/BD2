from database import Database
from helper.writeAJson import writeAJson

db = Database(database="pokedex", collection="pokemons")
#db.resetDatabase()

def getPokemonsByType(types: list):
    return db.collection.find({"type": {"$in": types}})

types = ["Grass"]
pokemons = getPokemonsByType(types)

writeAJson(pokemons, "pokemons_by_type")

pokemons = db.collection.find({"$or": [{"type":"Fire"},{"weaknesses": "Fire"}]})
writeAJson(pokemons, "Fraqueza de fogo")

fraquezas = ["Water", "Ice"]
pokemons = db.collection.find({"weaknesses": {"$all": fraquezas}})
writeAJson(pokemons, "Fraqueza de Agaue e Gelo")