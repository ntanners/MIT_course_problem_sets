# 6.00 Problem Set 4
#
# Caesar Cipher Skeleton
#
import string
import random

WORDLIST_FILENAME = "words.txt"

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
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
    wordlist = line.split()
    print "  ", len(wordlist), "words loaded."
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words  
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scramble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
def build_coder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: -27 < int < 27
    returns: dict

    Example:
    >>> build_coder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)
    """
    ### TODO.
    
    # Checks to see if shift is within the proper range.
    assert shift > -27 and shift < 27, 'shift value %s is not between -27 and 27' % (shift,)
    
    # Checks to see if shift is an integer.    
    try: int(shift)
    except: assert False, 'shift value is not an integer'
    
    coder = {}    
    
    # Creates separate lists of lowercase and uppercase letters so that each group loops back onto itself
    
    lowercase_and_space = string.ascii_lowercase + ' '
    uppercase_and_space = string.ascii_uppercase + ' '    
    
    shiftedlowercase_and_space = lowercase_and_space[shift:] + lowercase_and_space[:shift]
    shifteduppercase_and_space = uppercase_and_space[shift:] + uppercase_and_space[:shift]    
    
    # Creates dictionary with original lists and shifted lists.
    # Uppercase list is added first because for some reason the space is assigned to belong to the 
    # Lowercase list, so that should be the overwritten version.
    
    for i in range(len(uppercase_and_space)):
        coder[uppercase_and_space[i]] = shifteduppercase_and_space[i]    
    
    for i in range(len(lowercase_and_space)):
        coder[lowercase_and_space[i]] = shiftedlowercase_and_space[i]

    return coder
    

def build_encoder(shift):
    """
    Returns a dict that can be used to encode a plain text. For example, you
    could encrypt the plain text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_encoder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    ### TODO.
    assert shift >= 0 and shift < 27, 'shift value %s is not between 0 and 27' % (shift,)    
    
    return build_coder(shift)

def build_decoder(shift):
    """
    Returns a dict that can be used to decode an encrypted text. For example, you
    could decrypt an encrypted text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    >>>decrypted_text = apply_coder(plain_text, decoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_decoder(3)
    {' ': 'x', 'A': 'Y', 'C': ' ', 'B': 'Z', 'E': 'B', 'D': 'A', 'G': 'D',
    'F': 'C', 'I': 'F', 'H': 'E', 'K': 'H', 'J': 'G', 'M': 'J', 'L': 'I',
    'O': 'L', 'N': 'K', 'Q': 'N', 'P': 'M', 'S': 'P', 'R': 'O', 'U': 'R',
    'T': 'Q', 'W': 'T', 'V': 'S', 'Y': 'V', 'X': 'U', 'Z': 'W', 'a': 'y',
    'c': ' ', 'b': 'z', 'e': 'b', 'd': 'a', 'g': 'd', 'f': 'c', 'i': 'f',
    'h': 'e', 'k': 'h', 'j': 'g', 'm': 'j', 'l': 'i', 'o': 'l', 'n': 'k',
    'q': 'n', 'p': 'm', 's': 'p', 'r': 'o', 'u': 'r', 't': 'q', 'w': 't',
    'v': 's', 'y': 'v', 'x': 'u', 'z': 'w'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    ### TODO.
    assert shift >= 0 and shift < 27, 'shift value %s is not between 0 and 27' % (shift,)    
    
    return build_coder(-shift)
 

def apply_coder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text

    Example:
    >>> apply_coder("Hello, world!", build_encoder(3))
    'Khoor,czruog!'
    >>> apply_coder("Khoor,czruog!", build_decoder(3))
    'Hello, world!'
    """
    ### TODO.
    newtext = ""    
    for char in text:
        # Checks to see if char is in the coder.       
        if char in coder:
            newtext += coder[char]
        # If char is not in the coder (i.e., punctuation), then just add the char as is.
        else:
            newtext += char
    return newtext
  

def apply_shift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. The empty space counts as the 27th letter of the alphabet,
    so spaces should be replaced by a lowercase letter as appropriate.
    Otherwise, lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.
    
    text: string to apply the shift to
    shift: amount to shift the text
    returns: text after being shifted by specified amount.

    Example:
    >>> apply_shift('This is a test.', 8)
    'Apq hq hiham a.'
    """
    ### TODO.
    return apply_coder(text, build_encoder(shift))
#
# Problem 2: Codebreaking.
#
    
    
"""
Pseudocode for Problem 2:

Create a loop that tries all shifts between 0 and 26.
In each iteration, use the decoder to create a test string.
Go through all of the words in the test string and check to see if they're valid words.
If all words are valid words, exit the loop.

