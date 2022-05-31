import os
import psycopg2
import psycopg2.extras as extras
import pandas as pd
from config import postgresConfig

def rename_columns(df,**to_replace):
	#existing_name=df.columns.to_list()
	cur_names = df.columns.to_list()
	# print(cur_names)
	# print(to_replace)
	for key in to_replace:
		cur_names = cur_names
		for index,cName in enumerate(cur_names):
			print(index)
			print(cName)
			print(cur_names[index])
			cur_names[index]=cName.replace(key,to_replace[key])
			print(cur_names[index])
	for index,cName in enumerate(df.columns.to_list()):
		df.rename(columns={cName:cur_names[index]},inplace=True)
	return df

def execute_load_csv(conn, df, table):
	tuples = [tuple(x) for x in df.to_numpy()]
	to_replace={" ":"_","/":""}
	df=rename_columns(df,**to_replace)
	cols = ','.join(list(df.columns))

	query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
	curr = conn.cursor()
	try:
		extras.execute_values(curr, query, tuples)
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print("Error: %s" % error)

	curr.close()
	conn.close()
	return 1
	print("the dataframe is inserted")


def create_stock_table(conn,df):
	print(os.getcwd())
	to_replace={" ":"_","/":""}
	df=rename_columns(df,**to_replace)
	cols=df.columns.to_list()
	print(cols)
	sql='Create table data_science.stock_data (id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY \n'
	for cName in cols:
		sql = sql +','+cName + ' character varying(50)\n'
	sql =sql+')'
	print(sql)
	try:
		curr=conn.cursor()
		curr.execute(sql)
		curr.commit()
	except Exception as e:
		print(e)
		return e
	return 200

df=pd.read_csv("../stock_data.csv")
db_connect=postgresConfig.db_connect()
db_string=db_connect.config()
conn=psycopg2.connect(db_string)
curr=conn.cursor()
r=create_stock_table(conn,df)
execute_load_csv(conn,df,"data_science.stock_data")
