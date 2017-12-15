from ps3a import *
import time
from perm import *


#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    maxscore = 0
    maxword = ""    
    for n in range(calculate_handlen(hand)):
        perms = get_perms(hand, n)
        for word in perms:
            wordscore = get_word_score(word, HAND_SIZE)
            if wordscore > maxscore:
                if word not in word_list:
                    continue
                else:
                    maxscore = wordscore
                    maxword = word
    return maxword
    # TO DO...

#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    # TO DO ...    
    score = 0    
    while True:    
        print "Current hand:", 
        display_hand(hand)        
        word = comp_choose_word(hand, word_list)
        
        if word == "": break
        # when valid word is entered, it uses up letters from the hand.
        hand = update_hand(hand, word)    
        
        # after every valid word, the score for that word is displayed, the remaining
        # letters in the hand are displayed, and the user is asked to input another word

        wordscore = get_word_score(word, HAND_SIZE)
        score += wordscore        
        print '"%s" earned' % (word,), wordscore, 'points.', 'Total:', score, 'points.'
        print
        if calculate_handlen(hand) == 0: break        
    print "Total score:", score    
#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    # TO DO...
    print 'Welcome to the 6.00 Word Game!'
    hand = deal_hand(HAND_SIZE)    
    while True:
        choice1 = raw_input('Enter "n" for a new hand, "r" to repeat the last hand, or "e" to exit the game: ')
        if choice1 not in ('ren'):
            print 'invalid choice'
            continue
        if choice1 == 'e': break
        while True:
            choice2 = raw_input('Enter "u" to play the hand yourself or "c" to let the computer play the hand: ')        
            if choice2 not in ('uc'):
                print 'invalid choice'
                continue
            else: break                
        if choice1 == 'r':
            if choice2 == 'u': play_hand(hand, word_list)
            else: comp_play_hand(hand, word_list)
        else: 
            hand= deal_hand(HAND_SIZE)            
            if choice2 == 'u': play_hand(hand, word_list)
            else: comp_play_hand(hand, word_list)
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

    
