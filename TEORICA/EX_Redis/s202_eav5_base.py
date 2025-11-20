import redis


redis_conn = redis.Redis(
    host="localhost", port=6379,
    decode_responses=True
)

redis_conn.flushall()

# Questão 1
def questao_1(users):
    for user in users:
        # Armazena cada usuário como um Hash no Redis
        redis_conn.hset(f"user:{user['id']}", mapping=user)
    
    
    stored_users = []
    for user in users:
        u = redis_conn.hgetall(f"user:{user['id']}")
        stored_users.append(u)
        
    return stored_users

def test_questao_1():
    input_data = [
        {"id":'1', "nome":"Serafim Amarantes", "email":"samarantes@g.com"},
        {"id":'2', "nome":"Tamara Borges", "email":"tam_borges@g.com"},
        {"id":'3', "nome":"Ubiratã Carvalho", "email":"bira@g.com"},
        {"id":'4', "nome":"Valéria Damasco", "email":"valeria_damasco@g.com"}
    ]
    
    assert sorted(input_data, key=lambda d: d['id']) == sorted(questao_1(input_data), key=lambda d: d['id'])


# Questão 2
def questao_2(interests):
    result = []
    
    for user_data in interests:
        user_id = user_data["usuario"]
        user_interests = user_data["interesses"]
        
        # Mapeia a lista de dicionários para um formato que o ZADD aceita: {nome: score}
        mapping = {}
        for item in user_interests:
            for key, value in item.items():
                mapping[key] = value
        
       
        if mapping:
            redis_conn.zadd(f"user:{user_id}:interests", mapping)

        
        stored = redis_conn.zrange(f"user:{user_id}:interests", 0, -1, withscores=True)
        result.append(stored)

    return result

def test_questao_2():
    input_data = [
        {"usuario":1, "interesses": [{"futebol":0.855}, {"pagode":0.765}, {"engraçado":0.732}, {"cerveja":0.622}, {"estética":0.519}]},
        {"usuario":2, "interesses": [{"estética":0.765}, {"jiujitsu":0.921}, {"luta":0.884}, {"academia":0.541}, {"maquiagem":0.658}]},
        {"usuario":3, "interesses": [{"tecnologia":0.999}, {"hardware":0.865}, {"games":0.745}, {"culinária":0.658}, {"servers":0.54}]},
        {"usuario":4, "interesses": [{"neurociências":0.865}, {"comportamento":0.844}, {"skinner":0.854}, {"laboratório":0.354}, {"pesquisa":0.428}]}
    ]

    
    output = [
        [('estética', 0.519), ('cerveja', 0.622), ('engraçado', 0.732), ('pagode', 0.765), ('futebol', 0.855)],
        [('academia', 0.541), ('maquiagem', 0.658), ('estética', 0.765), ('luta', 0.884), ('jiujitsu', 0.921)], 
        [('servers', 0.54), ('culinária', 0.658), ('games', 0.745), ('hardware', 0.865), ('tecnologia', 0.999)],
        [('laboratório', 0.354), ('pesquisa', 0.428), ('comportamento', 0.844), ('skinner', 0.854), ('neurociências', 0.865)]         
    ]

    assert output == questao_2(input_data)


# Questão 3
def questao_3(posts):
    stored_posts = []
    for post in posts:
        key = f"post:{post['id']}"
       
        redis_conn.hset(key, mapping=post)
        
        redis_conn.expire(key, 18000) 
        
        stored_posts.append(redis_conn.hgetall(key))
    
    return stored_posts

def test_questao_3():
    input_data = [
        {"id": '345', "autor":"news_fc@g.com", "data_hora": "2024-06-10 19:51:03", "conteudo": "Se liga nessa lista de jogadores que vão mudar de time no próximo mês!", "palavras_chave": "brasileirao, futebol, cartola, esporte" },
        {"id": '348', "autor":"gastro_pub@g.com", "data_hora": "2024-06-10 19:55:13", "conteudo": "Aprenda uma receita rápida de onion rings super crocantes.", "palavras_chave": "onion rings, receita, gastronomia, cerveja, culinária" },
        {"id": '349', "autor":"make_with_tina@g.com", "data_hora": "2024-06-10 19:56:44", "conteudo": "A dica de hoje envolve os novos delineadores da linha Rare Beauty", "palavras_chave": "maquiagem, estética, beleza, delineador" },
        {"id": '350', "autor":"samarantes@g.com", "data_hora": "2024-06-10 19:56:48", "conteudo": "Eu quando acho a chuteira que perdi na última pelada...", "palavras_chave": "pelada, futebol, cerveja, parceiros" },
        {"id": '351', "autor":"portal9@g.com", "data_hora": "2024-06-10 19:57:02", "conteudo": "No último mês pesquisadores testaram três novos medicamentos para ajudar aumentar o foco.", "palavras_chave": "neurociências, tecnologia, foco, medicamento" },
        {"id": '352', "autor":"meme_e_cia@g.com", "data_hora": "2024-06-10 19:58:33", "conteudo": "Você prefere compartilhar a nossa página agora ou daqui cinco minutos?", "palavras_chave": "entretenimento, engraçado, viral, meme" },
        {"id": '353', "autor":"rnd_hub@g.com", "data_hora": "2024-06-10 19:59:59", "conteudo": "A polêmica pesquisa de V. Damasco sobre ciência do comportamente acaba de ser publicada.", "palavras_chave": "comportamento, ciência, pesquisa, damasco" }
    ]

    assert sorted(input_data, key=lambda d: d['id']) == sorted(questao_3(input_data), key=lambda d: d['id'])


