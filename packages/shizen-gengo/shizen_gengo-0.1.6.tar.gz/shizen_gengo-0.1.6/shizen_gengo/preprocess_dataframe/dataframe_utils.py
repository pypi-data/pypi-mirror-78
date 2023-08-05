#!/usr/bin/env python3
import numpy as np

def rename_column(df_col_names, before, after):
    """
    Rename column.

    :param df_col_names: dataframe column names <class 'pandas.core.indexes.base.Index'>
    :param before: string
    :param after: string
    :return: dataframe column names <class 'pandas.core.indexes.base.Index'>

    Example
    -------
    >>> from shizen_gengo.preprocess_dataframe import dataframe_utils
    >>> df.columns = dataframe_utils.rename_column(df.columns, 'Description2', 'Description')
    """
    return map(lambda x: str.replace(x, before, after), df_col_names)


def standardise_column_headers(df_col_names, before=None, after=None):
    """
    Make dataframe headers lowercase and replace spaces by underscores.

    The function allows to specify custom replacements.

    For example: `Group - Primary` can be changed to `group_primary` by calling

    `df.columns = utils.standardise_column_headers(df.columns, before='_-_', after='_')`

    :param df_col_names: dataframe column names <class 'pandas.core.indexes.base.Index'>
    :param before: string
    :param after: string
    :return: dataframe column names <class 'pandas.core.indexes.base.Index'>
    """
    df_col_names = map(str.lower, df_col_names)
    df_col_names = map(lambda x : x.replace(' ', '_'), df_col_names)
    if before and after:
        df_col_names = map(lambda x: x.replace(before, after), df_col_names)
    return df_col_names


def fill_missing(df_col, val='MISSING'):
    """
    Fill missing values with string of choice. Default is "MISSING".

    The function first replaces cells with an empty string and/or cells with only spaces with `np.nan`.

    :param df_col: a single dataframe column
    :param val: string
    :return: a single dataframe column
    """
    return (df_col
            .replace(r'^\s*$', np.nan, regex=True)
            .fillna(val)
            )


if __name__ == "__main__":
    pass