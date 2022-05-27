import os
import psycopg2
from configparser import ConfigParser
import sqlalchemy
from sqlalchemy.orm import sessionmaker

class db_connect:

    def __init__(self):
        pass


    def config(self,filename='database.ini', section='database'):
        print(os.getcwd())
        parser = ConfigParser()
        parser.read(filename)

        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
            print("file not found")

        db_string=url = f"postgresql://{db.get('user')}:{db.get('password')}@{db.get('host')}:{db.get('port')}/{db.get('database')}"
        return db_string

    def connect(self):
        """ Connect to the PostgreSQL database server """
        conn=db_connect()
        try:

            db_string = conn.config(filename='database.ini', section='database')
            db = sqlalchemy.create_engine(db_string)
            return db
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
