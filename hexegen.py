__author__ = 'Esther Seyffarth'


from nltk.corpus import cmudict
import re
import random


words = cmudict.dict()
to_delete = []
success = 0
error = 0
for word in words:
    try:
        words[word] = "".join(*words[word])
        success += 1
    except TypeError:
        # TODO: handle this better
        #print("couldn't generate dictionary entry")
        to_delete.append(word)
        error += 1

for item in to_delete:
    del words[item]



dactyl = re.compile("^[A-Z]+(1|2)[A-Z]+0[A-Z]+0[A-Z]*$")
spondee = re.compile("^[A-Z]+(1|2)[A-Z]+(1|2)[A-Z]*$")
final = re.compile("^[A-Z]+(1|2)[A-Z]+[0-9][A-Z]*$")

dactyl_words = set()
spondee_words = set()
final_words = set()
for word in words:
    if re.match(dactyl, words[word]):
        dactyl_words.add(word)
    elif re.match(spondee, words[word]):
        spondee_words.add(word)
    elif re.match(final, words[word]):
        final_words.add(word)


def make_verse():
    verse = []
    for i in range(4):
        # decide whether to generate a dactyl or a spondee
        choice = random.randint(0, 2)
        if choice == 0:
            verse.append(random.sample(dactyl_words, 1)[0])
        else:
            verse.append(random.sample(spondee_words, 1)[0])
    verse.append(random.sample(dactyl_words, 1)[0])
    verse.append(random.sample(final_words, 1)[0])
    return " ".join(verse)

def make_poem():
    poem = []
    for i in range(50):
        poem.append(make_verse())
    return "\n".join(poem)

outpath = input("please specify output path: ")
outpath = re.sub("\\\\", "/", outpath)
outfile = open(outpath, "w", encoding="utf8")
print(make_poem(), file=outfile)
outfile.close()