# Questão 4
def questao_4(user_id):
    # Pega todas as chaves de post
    post_keys = redis_conn.keys("post:*")
    
    
    user_interests = redis_conn.zrange(f"user:{user_id}:interests", 0, -1, withscores=True)
    
   
    interests_dict = {name: score for name, score in user_interests}

    post_scores = []
    
    for key in post_keys:
        post_data = redis_conn.hgetall(key)
        
        
        post_keywords = [k.strip() for k in post_data["palavras_chave"].split(",")]
        
        
        score = 0
        for keyword in post_keywords:
            if keyword in interests_dict:
                score += interests_dict[keyword]
                
        post_scores.append((score, post_data["conteudo"]))

    post_scores.sort(key=lambda x: (-x[0], x[1]))
    
    top_posts = [post[1] for post in post_scores]
    
    return top_posts

def test_questao_4():
    input_id = 3 
    output = [
        "No último mês pesquisadores testaram três novos medicamentos para ajudar aumentar o foco.", # Score alto (tecnologia)
        "Aprenda uma receita rápida de onion rings super crocantes.", # Culinaria
        "Se liga nessa lista de jogadores que vão mudar de time no próximo mês!",
        "A dica de hoje envolve os novos delineadores da linha Rare Beauty",
        "Eu quando acho a chuteira que perdi na última pelada...",
        "Você prefere compartilhar a nossa página agora ou daqui cinco minutos?",
        "A polêmica pesquisa de V. Damasco sobre ciência do comportamente acaba de ser publicada."                
    ]
    
    
    resultado = questao_4(input_id)
    
    assert resultado[:2] == output[:2]


# Questão 5
def questao_5(user_views, user_id):
    
    viewed_ids = set()
    for user in user_views:
        if user["usuario"] == user_id:
            
            viewed_ids = set(str(x) for x in user["visualizado"])
            break

    
    post_keys = redis_conn.keys("post:*")
    user_interests = redis_conn.zrange(f"user:{user_id}:interests", 0, -1, withscores=True)
    interests_dict = {name: score for name, score in user_interests}

    post_scores = []
    for key in post_keys:
        post_data = redis_conn.hgetall(key)
        post_id = post_data["id"]
        
        
        if post_id in viewed_ids:
            continue

        post_keywords = [k.strip() for k in post_data["palavras_chave"].split(",")]
        
        score = 0
        for keyword in post_keywords:
            if keyword in interests_dict:
                score += interests_dict[keyword]
                
        post_scores.append((score, post_data["conteudo"]))

  
    post_scores.sort(key=lambda x: (-x[0], x[1]))
    
    filtered_posts = [post[1] for post in post_scores]
    return filtered_posts

def test_questao_5():
    input_views = [
        {"usuario":1, "visualizado": [345,350,353]},
        {"usuario":2, "visualizado": [350,351]},
        {"usuario":3, "visualizado": [345,351,352,353]}, 
        {"usuario":4, "visualizado": []}
    ]

    
    
    output = [
        "Aprenda uma receita rápida de onion rings super crocantes.",
        "A dica de hoje envolve os novos delineadores da linha Rare Beauty",
        "Eu quando acho a chuteira que perdi na última pelada..."    
    ]

    
    resultado = questao_5(input_views, user_id=3)
    assert resultado[0] == output[0]


if __name__ == "__main__":
    try:
        test_questao_1()
        print("Q1 OK")
        test_questao_2()
        print("Q2 OK")
        test_questao_3()
        print("Q3 OK")
        test_questao_4()
        print("Q4 OK")
        test_questao_5()
        print("Q5 OK")
    except AssertionError as e:
        print(f"Erro de asserção: {e}")
    except Exception as e:
        print(f"Erro: {e}")