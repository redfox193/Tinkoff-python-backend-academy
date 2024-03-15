import datetime
import json
import os
import random
from pathlib import Path

import httpx
import pytest

from src.hangman.hangman import (
    WORDGEN_API_URL,
    guess_letter,
    hangman_game,
    is_time_out,
    is_valid_letter,
    pick_random_word_from_api,
    pick_random_word_from_file,
)

EXPECTED_PY_VERSION = '3.12.0rc2'

class FkInput(object):
    def __init__(self, return_values: list[str]):
        self._return_values = return_values
        self._shift = 0

    def __call__(self, text: str):
        value = self._return_values [self._shift]
        self._shift += 1 
        return value


class FkPrint(object):
    def __init__(self) -> None:
        self.container: list[str] = []

    def __call__(self, text: str):
        self.container.append(text)


@pytest.fixture()
def mock_word_get_request_success(respx_mock):
    respx_mock.get(WORDGEN_API_URL).mock(return_value = httpx.Response(200, text=json.dumps(['apple'])))


@pytest.fixture()
def mock_word_get_request_fail(respx_mock):
    respx_mock.get(WORDGEN_API_URL).mock(return_value = httpx.Response(400))


@pytest.mark.parametrize(('words', 'seed'), [
    (['apple', 'banana', 'cherry'], 1),
    (['phone', 'pc', 'laptop', 'tv'], 42)
])
def test_pick_random_word_from_file(words: list[str], seed: int):
    word = words[random.Random(seed).randint(0, len(words) - 1)]
    Path('test_words.txt').write_text('\n'.join(words))
    chosen_word = pick_random_word_from_file('test_words.txt', random.Random(seed))
    os.remove('test_words.txt')
    assert word == chosen_word


@pytest.mark.timeout(60)
def test_pick_random_word_from_api_success(mock_word_get_request_success):
    word, status_code = pick_random_word_from_api()
    assert word == 'apple'
    assert status_code == 200


@pytest.mark.timeout(60)
def test_pick_random_word_from_api_failure(mock_word_get_request_fail):
    word, status_code = pick_random_word_from_api()
    assert word == ''
    assert status_code == 400


@pytest.mark.parametrize(('letter', 'secret_word', 'guessed_word', 'new_guessed_word', 'was_guessed'), [
    ('a', 'apple', '_____', 'a____', True),
    ('p', 'apple', 'a____', 'app__', True),
    ('x', 'apple', 'a____', 'a____', False)
])
def test_guess_letter(letter: str, secret_word: str, guessed_word: str, new_guessed_word: str, was_guessed: bool):
    assert guess_letter(letter, secret_word, guessed_word) == (new_guessed_word, was_guessed)


@pytest.mark.parametrize(('letter', 'used_letters', 'valid', 'error_message'), [
    ('a', {},  True, ''),
    ('1', {},  False, 'letter must be a latin character!'),
    ('aa', {},  False, 'letter must be a single character!'),
    ('a', {'a', 'b', 'c'},  False, 'letter was already used!'),
])
def test_is_valid_letter(letter: str, used_letters: set, valid: bool, error_message: str):
    result, message = is_valid_letter(letter, used_letters)
    assert result is valid
    assert message == error_message


@pytest.mark.parametrize(('secret_word', 'input_list', 'end_message', 'lives'), [
    ('', ['a', 'a', 'x', 'y', 'z'],  'Incorrect secret word', 10),
    ('apple', ['a', 'a', 'x', 'y', 'z'],  '0 lives, game over. word: apple', 1),
    ('apple', ['a', 'P', 'l', 'E'],  "apple You've won!", 1),
])
def test_hangman_game(secret_word: str, input_list: list[str], end_message: str, lives: int):
    fk_output = FkPrint()
    fk_input = FkInput(input_list)
    hangman_game(secret_word, fk_input, fk_output, lives)
    assert end_message == fk_output.container[-1]


@pytest.mark.parametrize(('start_time', 'end_time', 'duration', 'out'), [
    ("2023-10-09", "2023-10-23", datetime.timedelta(days=10), True),
    ("2023-10-09 12:00:30", "2023-10-09 12:29:59", datetime.timedelta(minutes=30), False)
])
def test_is_time_out(freezer, start_time: str, end_time: str, duration: datetime.timedelta, out: bool):
    freezer.move_to(start_time)
    start_time = datetime.datetime.now()
    freezer.move_to(end_time)
    assert is_time_out(start_time, duration) is out