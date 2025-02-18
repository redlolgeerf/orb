import pytest
from decimal import Decimal as D
from pytest import param as p
from orb.types import MessageCost, ReportCost
from orb.utils import (
    calculate_message_cost,
    split_words,
    get_vowel_penalty,
    is_palindrom,
)


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        ("", []),
        ("foo", ["foo"]),
        ("foo bar", ["foo", "bar"]),
        ("fo-o bar", ["fo-o", "bar"]),
        ("foo ba'r", ["foo", "ba'r"]),
    ],
)
def test__split_words(input, expected):
    assert split_words(input) == expected


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        ("abc", D("0")),
        ("foo", D("0.3")),
        ("foo bar", D("0.6")),
    ],
)
def test__get_vowel_penalty(input, expected):
    assert get_vowel_penalty(input) == expected


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        ("", False),
        ("foo", False),
        ("aba", True),
        ("abba", True),
        ("ab'a", True),
        ("121", True),
        ("1 21", True),
        ("Aba", True),
    ],
)
def test__is_palindrom(input, expected):
    assert is_palindrom(input) == expected


@pytest.mark.parametrize(
    ("text", "report_cost", "expected"),
    [
        p(
            "foo",
            42,
            42,
            id="if report is present, it takes priority over everything else",
        ),
        p("", None, 1, id="no report or text, just base cost"),
        p("abc", None, 1, id="costs one, because of unique word discount"),
        p(
            "abc abc",
            None,
            1 + D("0.05") * 7 + 2 * D("0.1"),
            id="no vowel penaly, no discount for uniqueness, not a palindrom",
        ),
        p(
            "abc 1 1 cba",
            None,
            (D("1") + D("0.05") * 11 + 4 * D("0.1")) * 2,
            id="no vowel penaly, no discount for uniqueness, a palindrom",
        ),
        p(
            "b" * 50 + " 1" + "b" * 50,
            None,
            (D("1") + D("0.05") * 102 + 2 * D("0.3") - 2 + 5) * 2,
            id="no vowel penaly, no discount for uniqueness, a palindrom, lenght penalty",
        ),
    ],
)
def test__calculate_message_cost(text, report_cost, expected):
    message = MessageCost(id=123, text=text, timestamp="")
    if report_cost:
        report = ReportCost(id=246, name="a report", credit_cost=report_cost)
    else:
        report = None
    assert calculate_message_cost(message, report) == expected
