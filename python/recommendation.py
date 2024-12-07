import pickle
import pandas as pd
import numpy as np
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec, Phrases
from gensim.parsing.preprocessing import STOPWORDS as stop_words
from gensim.utils import simple_preprocess
from sklearn.feature_extraction import text
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import SnowballStemmer

# make words to exclude from processing
def make_stop_words(research_interests):
    global stop_words
    words = ['program', 'undergraduate', 'students', 'intern', 'experience', 'internship', \
        'university', 'college', 'research', 'opportunity', \
            'fellows', 'scholars', 'undergrad']
    words += research_interests
    stopwords = stop_words.union(set(words))
    
    my_stop_words = text.ENGLISH_STOP_WORDS.union(stopwords)
    return my_stop_words

def preprocessor(text, my_stop_words):
    """uses gensim simple_preprocess and then removes stop words
    -> used in the tag_docs function
    """
    # Instantiate a LancasterStemmer object, use gensim simple_preprocess to tokenize/lowercase
    # and then removes stop words
    simple = simple_preprocess(text)
    result = [word for word in simple if not word in my_stop_words]
    return result

def stem_tag_docs(docs, my_stop_words):
    ls = LancasterStemmer()
    results = docs.apply(lambda r: TaggedDocument(words=preprocessor(r['Description'], my_stop_words), tags=[str(r['Id'])]), axis=1)
    return results.tolist()

def recommend_RO(research_opps, research_interests):
    my_stop_words = make_stop_words(research_interests)
    tagged_research_opps = stem_tag_docs(research_opps, my_stop_words)
    model = Doc2Vec(vector_size=50, min_count=1, epochs=40)
    model.build_vocab(tagged_research_opps)
    model.train(tagged_research_opps, total_examples=model.corpus_count, epochs=model.epochs)
    vector = model.infer_vector(research_opps.iloc[0, 1].split())
    d2v_test = model.docvecs.most_similar(positive=[vector,], topn=10)
    return d2v_test