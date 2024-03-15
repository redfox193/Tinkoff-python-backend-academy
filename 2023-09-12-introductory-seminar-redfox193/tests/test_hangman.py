import os
from unittest.mock import patch

from src.hangman.hangman import (
    guess_letter,
    hangman_game,
    is_valid_letter,
    pick_random_word,
)


def test_pick_random_word():
    with open('test_words.txt', 'w', encoding='utf-8') as test_file:
        test_file.write('apple\nbanana\ncherry')
    word = pick_random_word('test_words.txt')
    os.remove('test_words.txt')
    assert word in {'apple', 'banana', 'cherry'}


def test_guess_letter():
    assert guess_letter('a', 'apple', '_____') == ('a____', True)
    assert guess_letter('p', 'apple', 'a____') == ('app__', True)
    assert guess_letter('x', 'apple', 'a____') == ('a____', False)


def test_is_valid_letter():
    used_letters: set[str] = set()
    assert is_valid_letter('a', used_letters) is True
    assert is_valid_letter('1', used_letters) is False
    assert is_valid_letter('aa', used_letters) is False
    assert is_valid_letter('a', {'a', 'b', 'c'}) is False


def test_hangman_game_wins(capfd):
    with patch('builtins.input', side_effect=['a', 'P', 'l', 'E']):
        hangman_game('apple', 6)
        captured = capfd.readouterr()
        assert "You've won!" in captured.out


def test_hangman_game_loses(capfd):
    with patch('builtins.input', side_effect=['a', 'a', 'x', 'y', 'z']):
        hangman_game('apple', 3)
        captured = capfd.readouterr()
        assert '0 lives, game over. word: apple' in captured.out
