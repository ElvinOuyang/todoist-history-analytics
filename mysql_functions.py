import sqlalchemy
import os
import sys
import pandas as pd
import todoist_functions as todofun


def connect_mysql():
    """
Setup MySQL connection for data connection
-----Environment Variables-----
Five enviroment variables should be set up before calling this function:
MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
The default encoding is set to utf-8 for better compatibility
-----OUTPUT-----
A SQLAlchemy engine with connections to MySQL database
    """
    try:
        host = os.environ['MYSQL_HOST']
        port = int(os.environ['MYSQL_PORT'])
        user = os.environ['MYSQL_USER']
        password = os.environ['MYSQL_PASSWORD']
        db = os.environ['MYSQL_DB']
    except KeyError:
        sys.stderr.write("MYSQL_* environment variable not set\n")
        sys.exit(1)
    conn = sqlalchemy.create_engine(
        'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
            user,
            password,
            host,
            port,
            db), encoding='utf-8')
    return conn


def overwrite_table_mysql(df, table_name):
    """
Function that overwrites a table in MysQL database
-----INPUT-----
df: the pandas dataframe to write in the MySQL table
table_name: the destination table name in the MySQL database
-----OUTPUT-----
none. the action was taken to upload data to MySQL database
    """
    conn = connect_mysql()
    df.to_sql(name=table_name, con=conn,
              if_exists='replace', index=False)


def append_table_mysql(df, table_name):
    """
Function that appends a table in MysQL database
-----INPUT-----
df: the pandas dataframe to write in the MySQL table
table_name: the destination table name in the MySQL database
-----OUTPUT-----
none. the action was taken to upload data to MySQL database
    """
    conn = connect_mysql()
    df.to_sql(name=table_name, con=conn,
              if_exists='append', index=False)


def create_full_activity(table_name='activity_history'):
    """
Function that creates a standardized activity pandas dataframe from MySQL table
-----INPUT-----
table_name: the table name of the full activity history table in MySQL database
-----OUTPUT-----
df: the standardized pandas dataframe of activity history
    """
    conn = connect_mysql()
    df = pd.read_sql(table_name, conn)
    df = todofun.df_standardization(df)
    return df
