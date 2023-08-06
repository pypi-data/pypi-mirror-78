from ..py_api_b import PyApiB
# pip install PyMySQL
import pymysql
import pymysql.cursors


class MysqlDBU(PyApiB):
    """
    mysql数据库操作工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
      
    def init(self, host, port, user, pswd, dbName, charset):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pswd, db=dbName,charset=charset)
        return self
      
    def rollback(self):
        """ 回滚 """
        self.conn.rollback()
        
    def commit(self):
        """ 提交 """
        self.conn.commit()
      
    def _get_cursor(self, type='stream'):
        """ 获取光标，用于输入命令 """
        if type == 'stream':
            return self.conn.cursor(pymysql.cursors.SSCursor)  # 返回流式游标,查询大量数据时不占用内存(返回数据形式是元组)
        elif type == 'dict':
            return self.conn.cursor(pymysql.cursors.DictCursor)  # 返回字典形式游标,查询出的数据以字典形式返回
        elif type == 'default':
            return self.conn.cursor()
        else:
            raise Exception("cursor type error")
    
    def execute_sql(self, sql, commit=False, type='stream'):
        """ sql语句 """
        # self._get_cursor()
        pass