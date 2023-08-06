
from PyProfane.functions import soundex, censorWord, censorSentences, updateSwearwords, isProfane
from pprint import pprint

if __name__ == "__main__":

    f2 = open('PyProfane/data/comments.txt', 'r')
    comments = f2.read().splitlines()
    pprint(censorSentences(comments))
