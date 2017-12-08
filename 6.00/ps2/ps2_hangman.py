# 6.00 Problem Set 3
# 
# Hangman
#


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program
wordlist = load_words()
letters = string.ascii_lowercase
workingletters = list(letters)
guesses = 8
# your code begins here!

# function for updating the guessed word so far.  Replaces '_' with 
# correctly-guessed letters.

def updateguessedword(word, guessedword, guess):
    for i in range(len(word)):
        if guess == word[i]:
            guessedword[i] = guess
    return guessedword

# prints welcome message and initializes values for guessedword and lettersleft

print("Welcome to the game, Hangman!")    
word = choose_word(wordlist)
print("I am thinking of a word that is %s letters long") % (len(word))
guessedword = list("_" * len(word))
lettersleft = len(word)

# loop for player guesses.

while True:    
    print "-" *15

# checks to see if player is out of guesses.

    if guesses == 0:
        print "Sorry, but you are all out of guesses!"
        print "The word was ", word
        break

# checks to see if player has guessed the word.

    if guessedword == list(word):
        print "Congratulations, you won!"
        break

# regular loop if game has not ended begins here:

    print "You have %d guesses left" % (guesses,)
    print "Available letters:", "".join(workingletters)        
    guess = raw_input("Please guess a letter (hit enter to quit): ").lower()
    if len(guess) < 1: break
    if guess not in letters:
        print "That is not a valid entry"
    elif guess not in workingletters:
        print "You already guessed that letter, you big ninny!"
    elif guess in word:
        workingletters.remove(guess)
        guessedword = updateguessedword(word, guessedword, guess)
        print "Good guess: ", " ".join(guessedword)
    else:
        workingletters.remove(guess)
        print "Oops!  That letter is not in my word: ", " ".join(guessedword)
        guesses -= 1
            
