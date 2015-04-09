__author__ = 'Esther Seyffarth'


from nltk.corpus import cmudict, gutenberg
import re
import random

words = cmudict.dict()
to_delete = []

for word in words:
    try:
        words[word] = "".join(*words[word])
    except TypeError:
        # TODO: handle this better
        #print("couldn't generate dictionary entry")
        to_delete.append(word)

for item in to_delete:
    del words[item]

re.VERBOSE

dactyl = re.compile("^[A-Z]+(1|2)[A-Z]+0[A-Z]+0[A-Z]*$")
spondee = re.compile("^[A-Z]+(1|2)[A-Z]+(1|2)[A-Z]*$")
final = re.compile("^[A-Z]+(1|2)[A-Z]+[0-9][A-Z]*$")

verse = re.compile("""^([A-Z]+(1|2)[A-Z]+0[A-Z]+0[A-Z]*)|([A-Z]+(1|2)[A-Z]+(1|2)[A-Z]*){4}    # first 4 feet are dactyl or spondee
                   [A-Z]+(1|2)[A-Z]+0[A-Z]+0[A-Z]*              # fifth foot is a dactyl
                   [A-Z]+(1|2)[A-Z]+[0-9][A-Z]*$                # sixth foot has two syllables
                   """
)

one_syllable = re.compile("^[^aeiou]*[aeiou]+[^aeiou]*$")

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

def get_poem():
    """
    This function should extract hexametric sentences from Gutenberg texts, but it doesn't.
    Either hexametric sentences are too rare, or the absence of basic function words from CMUdict results in problems
    with the matching of the whole sentence.
    """
    outtext = []
    for corpus in gutenberg.fileids():
        text = gutenberg.sents(corpus)
        for sentence in text:
            transcription = ""
            discard = False
            for word in sentence:
                if word.lower() in words:
                    transcription += words[word.lower()]
                elif re.match(one_syllable, word.lower()):
                    # consider this word a "small", unstressed word
                    transcription += "A0A"
                else:
                    discard = True
            if re.match(verse, transcription) and not discard:
                print(sentence, transcription)
                outtext.append(" ".join(sentence))
    return "\n".join(outtext)

outpath = input("please specify output path: ")
outpath = re.sub("\\\\", "/", outpath)
outfile = open(outpath, "w", encoding="utf8")
print(make_poem(), file=outfile)
outfile.close()
