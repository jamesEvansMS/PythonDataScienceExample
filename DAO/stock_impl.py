
import pandas.io.sql as sqlio


def execute_table_select(conn):

	query = "select * from data_science.stock_data order by Id"
	try:
		dat=sqlio.read_sql_query(query,conn)
		print(type(dat))
	except Exception as e:
		return e + " execute_house_select"

	return dat.to_json()


