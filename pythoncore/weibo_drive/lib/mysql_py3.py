#mysql fro offical. use setup.py to install it.
import mysql.connector

class mysql_db:
    _conn = None
    _cur = None
    _conf = None
    
    error_code = 0
    error_msg = ""
    
    def __init__(self, host = '127.0.0.1', port = '3306', user = 'root', password = '', dbname = '', charset = 'utf8'):
    #TODO: check config...
        config = {"host" : host, "port" : port, "user" : user, "password" : password, "dbname" : dbname, "charset" :  charset}
        self._conf = config
        self._get_conn(config)
        
    def _get_conn(self, config):
        try:
            self._conn = mysql.connector.connect(host = config["host"],
                                                 port = config["port"],
                                                 user = config["user"],
                                                 passwd = config["password"],
                                                 db = config["dbname"],
                                                 charset = config["charset"])
            self._cur = self._conn.cursor()
        except Exception:
            raise
    
    def _print_error(self):
        print ("Error Code: " + str(self.error_msg) + ", message is: " + self.error_msg)
        
    def close_conn(self):
        if self._cur is not None:
            self._cur.close()
        if self._conn is not None:
            self._conn.close()
            
    def query(self, sql):
        results = None
        try:
            self._cur.execute(sql)
            results = self._cur.fetchall()
            columns = self._cur.description 
            return [{columns[index][0]:column for index, column in enumerate(value)} for value in results]
        except Exception as e:
            self.error_code = e.args[0]
            self.error_msg = e.args[1]
            self._print_error()
        return results
    
    def insert(self, table_name, data):
        in_data = []
        for val in data.values():
            in_data.append("'" + val.replace("'", "\"") + "'")
        sql = "INSERT INTO " + table_name + " (" + ",".join(data.keys()) + ") VALUES (" + ",".join(in_data) + ')'
        print (sql)
        self._cur.execute(sql)
        self._conn.commit()
        
if __name__=='__main__':
    #pwd for example.
    DB = mysql_db(password = 'innovation', dbname = "userdata")
    DB.insert('userinfo', {'name': '天使动漫谐星战术研究院'})