#!/usr/bin/env python3
import pandas as pd

def search(df, df_col='', tok=''):
    """
    Search dataframe column and return rows that contain the specified token.

    :param df: dataframe
    :param df_col: string
    :param tok: string
    :return: dataframe

    Example
    -------
    >>> from shizen_gengo.explore import explore_utils
    >>> df.col_name = explore_utils.search(df, 'col_name', 'keyword')
    """
    df = df[df.index.notnull()]
    # Convert the dataframe column to a list for faster searching.
    listed = df[df_col].to_list()
    df['search_flag'] = [tok in str(i) for i in listed]
    return df[df.search_flag==True].drop('search_flag', axis = 1)


#TODO
def search_window(df_col, token = ''):
    # if dataframe_col.ndim == 1:
    #     raise Exception ("not a dataframe")
    # print(len(dataframe_col))
    # dataframe_col.replace("", np.nan, inplace=True)
    # dataframe_col = dataframe_col.dropna()
    # print(len(dataframe_col))
    # pat = r'(?P<before>(?:\w+\W+){,8})(?i)' + token + r'\W+(?P<after>(?:\w+\W+){,8})'
    # res = dataframe_col.str.extract(pat, expand=False)
    # res = res.dropna()
    # # print(len(new))
    # return res.sample(min(10, len(res)))
    pass


def check_missing_values(df):
    """
    Returns a dataframe with missing values count for all columns
    sorted in descending order.

    :param df: dataframe
    :return: dataframe
    """
    return (pd.DataFrame(df.isna().sum(),
                        columns=['missing'])
            .sort_values(by='missing', ascending=False))

if __name__ == "__main__":
    pass