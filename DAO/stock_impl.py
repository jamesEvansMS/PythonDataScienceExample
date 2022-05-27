
import pandas.io.sql as sqlio

from config.postgresConfig import db_connect


class db_dao:

	def __init__(self):
		pass
	def execute_table_select(self):

		db=db_connect()
		db_conn=db.connect()

		query = "select * from data_science.stock_data order by Id"
		try:
			dat=sqlio.read_sql_query(query,db_conn)

		except Exception as e:
			return str(e) + " execute_table_select"

		return dat

