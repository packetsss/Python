def trans(phrase):
    translation = ""
    for letter in phrase:
        if letter.lower() in "aeiou":
            if letter.isupper():
                translation = translation + "J"
            else:
                translation = translation + "j"
        else:
            translation = translation + letter
    return translation


print(trans(input("Enter a phrase: ")))
