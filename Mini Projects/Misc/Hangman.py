from Hangman_words import words
import random
import string


def valid_word(words):
    word = random.choice(words)
    while "-" in word or " " in word:
        word = random.choice(words)

    return word.upper()


def hangman():
    word = valid_word(words)
    word_letters = set(word)
    alphabet = set(string.ascii_uppercase)
    used_letters = set()

    lives = 10

    while len(word_letters) > 0 and lives > 0:
        print("You have", lives, " left and you have used these letters: ", " ".join(used_letters))

        word_list = [letter if letter in used_letters else "-" for letter in word]
        print("Current word: ", "".join(word_list))

        user_letter = input("Guess a letter: ").upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
                print('')

            else:
                lives = lives - 1

        elif user_letter in used_letters:
            print("You already guessed it.")

        else:
            print("Invalid input")

    if lives == 0:
        print("You died, the word is ", word)
    else:
        print("Congrets!", word)


if __name__ == "__main__":
    hangman()
