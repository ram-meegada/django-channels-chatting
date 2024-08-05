import nltk
from nltk.corpus import words

# Download the word list (if not already done)
nltk.download('words')

# Get the list of words
word_list = set(words.words())

def is_valid_word(word):
    return word.lower() in word_list

# Example usage
print(is_valid_word("hello"))  # True
print(is_valid_word("shlok"))  