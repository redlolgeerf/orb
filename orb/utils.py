import string
from decimal import Decimal
from orb.types import MessageCost, ReportCost
import re


VOWELS = {"a", "e", "i", "o", "u"}
ALPHANUMERIC = set(string.ascii_lowercase + string.digits)

word_pattern = re.compile("([\w'\-]+)")


def split_words(text: str) -> list[str]:
    """
    Split message text into words.
    A “word” is defined as any continual sequence of letters, plus ‘ and -
    """
    return word_pattern.findall(text)


def get_word_cost(word: str) -> Decimal:
    word_length = len(word)
    if word_length >= 8:
        return Decimal("0.3")
    elif word_length >= 4:
        return Decimal("0.2")
    return Decimal("0.1")


def get_vowel_penalty(text: str) -> Decimal:
    """
    Third Vowels: If any third (i.e. 3rd, 6th, 9th) character is an uppercase
    or lowercase vowel (a, e, i, o, u) add 0.3 credits for each occurrence.
    """
    cost = Decimal(0)
    for char in text[2::3]:
        if char.lower() in VOWELS:
            cost += Decimal("0.3")
    return cost


def are_words_unique(words: list[str]) -> bool:
    return len(set(words)) == len(words)


def is_palindrom(text: str) -> bool:
    if not text:
        return False
    clean_text = [char for char in text.lower() if char in ALPHANUMERIC]
    for i in range(len(clean_text) // 2):
        if clean_text[i] != clean_text[-i - 1]:
            return False
    return True


def calculate_message_cost(message: MessageCost, report: ReportCost | None) -> Decimal:
    if report:
        return Decimal(report.credit_cost)
    cost = Decimal(1)
    # add cost for character count
    cost += Decimal("0.05") * len(message.text)
    words = split_words(message.text)
    # add cost for word length
    for word in words:
        cost += get_word_cost(word)
    # add penalty for third vowels, in the brief, it's not clear, whether we
    # should look at words or the whole text, so I would assume that it's the
    # whole text
    cost += get_vowel_penalty(message.text)
    # add penalty for exceeding 100 characters
    if len(message.text) > 100:
        cost += 5
    # add credit for using only unique words
    if are_words_unique(words):
        cost = max(Decimal(1), cost - 2)
    # double the cost if palindrom
    if is_palindrom(message.text):
        cost += cost
    return cost
