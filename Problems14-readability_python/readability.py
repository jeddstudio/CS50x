# TODO

text = input("Text: ")

# letters counter
# using .isupper and .islower to check the string
# if it is a letter, add 1 to counter
letters = 0
for i in text:
    if i.isupper() or i.islower():
        letters += 1
# print(letters)


# word counter
# using .split, it will create a list of text then check the lenght and got the words count
word_list = text.split()
words = len(word_list)
# print(words)

# sentences counter
# counter the ".", "!", "?"
# those are the end of the sentences
sentences = 0
for i in text:
    if i == "." or i == "!" or i == "?":
        sentences += 1
# print(sentences)

# Coleman-Liau Formula
# L = letters / words * 100
l = letters / words * 100

# S = sentences / words * 100
s = sentences / words * 100

# index = 0.0588 * L - 0.296 * S - 15.8
index = (0.0588 * l) - (0.296 * s) - 15.8

# print(f"Index: {index}")

# Coleman-Liau Formula
if index <= 16 and index >= 1:
    # using round() to get the number (4.2=4, 4.5=5)
    print(f"Grade {round(index)}")

elif index < 1:
    index = 1
    print(f"Before Grade {index}")

elif index > 16:
    index = 16
    print("Grade 16+")