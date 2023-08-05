#!/usr/bin/env python3

import string
import unicodedata
import pandas as pd
import nltk
from nltk import RegexpTokenizer
from nltk.corpus import stopwords

stopwords = set(stopwords.words("english")) # set() speeds up stopword removal
punct_dict = dict((ord(punct), None) for punct in string.punctuation)

wnl = nltk.WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')


def remove_newline_chars(df_col):
    """
    Remove new line and/or carriage return from dataframe column.

    :param df_col: a single dataframe column <class 'pandas.core.series.Series'>
    :return: a single dataframe column <class 'pandas.core.series.Series'>

    Example
    -------
    >>> from shizen_gengo.preprocess_text import text_utils
    >>> df.col_name = text_utils.remove_newline_chars(df.col_name)
    """
    if df_col.ndim > 1:
        raise Exception ("not a dataframe column")
    return df_col.replace({r'(\r\n|\r|\n|\\r\\n|\\r|\\n)+' : ' '}, regex=True)


def remove_digits(df_col):
    """
    Remove digits.

    :param df_col: a single dataframe column <class 'pandas.core.series.Series'>
    :return: a single dataframe column <class 'pandas.core.series.Series'>
    """
    if df_col.ndim > 1:
        raise Exception("not a dataframe column")
    return df_col.str.replace(r'[0-9]+', '')


def remove_non_char(df_col):
    """
    Remove non-alphabetic tokens: :code:`[#<>=.,;:$&*|?\'\"\-()%]`

    :param df_col: a single dataframe column <class 'pandas.core.series.Series'>
    :return: a single dataframe column <class 'pandas.core.series.Series'>
    """
    if df_col.ndim > 1:
        raise Exception("not a dataframe column")
    return df_col.str.replace(r'[#<>=.,;:$&*|?\'\"\-()%]', ' ')


def custom_replace(df_col, change_from='', change_to=''):
    """
    Replace tokens.

    :param df_col: a single dataframe column <class 'pandas.core.series.Series'>
    :param change_from: string
    :param change_to: string
    :return: a single dataframe column <class 'pandas.core.series.Series'>
    """
    if df_col.ndim > 1:
        raise Exception("not a dataframe column")
    return df_col.str.replace(change_from, change_to, regex=True)


def remove_url(df_col):
    """
    Remove hyperlink / url.

    :param df_col: a single dataframe column <class 'pandas.core.series.Series'>
    :return: a single dataframe column <class 'pandas.core.series.Series'>
    """
    if df_col.ndim > 1:
        raise Exception("not a dataframe column")
    return df_col.str.replace(r'http\S+', '')


def remove_email(df_col):
    """
    Remove email address.

    :param df_col: a single dataframe column <class 'pandas.core.series.Series'>
    :return: a single dataframe column <class 'pandas.core.series.Series'>
    """
    if df_col.ndim > 1:
        raise Exception("not a dataframe column")
    return df_col.str.replace(r'\S*@\S*\s?', '')


def remove_consecutive_spaces(df_col):
    """
    Remove consecutive white spaces.

    :param df_col: a single dataframe column <class 'pandas.core.series.Series'>
    :return: a single dataframe column <class 'pandas.core.series.Series'>
    """
    if df_col.ndim > 1:
        raise Exception("not a dataframe column")
    return df_col.str.replace(r'\s+', ' ', regex=True)


def remove_repeating_letters(df_col):
    """
    Remove repeating letters with a minimum threshold of 2.

    The threshold prevents repeated letters in names e.g. Aaron to be preserved.

    :param df_col: a single dataframe column <class 'pandas.core.series.Series'>
    :return: a single dataframe column <class 'pandas.core.series.Series'>
    """
    if df_col.ndim > 1:
        raise Exception("not a dataframe column")
    min_threshold_rep = 3
    return df_col.str.replace(r'(\w)\1{%d,}' % (min_threshold_rep - 1), r'\1')


def remove_accented_chars(df_col):
    """
    Remove accented characters.

    :param df_col: a single dataframe column <class 'pandas.core.series.Series'>
    :return: a single dataframe column <class 'pandas.core.series.Series'>
    """
    listed = df_col.to_list()
    listed = [(unicodedata.normalize('NFKD', str(text))
                .encode('ascii', 'ignore')
                .decode('utf-8', 'ignore')) for text in listed]
    return pd.Series(listed)

def remove_punctuation(df_col):
    """
    Remove punctuation.

    :param df_col: a single dataframe column <class 'pandas.core.series.Series'>
    :return: a single dataframe column <class 'pandas.core.series.Series'>
    """
    listed = df_col.to_list()
    listed =  [text.translate(punct_dict) for text in listed]
    return pd.Series(listed)


def remove_stopwords(df_col):
    """
    Remove stopwords.

    Also removes carriage return `\\r` and line break `\\n` characters.

    :param df_col: a single dataframe column <class 'pandas.core.series.Series'>
    :return: a single dataframe column <class 'pandas.core.series.Series'>
    """
    ls = []
    listed = df_col.to_list()
    for text in listed:
        tokens = tokenizer.tokenize(str(text))
        filtered_words = [w for w in tokens if not w in stopwords]
        filtered_words = [wnl.lemmatize(w) for w in filtered_words]
        ls.append(" ".join(filtered_words))
    return ls

def clean_text(df_col):
    """
    Function that combines all text pre-processing tasks.

    * remove accented_chars
    * remove punctuation
    * remove repeating_letters
    * remove newline_chars
    * remove digits
    * remove non_char
    * remove url
    * remove email
    * remove consecutive_spaces
    * remove stopwords

    :param df_col: a single dataframe column <class 'pandas.core.series.Series'>
    :return: a single dataframe column <class 'pandas.core.series.Series'>
    """
    if df_col.ndim > 1:
        raise Exception("not a dataframe column")
    df_col = remove_accented_chars(df_col)
    df_col = remove_punctuation(df_col)
    df_col = remove_repeating_letters(df_col)
    df_col = remove_newline_chars(df_col)
    df_col = remove_digits(df_col)
    df_col = remove_non_char(df_col)
    # df_col = custom_replace
    df_col = remove_url(df_col)
    df_col = remove_email(df_col)
    df_col = remove_consecutive_spaces(df_col)
    df_col = remove_stopwords(df_col)

    return df_col

if __name__ == "__main__":
    pass