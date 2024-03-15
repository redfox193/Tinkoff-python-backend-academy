# Python Package for Hangman Game

## How to play

- Install package in your project using [TestPyPi](https://test.pypi.org/project/hw2-hangman-redfox193/0.1.2/)
(`python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ hw2-hangman-redfox193==0.1.2`)
- Write `from hangman import hangman` to import module
- Then you can start game using function `hangman.hangman_game(secret_word: str, lifes: int)`
- `secret_word` could be obtained using either `hangman.pick_random_word_from_api()` or `hangman.pick_random_word_from_file(filepath: str)`

## Game Rules

- You can only guess one letter at a time.
- The word to guess is randomly selected from a list of words.
- Only latin characters are valid guesses.
- The game ends when you either guess the word or run out of lives.

## How to Customize

You can customize the game by providing game with your set of words!

## Using Docker for playing

- After cloning this project from GitHub, open it and write in terminal to create a Docker Image: `docker build -t <your image name> -f ./docker/Dockerfile.python3.12 .`
- To run Docker Container and play in interactive mode execute `docker run --rm -it <your image name>` (`-it` is neccessary as game could run only in interactive mode)

Enjoy playing Hangman!
