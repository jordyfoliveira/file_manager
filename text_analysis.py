import unicodedata
import string

def top_words(text: str, n: int = 5) -> list[tuple[str, int]]:
    """Retorna as n palavras mais comuns em um texto, junto com suas contagens.

    Args:
        text: O texto a ser analisado.
        n: O número de palavras mais comuns a retornar. Padrão é 5."""
        
    #Normaliza o texto para minúsculas e remove acentos para garantir que palavras como "Olá" e "olá" sejam tratadas como a mesma palavra.
    textCaseSens = text.lower()
    #normalizedText = text.lower()
        
    #Substitui as letras acentuadas por suas equivalentes sem acentos para garantir que palavras como "olá" e "ola" sejam tratadas como a mesma palavra.
    normalizedText = unicodedata.normalize('NFKD', textCaseSens).encode('ascii', 'ignore').decode('utf8') #Remove os acentos do texto usando a normalização Unicode e a codificação ASCII, ignorando os caracteres que não podem ser convertidos para ASCII.
    #for char in normalizedText:
    #    if char in "áàâãäæ":
    #        normalizedText = normalizedText.replace(char, "a")
    #    elif char in "éèêë":
    #        normalizedText = normalizedText.replace(char, "e")
    #    elif char in "íìï":
    #        normalizedText = normalizedText.replace(char, "i")
    #    elif char in "óòôõöœø":
    #        normalizedText = normalizedText.replace(char, "o")
    #    elif char in "úùü":
    #        normalizedText = normalizedText.replace(char, "u")
    #    elif char in "ý":
    #        normalizedText = normalizedText.replace(char, "y")
        
    #Separa o texto em palavras, removendo pontuação e contando a frequência de cada palavra, ignorando diferenças de maiúsculas e minúsculas e acentos.
    table = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #Cria uma tabela de tradução que mapeia cada caractere de pontuação para um espaço, usando a função maketrans do módulo string. Isso é necessário para garantir que as palavras sejam separadas corretamente, mesmo quando estão seguidas por pontuação. Por exemplo, "olá!" e "olá" serão tratadas como a mesma palavra "olá" após a tradução, permitindo uma contagem precisa das palavras.
    cleanText = normalizedText.translate(table) #Remove a pontuação do texto usando a tabela de tradução criada anteriormente, substituindo cada caractere de pontuação por um espaço. Isso é necessário para garantir que as palavras sejam separadas corretamente, mesmo quando estão seguidas por pontuação. Por exemplo, "olá!" e "olá" serão tratadas como a mesma palavra "olá" após a tradução, permitindo uma contagem precisa das palavras.
    words = cleanText.split()
    #punct = ".,!?;:<>()[]{}\"'-@#$%^&*~`" #Lista de caracteres de pontuação a serem removidos das palavras
    repeatedWords = {} 
            
    for wordCount in words:
        #for char in punct:
        #    wordCount = wordCount.replace(char, " ") #Remove a pontuação das palavras usando a função replace para substituir cada caractere de pontuação por uma string vazia.
        #wordCount = wordCount.strip(punct) #Remove a pontuação das palavras usando a função strip para remover os caracteres de pontuação do início e do fim de cada palavra.
        #if wordCount in repeatedWords:
        #    repeatedWords[wordCount]  += 1 #Incrementa a contagem da palavra se ela já estiver no dicionário
        #else:
        #    repeatedWords[wordCount] = 1 #Adiciona a palavra ao dicionário com contagem 1 se ela não estiver presente
        repeatedWords[wordCount] = repeatedWords.get(wordCount, 0) + 1 #Usa o método get do dicionário para obter a contagem atual da palavra, retornando 0 se a palavra não estiver presente, e incrementa essa contagem em 1. Isso é uma forma mais concisa de contar a frequência das palavras, evitando a necessidade de verificar explicitamente se a palavra já está no dicionário.
        
    #topWords = sorted(repeatedWords.items(), key=lambda item:item[1], reverse=True) #Ordena as palavras por contagem em ordem decrescente
    topWords = sorted(repeatedWords.items(), key=lambda item: (-item[1], item[0])) #Ordena as palavras por contagem em ordem decrescente e, em caso de empate, ordena alfabeticamente
    
    #topWordsFormat = ""
    #for i, (word, count) in enumerate(topWords[:n], start=1): #Itera sobre as n palavras mais comuns e suas contagens, usando a função enumerate para obter o índice de cada palavra (começando em 1) e formatando cada palavra e sua contagem em uma linha da string formatada. Isso é necessário para apresentar os resultados de forma clara e organizada, permitindo que o usuário veja facilmente quais são as palavras mais comuns e quantas vezes elas aparecem no texto.
    #    topWordsFormat += f"{i}. {word} -> {count}\n" #Adiciona cada palavra e sua contagem à string formatada, numerando-as de 1 a n.
    
    #return topWordsFormat #Retorna a string formatada contendo as n palavras mais comuns e suas contagens, pronta para ser exibida ao usuário. A string inclui uma linha de título indicando o número de palavras listadas, seguida por cada palavra e sua contagem em linhas separadas, numeradas de 1 a n.
    return topWords[:n] #Retorna as n palavras mais comuns como uma lista de tuplas (palavra, contagem)

