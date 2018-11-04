import os, random, interface

# Source: http://wordlist.aspell.net/12dicts/
FILE_PATH_TO_WORD_LIST = "lib\\2of12inf.txt"

FILE_PATH_TO_SAVE_FILE = "lib\\save_file.txt"

SAVE_STATE = {
    "scene": "START",
    "mode": None,
    "with_timer": None,
    "time_left": None,
    "char_seq": None,
    "retries": 3,
    "score": 0,
    "valid_words": None,
    "used_words": []
}

SCRABBLE_POINTS = { 'e': 1, 'a': 1, 'i': 1, 'o': 1, 'n': 1, 'r': 1, 't': 1, 'l': 1, 's': 1, 'u': 1, 'd': 2, 'g': 2, 'b': 3, 'c': 3, 'm': 3, 'p': 3, 'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4, 'k': 5, 'j': 8, 'x': 8, 'q': 10, 'z': 10 }
MAX_WORD_LENGTH = 5
MAX_WORD_LIST_LENGTH = 3

def get_word_list(file_path=FILE_PATH_TO_WORD_LIST):
    file = open(file_path)
    words = []
    for line in file:
        line = line.replace("\n", "")
        if "!" in line:
            line = line.replace("!", "")
        if "%" in line:
            line = line.replace("%", "")
        if len(line) <= MAX_WORD_LENGTH:
            words.append(line)
    file.close()
    return words

def pick_word(game_state, word_list=get_word_list()):
    while True:
        word = random.choice(word_list)
        if word not in game_state["used_words"]:
            game_state["used_words"].append(word)
            break
    return word

def pick_set_of_words(no_of_words=MAX_WORD_LIST_LENGTH, word_list=get_word_list()):
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

def combine_words(words):
    unique_chars = []
    for char in "".join(words):	
	    if char not in unique_chars:	
	        unique_chars.append(char)
    char_seq = ""
    for char in sorted(unique_chars):
        char_seq += char*max([word.count(char) for word in words])
    return char_seq

def check_if_word_is_valid(word, seq_of_chars, word_list=get_word_list()):
    is_in_seq_of_chars = not(False in [(word.count(char) <= seq_of_chars.count(char)) for char in word])
    is_in_word_list = word in word_list
    return is_in_seq_of_chars and is_in_word_list

def get_valid_words_from_seq(seq_of_chars, word_list=get_word_list()):
    valid_words = []
    for word in word_list:
        if check_if_word_is_valid(word, seq_of_chars):
            valid_words.append(word)
    return valid_words

def get_score_equivalent_of_word(word):
    score = sum([SCRABBLE_POINTS[char] for char in word])
    return score

def load_save_file(file_path=FILE_PATH_TO_SAVE_FILE):
    file = open(file_path, "r+")
    game_state = {}
    for line in file:
        key, value = line.replace("\n","").split("=")
        if value == 'None':
            game_state[key] = None
        elif key in ["scene", "mode", "char_seq"]:
            if key == "scene" and value == "SAVE":
                game_state[key] = interface.PLAY
            else:
                game_state[key] = value
        elif key in ["time_left", "retries", "score"]:
            game_state[key] = int(value)
        elif key in ["valid_words", "used_words"]:
            game_state[key] = value[1:-1].split(",")
        elif key == "with_timer":
            game_state[key] = bool(value)
    file.close()
    return game_state

def save_to_file(game_state, file_path=FILE_PATH_TO_SAVE_FILE):
    file = open(file_path, "w+")
    for key in game_state:
        value = game_state[key]
        if value is None:
            file.write(key.strip() + "=" + str(value).strip() + "\n")
        elif key in ["scene", "mode", "char_seq"]:
            file.write(key.strip() + "=" + value.strip() + "\n")
        elif key in ["time_left", "retries", "score"]:
            file.write(key.strip() + "=" + str(value).strip() + "\n")
        elif key in ["valid_words", "used_words"]:
            file.write(key.strip() + "=[" + ",".join(value).strip() + "]\n")
        elif key == "with_timer":
            file.write(key.strip() + "=" + str(value).strip() + "\n")
    file.close()

def create_or_load_save_file(file_path=FILE_PATH_TO_SAVE_FILE):
    file = open(file_path, "r")
    if os.stat(file_path).st_size != 0:
        file.close()
        return load_save_file(file_path)
    print("here")
    game_state = SAVE_STATE
    save_to_file(game_state, file_path)
    return game_state

def get_time(seconds):
    if seconds % 60 > 9:
        return str(seconds // 60) + ":" + str(seconds % 60)
    else:
        return str(seconds // 60) + ":0" + str(seconds % 60)