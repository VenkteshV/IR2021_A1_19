import pickle
import os
import re, string, unicodedata
import nltk
# !pip install contractions
# !pip install inflect
import spacy
import contractions
import inflect
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords') 

def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def remove_between_square_brackets(text):
    text=re.sub('\n',' ',text)
    return re.sub('\[[^]]*\]', '', text)

def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    return text

def replace_contractions(text):
    return contractions.fix(text)

def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words

def get_wordnet_pos(tag):
    tag_dict = {"J": wordnet.ADJ,"N": wordnet.NOUN,"V": wordnet.VERB,"R": wordnet.ADV}
    return tag_dict.get(tag,wordnet.NOUN)

def lemmatize(words):
    """Lemmatize words in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    posTagged = nltk.pos_tag(words)
    wordnetTagged = list(map(lambda x: (x[0], get_wordnet_pos(x[1][0])), posTagged))
    for word,tag in wordnetTagged:
      lemma = lemmatizer.lemmatize(word,tag)
      lemmas.append(lemma)
    return lemmas
def lemmatizeSpacy(words):
    sent = ""
    lwords = []
    for word in words:
        sent += word + " " 
    model = spacy.load("en_core_web_sm")
    tokens = model(sent)
    for token in tokens:
        lwords.append(token.lemma_)
    return lwords
def preProcess_html(fileName):
    sample = denoise_text(fileName)
    sample = replace_contractions(sample)
    words = nltk.word_tokenize(sample)
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = remove_stopwords(words)
    words = lemmatize(words)
    return words  

def clean_text(text):
    # text=re.sub('\w*\d\w*','', text)
    text=re.sub('\n',' ',text)
    text=re.sub(r"http\S+", "", text)
    text=re.sub('[^a-z0-9A-Z]',' ',text)
    text=re.sub(' +',' ',text)
    return text

def preProcessSentence(sentence):
    sample = clean_text(sentence)
    sample = replace_contractions(sample)
    words = nltk.word_tokenize(sample)
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = remove_stopwords(words)
    words = lemmatizeSpacy(words)
    return words 