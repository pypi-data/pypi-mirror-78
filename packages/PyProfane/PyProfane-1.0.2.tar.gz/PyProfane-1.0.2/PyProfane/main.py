from PyProfane.functions import soundex, censorWord, censorSentences, updateSwearwords, isProfane, getProfaneWords
if __name__ == "__main__":
    f2 = open('data/comments.txt', 'r')
    comments = f2.read().splitlines()
    print(censorSentences(comments))