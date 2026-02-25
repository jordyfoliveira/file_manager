def text_stats(text: str) -> dict:
    """Retorna estatísticas sobre um texto, incluindo o número total de caracteres, caracteres sem espaços, palavras, linhas e vogais."""
    #counting = text.lower()
    #countAletterSpace= counting.count(" ")
    countAletterSpace = 0
    
    #conta o número de espaços em branco no texto, ignorando "\t" e "\n"
    for cSpace in text:
        if cSpace.isspace():
            countAletterSpace += 1
    
    
    countTotalLetter = len(text)
    countTotalLetterNoSpace = len(text) - countAletterSpace
    countTotalWords= len(text.split())
    countTotalLines = len(text.splitlines())
    
    #countTotalVowels = counting.count("a") + counting.count("e") + counting.count("i") + counting.count("o") + counting.count("u") + counting.count("y")
    countTotalVowels = 0
    
    #conta o número de vogais no texto, considerando letras acentuadas e sem acentos, e ignorando maiúsculas e minúsculas
    for char in text.lower():
        if char in "aeiouyáàâãäæéèêëíìïóòôõöœøúùüý":
            countTotalVowels += 1

    
    #StringStat = "char: "+str(countTotalLetter) + "\n" + "char without space: "+str(countTotalLetterNoSpace) + "\n" + "words: " + str(countTotalLettersAfterSpace) + "\n" + "lines: " + str(countTotalLines)  + "\n" + "vowels: " + str(countTotalVowels)
    #return StringStat
    return {
        "char": countTotalLetter,
        "char_without_space": countTotalLetterNoSpace,
        "words": countTotalWords,
        "lines": countTotalLines,
        "vowels": countTotalVowels
    }

if __name__ == "__main__":
    val = text_stats("Olá mundo!\nIsto é Python.")
    print(val)

    #stats = text_stats("abc")
    #print(stats["words"])