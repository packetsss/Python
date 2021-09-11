# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import random
# game rule
# player turn
# computer turn


def condition(man, pc):
    if (man == "r" and pc == "s") or (man == "p" and pc == "r") or (man == "s" and pc == "p"):
        return True


def play():
    human = input("Please type in \"R\" for rock, \"P\" for paper, \"S\" for Scissors: ").lower()

    while not(human == "r" or human == "p" or human == "s"):
        print("Invalid input, try again.")
        human = input("Please type in \"R\" for rock, \"P\" for paper, \"S\" for Scissors: ").lower()

    computer = random.choice(["r", "p", "s"])

    letter_conv = {
        "r": "Rock",
        "p": "Paper",
        "s": "Scissors",
    }
    print(f"\nComputer chooses {letter_conv.get(computer)}")

    if human == computer:
        print("It's a Tie!")
    elif condition(human, computer):
        print("You win!")
    else:
        print("You Lose!")


continue1 = " "
while continue1 != "n":
    play()
    continue1 = input("\nWanna play again? (Y/N)").lower()
    while continue1 != "y" and continue1 != "n":
        print("Invalid input, try again.")
        continue1 = input("\nWanna play again? (Y/N)").lower()


from PIL import Image

image = Image.open('File.jpg')
image.show()
