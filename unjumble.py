import itertools
import mmap

# assume list of words in same directory as script. (adjust if not the case)
# Note: Currently using dictionary from github dwyl/english-words
_word_dict = 'words_alpha.txt'


def scan_words(document_folder, scrambled_word, unscrambled_length):
    """ produce a list of unique perms and print the ones in the dictionary """
    t = list(set(itertools.permutations(scrambled_word, unscrambled_length)))
    results = []
    for i in range(len(t)):
        potential_word = "".join(t[i])
        if check_word(document_folder + _word_dict, potential_word):
            results.append(potential_word)
    return results


def check_word(dictionary, word):
    """ scan dictionary for matches. Note this is a HUGE file; use mmap """
    found = False
    try:
        with open(dictionary, 'rb') as f:
            s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            # Note that each word terminates with \r\n.
            temp = '\n' + word.lower() + '\r'
            if s.find(str.encode(temp)) != -1:
                return True
    except FileNotFoundError:
        return False

