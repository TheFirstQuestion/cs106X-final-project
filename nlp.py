from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, words
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tag import pos_tag
from nltk import Counter, FreqDist
from nltk.collocations import BigramAssocMeasures, TrigramAssocMeasures, BigramCollocationFinder, TrigramCollocationFinder

bigram_measures = BigramAssocMeasures()
trigram_measures = TrigramAssocMeasures()
ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()
stopwords = set(stopwords.words('english'))
allEnglishWords = set(words.words())

def countWords(self):
    filteredWords = cleanWords(self.contents)
    counts = Counter(filteredWords)
    wordFreq = dict()
    # Convert to relative frequency
    for c in counts:
        wordFreq[c] = counts[c] / len(filteredWords)
    return wordFreq


def cleanWords(text):
    # Tokenize -- split on spaces, basically
    tokens = word_tokenize(text)
    # Pull out proper nouns for later
    properNouns = [word for word,pos in pos_tag(tokens) if pos == 'NNP']

    filteredWords = []
    for token in tokens:
        if (not token.isalpha()):
            # What about acronyms? (F.B.I.) https://stackoverflow.com/questions/17703684/how-to-find-acronyms-in-a-pdf-file
            continue
        token = lemmatizer.lemmatize(token)
        low = token.lower()
        # Ignore and, the, etc. as well as urls
        if (token in stopwords or low in stopwords or token == "http"):
            continue
        # Make sure it's either a word or a proper noun (name, e.g.)
        # or in properNouns
        if (token in allEnglishWords or token in properNouns):
            filteredWords.append(token)

    return filteredWords


def getCommonPhrases(self):
    words = cleanWords(self.contents)
    finder2 = BigramCollocationFinder.from_words(words)
    # only bigrams that appear 3+ times
    finder2.apply_freq_filter(3)
    # return the 10 n-grams with the highest PMI
    twoWordPhrases = sorted(finder2.nbest(bigram_measures.pmi, 10))
    # Same thing but trigrams
    finder3 = TrigramCollocationFinder.from_words(words)
    finder3.apply_freq_filter(3)
    threeWordPhrases = sorted(finder3.nbest(trigram_measures.pmi, 10))
    return (twoWordPhrases + threeWordPhrases)


def stem(word):
    return ps.stem(word)
