import random

# Source: http://wordlist.aspell.net/12dicts/
FILE_PATH_TO_WORD_LIST = "2of12inf.txt"

SCRABBLE_POINTS = { 'e': 1, 'a': 1, 'i': 1, 'o': 1, 'n': 1, 'r': 1, 't': 1, 'l': 1, 's': 1, 'u': 1, 'd': 2, 'g': 2, 'b': 3, 'c': 3, 'm': 3, 'p': 3, 'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4, 'k': 5, 'j': 8, 'x': 8, 'q': 10, 'z': 10 }

def get_word_list(file_path=FILE_PATH_TO_WORD_LIST):
    file = open(file_path)
    words = [line for line in file if ("!" not in line) and ("%" not in line)]
    file.close()
    return words

def pick_word(word_list=get_word_list()):
    word = random.choice(word_list)
    return word

def pick_set_of_words(no_of_words, word_list=get_word_list()):
    set_of_words = []
    while True:
        if len(set_of_words) == no_of_words:
            break
        word = random.choice(word_list)
        if word not in set_of_words:
            set_of_words.append(word)
    return set_of_words

def get_anagrams_for_word(word, word_list=get_word_list()):
    anagrams = [el for el in word_list if sorted(el) == sorted(word)]
    return anagrams

def get_anagrams_for_words(words, word_list=get_word_list()):
    anagrams = {}
    for word in words:
        anagrams[word] = get_anagrams_for_word(word, word_list)
    return anagrams

def combine_words(words):
    unique_chars = []
    for char in "".join(words):	
	    if char not in unique_chars:	
	        unique_chars.append(char)
    seq_of_chars = ""
    for char in sorted(unique_chars):
	    seq_of_chars += char*max([word.count(char) for word in words])
    return seq_of_chars

def check_if_word_is_valid(word, seq_of_chars, word_list=get_word_list()):
    is_in_seq_of_chars = not(False in [(word.count(char) <= seq_of_chars.count(char)) for char in word])
    is_in_word_list = word in word_list
    is_valid = is_in_seq_of_chars and is_in_word_list
    return is_valid

def get_score_equivalent_of_word(word):
    score = sum([SCRABBLE_POINTS[char] for char in word])
    return score

def get_set_score(words):
    set_score = sum([get_score_equivalent_of_word(word) for word in words])
    return set_score

def get_total_score_from_seq_of_chars(seq_of_chars, word_list=get_word_list()):
    total_score = 0
    for word in word_list:
        if not(False in [(word.count(char) <= seq_of_chars.count(char)) for char in word]):
            total_score += get_score_equivalent_of_word(word)
    return total_score