import os
import random
from typing import Tuple

UNGUESSED_LETTER = '_'


def pick_random_word(rel_filepath: str) -> str:
    """
    Pick a random word from a file and returns it.

    :param rel_filepath: Relative path to the file containing words.
    :return: A randomly selected word from the file.
    """
    with open(rel_filepath, encoding='utf-8') as words_file:
        words_list = words_file.read().splitlines()
    word_num = random.randint(0, len(words_list) - 1)  # noqa: S311
    return words_list[word_num]


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


def is_valid_letter(letter: str, u_letters: set[str]) -> bool:
    """
    Check if a letter is a valid input for the game.

    The function checks if the letter meets the following criteria:
    1. It is a single character.
    2. It is a Latin character.
    3. It has not been used before in the game.

    :param letter: The letter to validate.
    :param u_letters: A set containing letters that have already been used.
    :return: True if the letter is valid, False otherwise.
    """
    if len(letter) > 1:
        print('letter must be a single character!')  # noqa: WPS421
        return False
    elif not letter.isalpha():
        print('letter must be a latin character!')  # noqa: WPS421
        return False
    elif letter in u_letters:
        print('letter was already used!')  # noqa: WPS421
        return False
    return True


def hangman_game(secret_word: str, lives: int):
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
    used_letters: set[str] = set()
    guessed_word = UNGUESSED_LETTER * len(secret_word)
    print('Welcome to Hangman! You have {0} lifes to guess, go!'.format(lives))  # noqa: WPS421
    while lives > 0:
        letter = input('{0}, {1} lives, guess a character: '.format(guessed_word, lives))  # noqa: WPS421
        if is_valid_letter(letter, used_letters):
            guessed_word, ok = guess_letter(letter, secret_word, guessed_word)
            used_letters.add(letter.lower())
            if not ok:
                lives -= 1
        if UNGUESSED_LETTER not in guessed_word:
            break
    if lives > 0:
        print(guessed_word, "You've won!")  # noqa: WPS421
    else:
        print('0 lives, game over. word:', secret_word)  # noqa: WPS421


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)

    hangman_game(pick_random_word('words.txt'), 10)
