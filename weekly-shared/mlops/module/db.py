"""
    與 DB 的交互模組。
"""

import pandas as pd     # 通常會儲存到DB，如BQ，這邊先用 csv 替代，或者批量轉到BQ。
import sqlite3
import json


def get_json(filename, mode='r'):
    with open(filename, mode=mode) as f:
        json_file = json.load(f)
    return json_file


def connect_db(db_name, query, is_insert=False):
    """
        # cur.execute(```
        # INSERT INTO movie VALUES
        #     ('Monty Python and the Holy Grail', 1975, 8.2),
        #     ('And Now for Something Completely Different', 1971, 7.5)
        # ```) 
    """
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    res = cur.execute(query)
    if is_insert:
        con.commit()
    
    return res
       

def query_db(db_name, query):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    return cur.execute(query)


def transform_db_query_to_df(db_name, db_query):
    # column_query = "PRAGMA table_info('prediction') "
    df = pd.DataFrame(query_db(db_name, db_query))
    return df


def get_column_name_from_sqlite(db_name, table_name):
    db_query = f"PRAGMA table_info('{table_name}')"
    df = transform_db_query_to_df(db_name, db_query)
    column_names = df[1].tolist()
    return column_names


def save_prediction_data(data, db_name):
    """
        將資料儲存好。
        X, y_pred
    """
    con = sqlite3.connect(db_name)      # 需要用 ab path
    cur = con.cursor()
    # data = [
    #     ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
    #     ("Monty Python's The Meaning of Life", 1983, 7.5),
    #     ("Monty Python's Life of Brian", 1979, 8.0),
    # ]
    fstring = "INSERT INTO prediction VALUES " + '(' + '?,' * 32 + '?)'
    print(fstring)
    cur.executemany(fstring, data)
    con.commit()