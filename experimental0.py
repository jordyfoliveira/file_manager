#texto1 = "Olá mundo!"
#texto2 = "Isto é Python."
texto = "Olá mundo!\nIsto é Python."

counting = texto.lower()
countAletter= counting.count(" ")
countTotalLetter = len(texto)
countTotalLetterNoSpace = len(texto) - countAletter
countTotalLettersAfterSpace= len(texto.split())
countTotalLines = len(texto.splitlines())

#print(texto1 + "\n" + texto2)
print(texto)

print("char: "+str(countTotalLetter) + "\n" + "char without space: "+str(countTotalLetterNoSpace) + "\n" + "words: " + str(countTotalLettersAfterSpace) + "\n" + "lines: " + str(countTotalLines))