import difflib

remove_words = ["remover", "retirar", "tirar", "apagar", "eliminar", "produto", "do", "carrinho", "de", "compras"]

stores = {"pingo Doce": 1, "pingo doce madeira": 2, "pingo doce solmar açores": 3, "mercadão solidário": 4, "saúde": 5, "medicamentos": 6 }

string = "madeira"

string_splt = string.lower().split()

print(difflib.get_close_matches(string, stores, cutoff=0.4))