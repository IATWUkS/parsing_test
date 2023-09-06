import sqlite3
import traceback


def connection_db():
    sqlite_connection = sqlite3.connect('company_info.db')
    return sqlite_connection


def create_table():
    sqlite_connection = connection_db()
    try:
        sql_query = ''' CREATE TABLE if not exists company (id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    okved_code TEXT NOT NULL,
                    inn INTEGER NOT NULL,
                    kpp INTEGER NOT NULL,
                    place_registration TEXT NOT NULL)'''
        cursor = sqlite_connection.cursor()
        cursor.execute(sql_query)
        sqlite_connection.commit()
        cursor.close()
    except:
        print(traceback.format_exc())
    finally:
        sqlite_connection.close()


def insert_company_data(name: str, okved_code: str, inn: int, kpp: int, place_registration: str):
    sqlite_connection = connection_db()
    try:
        sql_query = f""" INSERT INTO company (name, okved_code, inn, kpp, place_registration) 
                    VALUES ('{name}', '{okved_code}', {inn}, {kpp}, '{place_registration}')"""
        cursor = sqlite_connection.cursor()
        cursor.execute(sql_query)
        sqlite_connection.commit()
        cursor.close()
    except:
        print(traceback.format_exc())
    finally:
        sqlite_connection.close()
