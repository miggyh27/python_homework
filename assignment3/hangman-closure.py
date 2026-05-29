# Task 4


def make_hangman(secret_word: str):
    secret = secret_word.strip()
    guesses: list[str] = []

    def hangman_closure(letter: str) -> bool:
        guesses.append(letter)
        masked = "".join(ch if ch in guesses else "_" for ch in secret)
        print(masked)
        return all(ch in guesses for ch in secret)

    return hangman_closure


if __name__ == "__main__":
    while True:
        secret = input("Enter the secret word: ").strip()
        if secret:
            break
        print("Secret word cannot be empty.")

    play = make_hangman(secret)
    while True:
        guess = input("Guess a letter: ").strip()
        if len(guess) != 1:
            print("Please enter a single character.")
            continue
        if play(guess):
            print("You guessed the whole word.")
            break
