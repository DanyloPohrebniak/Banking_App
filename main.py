import re
import database
import security

current_user = None


def get_positive_amount(prompt):
    try:
        amount = float(input(prompt))
        if amount <= 0:
            raise ValueError
        return amount
    except ValueError:
        print("Invalid amount. Must be a positive number.")
        return None


def login_menu():
    global current_user

    print("Welcome to Danylo Banking App!")

    while current_user is None:
        try:
            choice = int(input("\nChoose an action:\n 1. Create Account\n 2. Log In\n 3. Exit\nYour input: "))
        except ValueError:
            print("Invalid input. Enter a number.")
            continue

        if choice == 1:
            print("Account creating:")
            name = input("Enter your name: ")
            if not re.match(r"^[A-Za-z]{3,20}$", name):
                print("Invalid name. Use only letters (3-20 characters).")
                continue

            password = input("Create password: ")

            if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$", password):
                print("Password must be at least 6 characters long and include letters and numbers.")
                continue

            confirm = input("Confirm password: ")

            if password != confirm:
                print("Passwords do not match!")
                continue

            password_hash = security.hash_password(password)
            mfa_code = security.generate_mfa_code()

            if database.add_customer(name, password_hash, mfa_code):
                print(f"Your MFA code is: {mfa_code} (you'll need it to log in)")
                print("Account created successfully.")
            else:
                print("Username already exists.")

        elif choice == 2:
            print("Logging in:")
            user_name = input("Enter your name: ")
            if not re.match(r"^[A-Za-z]{3,20}$", user_name):
                print("Invalid username format.")
                continue

            user = database.get_user_by_name(user_name)
            if not user:
                print("User not found!")
                continue

            user_password = input("Enter password: ")
            mfa_input = input("Enter MFA code: ")

            if not mfa_input.isdigit() or len(mfa_input) != 6:
                print("Invalid MFA code format.")
                continue

            stored_hash = user[3]
            stored_mfa = int(user[4])

            if security.check_password(user_password, stored_hash) and int(mfa_input) == stored_mfa:
                current_user = user
                print(f"Welcome, {user_name}! You are logged in now!")
            else:
                print("Login failed. Wrong password or MFA code.")

        elif choice == 3:
            print("Goodbye!")
            exit()

        else:
            print("Invalid choice. Please select from the menu.")


def user_menu():
    global current_user

    while current_user is not None:
        try:
            choice = int(input("\nChoose an action:\n 1. Check Balance\n 2. Deposit\n 3. Withdraw\n 4. Log Out\n 5. Exit\nYour input: "))
        except ValueError:
            print("Invalid input. Enter a number.")
            continue

        if choice == 1:
            print("Check Balance")
            user_balance = round(database.get_user_balance_by_id(current_user[0]), 2)
            print(f"Your balance is {user_balance}€")

        elif choice == 2:
            print("Deposit Money")
            amount = get_positive_amount("Enter amount you want to deposit: ")
            if amount is None:
                continue

            current_balance = database.get_user_balance_by_id(current_user[0])
            database.update_balance(current_user[0], current_balance + amount)
            print(f"Deposited {amount}€. New balance: {round(database.get_user_balance_by_id(current_user[0]), 2)}€")

        elif choice == 3:
            print("Withdraw Money")
            current_balance = database.get_user_balance_by_id(current_user[0])
            amount = get_positive_amount("Enter amount you want to withdraw: ")
            if amount is None:
                continue
            if amount > current_balance:
                print("Insufficient funds.")
            else:
                database.update_balance(current_user[0], current_balance - amount)
                print(f"Withdrawn {amount}€. New balance: {round(database.get_user_balance_by_id(current_user[0]), 2)}€")

        elif choice == 4:
            print("Logging out...")
            current_user = None
            break

        elif choice == 5:
            print("Goodbye!")
            exit()

        else:
            print("Invalid choice. Please try again.")


# === Main Cycle ===
if __name__ == '__main__':
    while True:
        login_menu()
        user_menu()
