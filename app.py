from flask import Flask

from DAO.stock_impl import execute_table_select
from config import postgresConfig

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/tabledata')
def get_table_data():
    conn=postgresConfig.connect()
    return execute_table_select(conn)

if __name__ == '__main__':
    app.run()
