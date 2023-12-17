"""Banking app:
- Checking Balances
- Depositing Money
- Withdrawing Money
- Confirmation Prompts"""

import random
import string
import json


def load_customer_data():
    """Load customer information from a file"""
    try:
        with open("customer_data.json", "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        # Generate demo list of userIDs, pin codes, and balances
        user_ids = [generate_user_id() for _ in range(20)]
        pin_numbers = [generate_pin_numbers() for _ in range(20)]
        balances = [generate_balance() for _ in range(20)]
        data = {"user_ids": user_ids, "pin_numbers": pin_numbers, "balances": balances}

        # Save demo list to the file
        save_customer_data(user_ids, pin_numbers, balances)

        return data


def save_customer_data(user_ids, pin_numbers, balances):
    """Save customer information to a file"""
    data = {"user_ids": user_ids, "pin_numbers": pin_numbers, "balances": balances}
    with open("customer_data.json", "w") as file:
        json.dump(data, file)


def generate_user_id():
    """Generates User IDs for each customer"""
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=5))
    user_id = letters + numbers
    return user_id


def generate_pin_numbers():
    """Generates pin codes for each customer"""
    pin_number = ''.join(random.choices(string.digits, k=4))
    return pin_number


def generate_balance():
    """Generates initial balances for each customer"""
    balance = round(random.uniform(10.00, 9999.00), 2)
    return balance


def customer_options():
    """Present users with banking options on a loop until they request to sign out"""
    while True:
        try:
            choice = int(input("\nWhat would you like to do?\nEnter 1 to check your balance\nEnter 2 to deposit money\n"
                               "Enter 3 to withdraw money\nEnter 4 to sign out\n"))
            if choice not in [1, 2, 3, 4]:
                print("Please enter 1, 2, 3, or 4")
            elif choice == 1:
                print(f"Your balance is £{balances[id_index]:.2f}")
            elif choice == 2:
                while True:
                    try:
                        deposit = float(input("How much would you like to deposit?\n£"))
                        if deposit != round(deposit, 2):
                            print("Please enter a value with 2 decimal places.")
                        else:
                            balances[id_index] += deposit  # Update the balance in the balances list
                            print(
                                f"Your deposit of £{deposit:.2f} has been received. Your balance is now "
                                f"£{balances[id_index]:.2f}")
                            break
                    except ValueError:
                        print("You have entered an invalid amount. Please enter a numeric value.")
            elif choice == 3:
                while True:
                    try:
                        withdrawal = float(input("How much money would you like to withdraw?\n£"))
                        if withdrawal != round(withdrawal, 2):
                            print("Please enter a value with 2 decimal places.")
                        elif balances[id_index] - withdrawal < 0:
                            while True:
                                overdraft = input(
                                    "This will take your account into overdraft. Would you like to proceed? [Y/N]\n")
                                if overdraft.upper() not in ["Y", "N"]:
                                    print("Please enter Y or N to proceed")
                                elif overdraft.upper() == "Y":
                                    balances[id_index] -= withdrawal
                                    print(
                                        f"Your withdrawal of £{withdrawal:.2f} has been confirmed. Your balance is now "
                                        f"£{balances[id_index]:.2f}")
                                    break
                                elif overdraft.upper() == "N":
                                    break
                        else:
                            balances[id_index] -= withdrawal
                            print(
                                f"Your withdrawal of £{withdrawal:.2f} has been confirmed. Your balance is now "
                                f"£{balances[id_index]:.2f}")
                            break
                    except ValueError:
                        print("You have entered an invalid amount.")
            elif choice == 4:
                print("Thank you for using SafeBank.")
                break
        except ValueError:
            print("You have entered an invalid value")


# Generate demo list of userIDs, pin codes and balances or load from a file

customer_data = load_customer_data()
user_ids = customer_data["user_ids"]
pin_numbers = customer_data["pin_numbers"]
balances = customer_data["balances"]


print("Welcome to SafeBank Banking App!")

'''Security checks with ability to create an account if UserID doesn't exist. Program ends if incorrect pin is 
entered 3 times'''

while True:
    user_id = input("Please enter your User ID: ")

    if user_id in user_ids:
        print("Thank you.")
        attempts = 3
        while attempts >= 1:
            try:
                pin = input("Please enter your 4-digit pin:\n")
                id_index = user_ids.index(user_id)
                if pin == pin_numbers[id_index]:
                    print(f"Thank you. You have cleared the security checks.")
                    break
                else:
                    attempts -= 1
                    print(f"Incorrect pin. You have {attempts} attempts to try again.")
            except ValueError:
                print("Please enter a 4-digit number.")
        if attempts == 0:
            break
        customer_options()
        save_customer_data(user_ids, pin_numbers, balances)  # Save customer data for when the program is run again
        break
    else:
        print("UserID doesn't exist.")
        try_again = input(
            "If you're a current customer, please press 1 to try again. If you're a new customer, please press 2.\n")
        if try_again == "1":
            continue
        elif try_again == "2":
            new_customer_id = generate_user_id()
            user_ids.append(new_customer_id)
            new_customer_pin = generate_pin_numbers()
            pin_numbers.append(new_customer_pin)
            id_index = user_ids.index(new_customer_id)
            print(
                f"Your UserID is {new_customer_id} and your pin number is {new_customer_pin}. Please keep these "
                f"details safe.")

            # Use the existing balance or ask the user for an initial deposit
            initial_balance = float(
                input("How much money would you like to deposit into your account? £")) if balances else 0.0
            balances.append(initial_balance)

            customer_options()
            save_customer_data(user_ids, pin_numbers, balances)  # Save customer data after a new customer is added
            break
        else:
            print("Please enter 1 or 2.")
