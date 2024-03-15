import random
from datetime import datetime, timedelta
from typing import Callable, Tuple
from pathlib import Path

import httpx

UNGUESSED_LETTER = '_'
WORDGEN_API_URL = 'https://random-word-api.herokuapp.com/word'

def is_time_out(start_time: datetime, time_limit: timedelta) -> bool:
    """
    Check if a specified duration has elapsed since a given start time.

    :param start_time: The start time as a datetime object.
    :param current_time: The current time as a datetime object.
    :param time_limit: The duration in seconds to compare against.
    :return: True if the duration has elapsed, False otherwise.
    """
    elapsed_time = datetime.now() - start_time
    return elapsed_time >= time_limit


def pick_random_word_from_file(rel_filepath: str, rand: random.Random = random.Random()) -> str:
    """
    Pick a random word from a file and returns it.

    :param rel_filepath: Relative path to the file containing words.
    :return: A randomly selected word from the file.
    """
    words_list = Path(rel_filepath).read_text(encoding='utf-8').splitlines()
    word_num = rand.randint(0, len(words_list) - 1)  # noqa: S311
    return words_list[word_num]


def pick_random_word_from_api() -> Tuple[str, str]:
    """
    Pick a random word using wordgen API and return it.

    :return: A randomly selected word using the API with a status message. If an error was occured, return empty word
    """
    response = httpx.get(WORDGEN_API_URL)
    word = response.json()[0] if response.status_code == httpx.codes.OK else ''
    return (word, response.status_code)


def guess_letter(letter: str, s_word: str, g_word: str) -> Tuple[str, bool]:
    """
    Guess a letter in the secret word and updates the guessed word.

    :param letter: The letter to guess.
    :param s_word: The secret word.
    :param g_word: The currently guessed word.
    :return: A tuple containing the updated guessed word and a boolean indicating if the guess was correct.
    """
    letter = letter.lower()
    if letter not in s_word:
        return (g_word, False)
    new_g_word = ''
    for s_letter, g_letter in zip(s_word, g_word):  # Constract new guessed word, revealing guessed letter
        if s_letter == letter:
            new_g_word += s_letter
        else:
            new_g_word += g_letter
    return (new_g_word, True)


def is_valid_letter(letter: str, u_letters: set[str]) -> Tuple[bool, str]:
    """
    Check if a letter is a valid input for the game.

    The function checks if the letter meets the following criteria:
    1. It is a single character.
    2. It is a Latin character.
    3. It has not been used before in the game.

    :param letter: The letter to validate.
    :param u_letters: A set containing letters that have already been used.
    :return: True if the letter is valid, False with a message otherwise.
    """
    if len(letter) > 1:
        return (False, 'letter must be a single character!')
    elif not letter.isalpha():
        return (False, 'letter must be a latin character!')
    elif letter in u_letters:
        return (False, 'letter was already used!')
    return (True, '')


def hangman_game(secret_word: str, inputf: Callable[[str], str], printf: Callable[[str], object],
                  lives: int = 10, 
                  time_limit: timedelta = timedelta(seconds=60)):
    """
    Play a game of Hangman.

    :param secret_word: The word to be guessed by the player.
    :type secret_word: str
    :param lives: The number of lives the player has to guess the word.
    :type lives: int

    This function allows the player to play a game of Hangman, where they must guess
    the letters of the secret word before running out of lives.
    The game continues until the player guesses the word or runs out of lives.

    The function provides feedback to the player on the current state of the word,
    remaining lives, and whether they have won or lost the game.

    Example:
        hangman_game("apple", 6)

        This will start a game of Hangman with the word "apple" and 6 lives.
    """
    if not len(secret_word):
        printf('Incorrect secret word')
        return
    
    start_time = datetime.now()
    used_letters: set[str] = set()
    guessed_word = UNGUESSED_LETTER * len(secret_word)
    printf('Welcome to Hangman! You have {0} lifes to guess, go!'.format(lives))
    while lives > 0:
        letter = inputf('{0}, {1} lives, guess a character: '.format(guessed_word, lives))
        
        if is_time_out(start_time, time_limit):
            printf('Run out of time... word: {0}'.format(secret_word))
            return
        
        is_valid, message = is_valid_letter(letter, used_letters)
        if is_valid:
            guessed_word, ok = guess_letter(letter, secret_word, guessed_word)
            used_letters.add(letter.lower())
            if not ok:
                lives -= 1
        else:
            printf(message)

        if UNGUESSED_LETTER not in guessed_word:
            break

    if lives > 0:
        printf("{0} You've won!".format(guessed_word))
    else:
        printf('0 lives, game over. word: {0}'.format(secret_word))


if __name__ == '__main__':
    secret_word, status_code = pick_random_word_from_api()
    hangman_game(secret_word, input, print)