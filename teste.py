text = "Olá, olá!"
 
for char in text:
    if char in "áàâãäæ":
        text = text.replace(char, "a")
    elif char in "éèêë":
        text = text.replace(char, "e")
    elif char in "íìï":
        text = text.replace(char, "i")
    elif char in "óòôõöœø":
        text = text.replace(char, "o")
    elif char in "úùü":
        text = text.replace(char, "u")
    elif char in "ý":
        text = text.replace(char, "y")

        
print(text)