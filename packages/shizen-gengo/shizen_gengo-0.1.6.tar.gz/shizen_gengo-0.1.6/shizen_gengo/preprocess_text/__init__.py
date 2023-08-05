"""
Functions to clean text in a pandas dataframe column.
"""

from .nltkmodules import *
from .text_utils import remove_newline_chars, remove_digits, remove_non_char, custom_replace, remove_url, remove_email, \
                        remove_consecutive_spaces, remove_stopwords, remove_accented_chars, remove_punctuation, \
                        remove_repeating_letters, clean_text

__all__ = ['remove_newline_chars',
           'remove_digits',
           'remove_non_char',
           'custom_replace',
           'remove_url',
           'remove_email',
           'remove_consecutive_spaces',
           'remove_stopwords',
           'remove_accented_chars',
           'remove_punctuation',
           'remove_repeating_letters',
           'clean_text']