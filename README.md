# Dutch21

Welcome to Dutch-21!

This project is made by Jazz Kargin for a technical assignment.
It is the game called "21", similar to Blackjack. It is a game where players try to win against the Bank individually.

I have implemented the game in Python on Ubuntu operating system. Then I tested on Windows 8 and it works fine.
It can be played with any number of players through the command line interface.

The program is implemented and tested in Python 2.7.12. That is needed to run the program.
You can download it here: 
https://www.python.org/downloads/release/python-2712/

After unziping, go under source and you can run the game via command:

> python twentyone.py

Then the user interface gives clear instructions and information about how you play the game.

For unit testing, I used pytest. That is listed in the requirements.txt. You can install via command:

> pip install -r requirements.txt

When you go under test directory, you can run tests via command:

> pytest -s test.py

The code is organized as one file per class and one file for the main which contains the user interaction.

Enjoy playing!
