import re


def determine():
    confirm_info = input("Type in \'S\' for sign up and \'L\' for login: ").upper()
    while confirm_info != "S" and confirm_info != "L":
        print("Invalid input")
        confirm_info = input("Type in \'S\' for sign up and \'L\' for login: ").upper()
    if confirm_info == "S":
        return 1


def signup():
    user_name = input("Type in a new username: ")

    with open("User_data.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            while re.search(f"Username: {user_name};", line):
                print("Username already taken, try a new one.")
                user_name = input("Type in a new username: ")

    password = input("Type in a new password: ")

    with open("User_data.txt", "a") as f:
        f.writelines("Username: " + user_name + ";\nPassword: " + password + ".\n\n")

    print("You now have created your account! Please sign in")


def login():
    name = input("Type in your username: ")

    with open("User_data.txt", "r") as f:
        lines = f.readlines()
        user_found = False
        while not user_found:
            for line in lines:
                if re.search(f"Username: {name};", line):
                    user_found = True
                    break
            if not user_found:
                print("No user found, try again.")
                name = input("Type in your username: ")

    pw = input("Type in your password: ")

    # with open("User_data.txt", "r") as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         if re.search(f"Username: {name};", line):
    #             print(line.)

    with open("User_data.txt", "r") as f:
        string = f"Username: {name};"
        line_count = 0
        for line in f:
            line_count += 1
            if string == line.rstrip():  # remove trailing newline
                # print(line_count)
                break

        pas = 1 + line_count
        lines = f.readlines(pas)
        wrong_password = True
        while wrong_password:
            for line in lines:
                if re.search(f"Password: {pw}.", line):
                    wrong_password = False
                    print(f"Welcome {name}!!!")
                    break
            if wrong_password:
                print("Wrong password try again.")
                pw = input("Type in your password: ")


if __name__ == "__main__":
    cond = determine()
    if cond == 1:
        signup()
        login()
    else:
        login()
