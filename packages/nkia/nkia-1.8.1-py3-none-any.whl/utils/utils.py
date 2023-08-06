from pathlib import Path
import os
import sys
import re
import string
import tarfile
import pymongo
import unidecode
import nltk
import tensorflow_datasets as tfds
import tensorflow as tf
import pandas as pd
import gdown
from symspellpy import SymSpell, Verbosity
import numpy as np


def get_dataframe_from_mongo(mongo_conn, collection):
    products_df = mongo_conn.db[collection].find(
        {}).sort('created', pymongo.DESCENDING)

    return pd.DataFrame(products_df[0]['df']) if products_df else ''


def get_cleaned_predictor(sym_spell, description, product_name, model_name):
    stop_words = get_stop_words_list(model_name)
    description = [get_description_and_name(x, stop_words) for x in description]
    product_name = [get_description_and_name(x, stop_words) for x in product_name]

    X = join_all_predictors(description, product_name)

    X = correct_word_spelling(sym_spell, X)
    return X


def get_stop_words_list(model_name):
    stop_words = nltk.corpus.stopwords.words('portuguese')

    custom_stop_words = ['carrefour', 'compre', 'aproveite', 'produto', 'qualidade', 'oportunidade', 'preco', 'justo', 
    'voce', 'curtiu', 'qualidade', 'alem', 'disso']

    if model_name == 'category_model':
        food_model_stop_words = ['unidades', 'saboroso', 'boca', 'g', 'ml', 'cm', 'kg', 'sabor', 'kcal', 'mg', 'delicioso', 'mercado']
        custom_stop_words.extend(food_model_stop_words)
    
    stop_words.extend(custom_stop_words)
    return stop_words

def get_description_and_name(data, stop_words):
    data = unidecode.unidecode(data[0]).lower()
    data = re.sub(r'['+string.punctuation+']', '', data)
    data = [word for word in data.split() if word not in stop_words]

    return ' '.join(data)


def join_all_predictors(description, product_name):
    count = 0
    X = []

    for name in product_name:
        X.append(name + ' ' + description[count])
        count += 1

    return X


def preprocessing_fn(X, token_path):
    X, tokenizer = tokenize_data(X, token_path)
    X = padding_matrix(X)

    print('Preprocessing_fn finished')
    sys.stdout.flush()
    return X, tokenizer


def tokenize_data(data, token_path):
    tokenizer = tfds.features.text.SubwordTextEncoder.build_from_corpus(
        data, target_vocab_size=2**14)

    tokenizer.save_to_file(token_path)
    data = [tokenizer.encode(sentence) for sentence in data]

    return data, tokenizer


def padding_matrix(data):
    max_sentence_len = max([len(sentence) for sentence in data])
    data = tf.keras.preprocessing.sequence.pad_sequences(
        data,
        value=0,
        padding='post',
        maxlen=max_sentence_len)

    return data


def read_file(file_name, content=''):
    if content:
        with open(os.path.join(Path(os.path.dirname(__file__)), file_name), 'w') as _file:
            _file.write(str(content))
            _file.close()
    else:
        with open(os.path.join(Path(os.path.dirname(__file__)), file_name)) as _file:
            return _file.read()


def get_model_files_by_version(model_name, model_version):
    splitted_name = model_name.split('/')
    bucket = 'category-model' if 'category_model' in splitted_name else 'food-model'

    url = 'https://{}.s3.amazonaws.com/{}'.format(
        bucket, model_version + '.tar.gz')

    if model_version not in os.listdir(model_name):
        download_model(url, model_name + model_version + '.tar.gz')


def download_model(url, output):
    gdown.download(url, output, quiet=False)

    tar = tarfile.open(output)
    tar.extractall('/'.join(output.split('/')[0:-1]))
    tar.close()
    os.remove(output)


def instantiate_spelling_corrector(dict_path='./src/utils/datasets/dictionary.pkl'):
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    sym_spell.load_pickle(dict_path)
    return sym_spell


def correct_word_spelling(sym_spell, corpus):
    final_corpus = []
    corpus = np.char.split(np.array(corpus))

    for phrase in corpus:
        new_phrase = [get_word_suggestion(sym_spell, x) for x in phrase]
        final_corpus.append(' '.join(new_phrase).replace('  ', ' ').strip())

    return final_corpus


def get_word_suggestion(sym_spell, input_term):
    suggestion = sym_spell.lookup(
        input_term, Verbosity.TOP, max_edit_distance=2)

    if len(suggestion) > 0:
        return suggestion[0].term

    return ''
