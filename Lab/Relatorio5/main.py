from database import Database
from BookModel import BookModel

db = Database(database="Rela5", collection="Livros")
data = db.collection.find()
bookModel = BookModel(db)

#Realizando a insercao de livros

livro = bookModel.create_book("Diario de um Banana", "Jeff Kiney", 2007, 66.70)
livro1 = bookModel.create_book("O Escaravelho do Diabo", " Lúcia Machado de Almeida", 1953, 49.90)
livro2 = bookModel.create_book("Crônicas de gelo e fogo", "George R.R Martin", 1996, 66.90)


#Realizando a leitura dos livros
read_book = bookModel.read_book_by_id(livro)
read_book1 = bookModel.read_book_by_id(livro1)
read_book2 = bookModel.read_book_by_id(livro2)


#atualizacao de dados do livro
updatebook = bookModel.update_book(livro, "Diario de um Banana", 66.90)
updatebook1 = bookModel.update_book(livro2, "Crônicas de gelo e fogo", 75.00)

#Realizando a exclusao de um livro do Bando de Dados
delete_book = bookModel.delete_book(livro1)