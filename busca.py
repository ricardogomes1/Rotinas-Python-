# A variavel livros tem que ter as informaçoes da busca e o resultado que vc quer exibir, nesse caso vai ser livros
livros = {"Duna":" Livro: Duna\n Autor: Frank Herbert", "Shikasta":" Livro: Shikasta\n Autora: Doris Lessing", "A Coisa":" Livro: A Coisa\n Autor: Stephen King", "Dracula":" Livro: Dracula\n Autor: Bram Stoker"}
denovo = "Sim"
while denovo == "Sim":
  print "BUSCA DE LIVROS\n"
# aqui é onde vc escreve o que quer procurar, para poder ser achado tem que coincidir com o
#que esta escrito na variavel livro, inclusive minuscula e maiscula
  busca = raw_input("Livro: ")
  print "\nRESULTADO\n"
# o resultado vai ser as informaçoes da variavel livros
  if livros.has_key(busca):
    print livros[busca]
  elif busca != livros:
    print "Nao tenho esse livro\n"
# o programa pergunta se vc quer fazer uma nova busca ;)
  denovo = raw_input("Nova Busca?(Sim/Nao): ")
print "FIM"