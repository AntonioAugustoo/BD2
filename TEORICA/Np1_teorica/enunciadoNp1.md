# [S202] NP1

Poles gosta muito de jogar RPG de mesa com seus amigos. Ele quer construir um site para gerenciar as informações sobre os diferentes mundos que eles e seus amigos criaram para jogar. Ele precisa de sua ajuda para popular dois bancos de dados para dois subsistemas. 

O primeiro subsistema é uma loja de itens. Nesse sistema os itens podem possuir nome, preço e peso.

O segundo subsistema é um gestor de conhecimentos. Nesse sistema podem existir páginas e personagens. As páginas contém um título e uma descrição. Os personagens podem ter nome, idade, uma lista de habilidade, profissão (Acadêmico, Canalizador, Guerreiro, Ladino ou Caçador), cultura (Eban, Aaron, Eron, Hotan, Marruchi, Ynaia, Uesto, Yuni ou Nomi) e data de criação. Além disso, cada personagem pode conhecer algumas informações descritas pelas páginas. Para cada página cadastrada será informada uma lista de profissões e culturas de personagens que podem conhecer esta página.

Considere os casos de teste e as informações dadas em cada teste para registrar com os dados dos itens, páginas e personagens. Para cada questão um conjuto de dados diferente vai ser usado, contendo a entrada necessária e a saída esperada para resolver cada um dos problemas.

## Configuração

Coloque todos os arquivos em uma mesma pasta.

Crie um ambiente virtual (python 3.11) se achar necessário e execute o seguinte comando para instalar as bibliotecas necessárias:

`pip install -r requirements.txt`

Para executar os testes use o comando:

`pytest s202_np1_base.py`


## Questão 1 (classe ItemDAO)

(20 pontos) Desenvola a função `add_item` para inserir as informações dos itens no MongoDB. 

(10 pontos) Desenvolva a função `get_available_itens` para buscar no Mongo DB os nomes e o preço de todos os itens que um determinado personagem possa pagar e carregar, em ordem do mais barato para o mais caro. Dadas as informações de capacidade de peso que o personagem pode carregar e a quantidade de moedas que ele tem, faça um busca no banco de dados e retorne apenas os itens que tiverem um peso menor do que a quantiade que ele aguenta e um preço menor do que a sua quantidade de moedas. Ordene a lista em ordem decresence de preço (em caso de empate, coloque em ordem descrescente de peso).

## Questão 2 (classes PageDAO e CharacterDAO)

(20 pontos) Desenvolva a função `add_page` para inserir as páginas no Neo4j, incluindo os seus relacionamentos com as diferentes profissões e culturas de personagems que podem conhecer cada página. 

(10 pontos) Desenvola a função `add_character` para inserir as informações de um personahem no Neo4j. Não esqueça de criar um relacionamento entre o personagem e as páginas que ele conhece.

(10 pontos) Desenvolva a função `get_knowledge` que retorna todas as páginas que um determinado personagem conhece.
