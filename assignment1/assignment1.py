from __future__ import annotations

from typing import Any, Literal


# Task 1


def hello() -> str:
    return "Hello!"


# Task 2


def greet(name: str) -> str:
    return f"Hello, {name}!"


# Task 3


def calc(
    a: Any,
    b: Any,
    operation: Literal[
        "add",
        "subtract",
        "multiply",
        "divide",
        "modulo",
        "int_divide",
        "power",
    ] = "multiply",
) -> Any:
    try:
        match operation:
            case "add":
                return a + b
            case "subtract":
                return a - b
            case "multiply":
                return a * b
            case "divide":
                return a / b
            case "modulo":
                return a % b
            case "int_divide":
                return a // b
            case "power":
                return a**b
            case _:
                raise ValueError(operation)
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"


# Task 4


def data_type_conversion(value: Any, target: Literal["float", "str", "int"]) -> Any:
    match target:
        case "float":
            converter = float
        case "str":
            converter = str
        case "int":
            converter = int
        case _:
            raise TypeError(target)

    try:
        return converter(value)
    except (ValueError, TypeError):
        return f"You can't convert {value} into a {target}."


# Task 5


def grade(*args: Any) -> str:
    try:
        average = sum(args) / len(args)
    except (TypeError, ZeroDivisionError):
        return "Invalid data was provided."

    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


# Task 6


def repeat(text: str, count: int) -> str:
    parts: list[str] = []
    for _ in range(count):
        parts.append(text)
    return "".join(parts)


# Task 7


def student_scores(
    mode: Literal["best", "mean"],
    **kwargs: int | float,
) -> str | float:
    if not kwargs:
        raise ValueError("no scores")

    if mode == "mean":
        return sum(kwargs.values()) / len(kwargs)
    if mode == "best":
        return max(kwargs, key=kwargs.__getitem__)
    raise ValueError("mode must be best or mean")


# Task 8


_SMALL_WORDS = frozenset({"a", "on", "an", "the", "of", "and", "is", "in"})


def titleize(text: str) -> str:
    words = text.split()
    if not words:
        return ""

    out: list[str] = []
    last_i = len(words) - 1
    for i, word in enumerate(words):
        if i in (0, last_i) or word not in _SMALL_WORDS:
            out.append(word.capitalize())
        else:
            out.append(word)
    return " ".join(out)


# Task 9


def hangman(secret: str, guess: str) -> str:
    guessed = frozenset(guess)
    return "".join(ch if ch in guessed else "_" for ch in secret)


# Task 10


_VOWELS = frozenset("aeiou")


def _consonant_prefix_len(word: str) -> int:
    i = 0
    while i < len(word):
        c = word[i]
        if c in _VOWELS:
            if c == "u" and i > 0 and word[i - 1] == "q":
                i += 1
                continue
            return i
        i += 1
    return len(word)


def _pig_word(word: str) -> str:
    if not word:
        return word
    k = _consonant_prefix_len(word)
    if k == 0:
        return f"{word}ay"
    return f"{word[k:]}{word[:k]}ay"


def pig_latin(sentence: str) -> str:
    return " ".join(_pig_word(w) for w in sentence.split())


if __name__ == "__main__":
    print(hello())
    print(greet("World"))
    print(calc(3, 4, "add"))
    print(data_type_conversion("3.14", "float"))
    print(grade(90, 80, 70))
    print(repeat("ha", 3))
    print(student_scores("mean", Ada=100, Grace=95))
    print(student_scores("best", Ada=100, Grace=95))
    print(titleize("the lord of the rings"))
    print(hangman("python", "yo"))
    print(pig_latin("hello world"))
