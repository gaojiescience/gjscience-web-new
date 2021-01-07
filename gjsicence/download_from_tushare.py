import tushare as ts
import pymysql

pro = ts.pro_api(token="df36b05825c5f945cdd1b566f85f69d6db45e597765a0bdc9f616f44")

connect = pymysql.connect(
	host = "localhost",
	user = "root",
	password = "123456",
	database = "gjscience",	
)
cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)

def download (symbol, date, param):
	sql = "SELECT exchange FROM server_stock WHERE symbol = %s;" % symbol
	cursor.execute(sql)
	res = "SZ" if cursor.fetchall()[0]["exchange"] == "SZSE" else "SH"
	data = pro.fina_indicator(ts_code=symbol+"."+res, start_date=date, end_date=date, fields=param).to_dict(orient='dict')
	return data[param][0]
