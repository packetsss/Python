import random


def guess(num):
    random_number = random.randint(1, num)
    guess = 0
    while guess != random_number:
        guess = int(input(f"Guess a number between 1 and {num}: "))
        print(guess)
        if guess < random_number:
            print("Too low, try again.")
        elif guess > random_number:
            print("Too high, try again.")

    print(f'You got it! Its {random_number}!')


# guess(100)

def computer_guess(num):
    low = 1
    high = num
    feedback = ""
    while feedback != "c":
        if low != high:
            guess = random.randint(low, high)
        else:
            guess = low
        feedback = input(f"Is {guess} too high (H), too low (L), or correct (C)").lower()
        if feedback == "h":
            high = guess - 1
        elif feedback == "l":
            low = guess + 1
    print(f"You got it {guess}")


computer_guess(100)