#text = "Olá, olá! Mundo, mundo... Código é divertido? Código é incrível!"
#text = "b a b a c c c"
#text = "a a a ---"
#text = "ola!!!ola"
#text = input("Introduza o texto: ")

def top_words_format(text: str, n: int = 5) -> str:
    """Retorna as n palavras mais comuns em um texto, junto com suas contagens, formatadas como uma string.

    Args:
        text: O texto a ser analisado.
        n: O número de palavras mais comuns a retornar. Padrão é 5."""
    
    topWords = top_words(text, n) #Chama a função top_words para obter as n palavras mais comuns e suas contagens a partir do texto fornecido, e armazena o resultado na variável topWords.
    
    topWordsFormat = f"Top {n} palavras mais comuns:\n" #Inicializa uma string formatada com um título indicando o número de palavras listadas, para apresentar os resultados de forma clara e organizada.
    for i, (word, count) in enumerate(topWords, start=1): #Itera sobre as n palavras mais comuns e suas contagens, usando a função enumerate para obter o índice de cada palavra (começando em 1) e formatando cada palavra e sua contagem em uma linha da string formatada. Isso é necessário para apresentar os resultados de forma clara e organizada, permitindo que o usuário veja facilmente quais são as palavras mais comuns e quantas vezes elas aparecem no texto.
        topWordsFormat += f"{i}. {word} -> {count}\n" #Adiciona cada palavra e sua contagem à string formatada, numerando-as de 1 a n.
    
    return topWordsFormat #Retorna a string formatada contendo as n palavras mais comuns e suas contagens, pronta para ser exibida ao usuário. A string inclui uma linha de título indicando o número de palavras listadas, seguida por cada palavra e sua contagem em linhas separadas, numeradas de 1 a n.

if __name__ == "__main__": #Verifica se o script está sendo executado diretamente (em vez de importado como um módulo) e, se for o caso, executa o código dentro do bloco if. Isso é uma prática comum em Python para permitir que um arquivo seja usado tanto como um script executável quanto como um módulo importável.
    print("Introduza o texto (linha vazia para terminar):")

    #Lê várias linhas de entrada do usuário até que uma linha vazia seja inserida, armazenando cada linha em uma lista. Em seguida, junta as linhas em um único texto usando a função join, separando-as por quebras de linha. Isso permite que o usuário insira um texto multilinha para análise.
    lines = [] 
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    #Junta as linhas de texto em um único string, separando-as por quebras de linha, para criar o texto completo a ser analisado pela função top_words.
    text = "\n".join(lines)
    
    #Verifica se o texto fornecido não está vazio (após remover espaços em branco) e, se não estiver, chama a função top_words_format para obter as 10 palavras mais comuns e suas contagens, imprimindo o resultado formatado. Caso contrário, imprime uma mensagem indicando que nenhum texto foi fornecido.
    if text.strip():
        print(top_words_format(text, 10))
    else:
        print("Nenhum texto fornecido.")