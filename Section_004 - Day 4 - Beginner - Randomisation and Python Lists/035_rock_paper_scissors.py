"""
Rock Paper Scissors — Professional CLI Version (ASCII Art)

Features:
- Clean structure with functions
- Clear ASCII art visuals
- Input validation
- Deterministic, readable flow
- Beginner-friendly but professional-grade

Rules:
- Rock beats Scissors
- Scissors beats Paper
- Paper beats Rock
"""

import random


# ASCII art representations stored in a dictionary
ASCII_ART = {
    "rock": """
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
""",
    "paper": """
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
""",
    "scissors": """
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""
}


def get_user_choice():
    """
    Prompts the user for input and validates it.

    Returns:
        str: 'rock', 'paper', or 'scissors'
    """
    while True:
        choice = input("Choose Rock, Paper, or Scissors: ").strip().lower()
        if choice in ASCII_ART:
            return choice
        print("Invalid choice. Please enter Rock, Paper, or Scissors.")


def get_computer_choice():
    """
    Randomly selects a choice for the computer.

    Returns:
        str: 'rock', 'paper', or 'scissors'
    """
    return random.choice(list(ASCII_ART.keys()))


def decide_winner(user, computer):
    """
    Determines the winner based on game rules.

    Returns:
        str: Result message
    """
    if user == computer:
        return "It's a draw."

    winning_conditions = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }

    if winning_conditions[user] == computer:
        return "You win!"
    else:
        return "Computer wins!"


def main():
    """
    Main game controller.
    """
    print("\n=== ROCK PAPER SCISSORS ===\n")

    user_choice = get_user_choice()
    computer_choice = get_computer_choice()

    print("\nYou chose:")
    print(ASCII_ART[user_choice])

    print("Computer chose:")
    print(ASCII_ART[computer_choice])

    result = decide_winner(user_choice, computer_choice)

    print("Result:")
    print(result)


# Program entry point
if __name__ == "__main__":
    main()
