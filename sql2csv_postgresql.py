#!/usr/bin/python
"""
connects to a database
reads all .sql files of current directory
excecutes one after the other
results are written to .csv files

ONLY USE READ-ONLY DB-USER ACCOUNTS via:
GRANT SELECT ON ALL TABLES IN SCHEMA schema_name TO username
"""

# Convert to .exe via
# pyinstaller --onefile --console sql2csv_postgresql.py

# FIXME: this security check is not working
# if (sql1.find('insert') or sql1.find('update') or sql1.find('delete') or sql1.find('drop') or sql1.find('grant')):
#     print ("invalid SQL")
#     sys.exit(1)


import os
import glob
import psycopg2


def connect():
    """ Connect to the PostgreSQL database server """
    connection = None
    cursor = None
    try:
        credentials_MyDB1 = {'host': 'myHost', 'port': 5432,
                                     'database': 'myDB', 'user': 'myUser', 'password': 'myPwd'}
        credentials = credentials_MyDB1
        connection = psycopg2.connect(**credentials)
        cursor = connection.cursor()
        print(
            f"connected to database {credentials['database']} on host {credentials['host']}")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    return connection, cursor


def sql2csv(cursor, sql: str, outfile: str = 'out.csv'):
    """ Excecute SQL statement and write results into csv file """
    try:
        sql2 = "COPY (" + sql + ") TO STDOUT WITH CSV HEADER DELIMITER ';'"
        with open(outfile, "w") as fhOut:
            cursor.copy_expert(sql2, fhOut)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


if __name__ == '__main__':
    (connection, cursor) = connect()
    for filename in glob.glob("*.sql"):
        print(f'File: {filename}')
        fh = open(filename, "r")
        sql = fh.read()
        fh.close()
        (fileBaseName, fileExtension) = os.path.splitext(filename)
        sql2csv(cursor, sql, fileBaseName+'.csv')

    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection closed")
