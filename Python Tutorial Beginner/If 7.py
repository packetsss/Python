is_male = True
is_tall = False

if is_male or is_tall:
    print("Your are a male and tall")
else:
    print("You are not a male or tall")

if is_male and is_tall:
    print("Your are a male and tall")
else:
    print("You are not a male or tall")

if is_male and is_tall:
    print("Your are a male and tall")
elif is_male and not(is_tall):
    print("You are a short male")
elif not(is_male) and is_tall:
    print("You are a tall female")
else:
    print("You are not a male or tall")
