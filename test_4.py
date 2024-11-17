
tokenized_word = '10110'
tokenized_tafeela = '11110'

comp = ''
if len(tokenized_word) < len(tokenized_tafeela):
    l = len(tokenized_tafeela) - len(tokenized_word)
    for i in range(l):
        tokenized_word += '#'

for j in range(len(tokenized_word)):
    if tokenized_word[j] == tokenized_tafeela[j]:
        comp += tokenized_word[j]  # Keep the matching element
    else:
        comp += '#'  # Replace mismatch with '#'

print(comp)