"""



def find_best_shift(wordlist, text):
    """
    Decrypts the encoded text and returns the plaintext.

    text: string
    returns: 0 <= int 27

    Example:
    >>> s = apply_coder('Hello, world!', build_encoder(8))
    >>> s
    'Pmttw,hdwztl!'
    >>> find_best_shift(wordlist, s) returns
    8
    >>> apply_coder(s, build_decoder(8)) returns
    'Hello, world!'
    """
    ### TODO
    maxRealWords = 0
    bestShift = 0
    # Try all possible shifts    
    for n in range(27):
        # Initialize temporary realWords tracker        
        testRealWords = 0
        # Make temporary shifted text
        testtext = apply_coder(text, build_decoder(n))
        # Split temporary shifted text into words
        testwords = testtext.split()
        # Count number of real words
        for word in testwords:
            if is_word(wordlist, word):
                testRealWords += 1
        # Compare number of real words in current sample to best so far.
        if testRealWords > maxRealWords:
            maxRealWords = testRealWords
            bestShift = n
    return bestShift
   
   
#
# Problem 3: Multi-level encryption.
#
def apply_shifts(text, shifts):
    """
    Applies a sequence of shifts to an input text.

    text: A string to apply the Ceasar shifts to 
    shifts: A list of tuples containing the location each shift should
    begin and the shift offset. Each tuple is of the form (location,
    shift) The shifts are layered: each one is applied from its
    starting position all the way through the end of the string.  
    returns: text after applying the shifts to the appropriate
    positions

    Example:
    >>> apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    """
    ### TODO.
    #codedtext = ""    
    for i in range(len(shifts)):
        text = text[:shifts[i][0]] + apply_shift(text[shifts[i][0]:], shifts[i][1])        
    return text
    
#
# Problem 4: Multi-level decryption.
#
"""
Pseudocode for Problem 4:
1. Create a loop that tries all shifts between 0 and 26.
2. Once a valid word is found for a shift, keep that shift and apply a new shift to 
    the remaining text.
3. If the remaining text does not generate a valid word, undo the last shift.
4. For recursive function:
    4A. If the loop tries all shifts and does not find a valid word, then return False.
    4B. If a call of the recursive function returns False, then continue in the loop.
    4C. If a call of the recursive function does not return False, append the recursive function's 
        output to the tuple list and return that.
"""

def find_best_shifts(wordlist, text):
    """
    Given a scrambled string, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: Make use of the recursive function
    find_best_shifts_rec(wordlist, text, start)

    wordlist: list of words
    text: scambled text to try to find the words for
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    
    Examples:
    >>> s = random_scrambled(wordlist, 3)
    >>> s
    'eqorqukvqtbmultiform wyy ion'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> shifts
    [(0, 25), (11, 2), (21, 5)]
    >>> apply_shifts(s, shifts)
    'compositor multiform accents'
    >>> s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    >>> s
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> print apply_shifts(s, shifts)
    Do Androids Dream of Electric Sheep?
    """
       
    #for shift in range(27):
    #    testtext = 
    #            testtext = apply_coder(text, build_decoder(n))
        # Split temporary shifted text into words
    #    testwords = testtext.split()
    def find_best_shifts_rec(wordlist, text, start):
        
        validWord = 0
        #goodShift = 0        
        for shift in range(27):
            s = text[:start] + apply_coder(text[start:], build_coder(shift))
            spaceLoc = s.find(" ", start)
            if spaceLoc != -1 and is_word(wordlist, s[start:spaceLoc]):
                tuples = find_best_shifts_rec(wordlist, s, spaceLoc+1)
                if tuples == None:
                    continue
                else: return [(start, shift)] + tuples
            else:
                if is_word(wordlist, s[start:]):
                    validWord = 1
                    return [(start, shift)]
                else:
                    continue
        if validWord == 0:
            return None
        
    return find_best_shifts_rec(wordlist, text, 0)
    """
    testText = apply_coder(text[start:], build_decoder(shift))
    testWords = testText.split()
    if is_word(wordlist, testWords[0]):
        print testWords[0]                
        validWord = 1                
        goodShift = shift
        thisTuple = (start, goodShift)
        if len(testWords) == 1:
            return [thisTuple]
        else:
            remainingShifts = find_best_shifts_rec(
            wordlist, text[:start] + testText, testText.find(" ")+1)
            if remainingShifts == None:
                validWord = 0
                continue
            else: 
                return [thisTuple] + remainingShifts
    if validWord == 0:
    return None
    """
    

    #def find_best_shifts_rec(wordlist, text, start):
    """
    Given a scrambled string and a starting position from which
    to decode, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: You will find this function much easier to implement
    if you use recursion.

    wordlist: list of words
    text: scambled text to try to find the words for
    start: where to start looking at shifts
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    """
    ### TODO.


def decrypt_fable():
    """
    Using the methods you created in this problem set,
    decrypt the fable given by the function get_fable_string().
    Once you decrypt the message, be sure to include as a comment
    at the end of this problem set how the fable relates to your
    education at MIT.

    returns: string - fable in plain text
    """
    ### TODO.
    fable = get_fable_string()
    shifts = find_best_shifts(wordlist, fable)    
    return apply_shifts(fable, shifts)


    
#What is the moral of the story?
#
#
#
#
#

