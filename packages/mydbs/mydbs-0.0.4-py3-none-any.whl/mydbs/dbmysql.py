import pymysql
import sys
from configparser import ConfigParser
import xml.etree.ElementTree as Et
from functools import wraps

conf = ConfigParser()
conf.read('mydbs.ini')

xml_file = open('sql.xml')
tree = Et.parse(xml_file)
root = tree.getroot()

def error_report(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print('Error! '+str(e))
        return result
    return wrapper

class MySql():

    @error_report
    def __init__(self, name = '', pwd = '', db_name = ''):
        """
        初始化参数
        :param name: 用户名 
        :param pwd: 用户密码
        :param db_name: 使用的数据库名称
        """
        self.host = conf.get('mysql', 'host')
        self.name = name
        self.port = int(conf.get('mysql', 'port'))
        self.pwd = pwd
        self.db_name = db_name
        self.charset = conf.get('mysql', 'charset')
        self.conn = pymysql.connect(host=self.host,
                                    user=name,
                                    port=self.port,
                                    password=pwd,
                                    database=db_name,
                                    charset=self.charset)

        self.cursor = self.conn.cursor()

    @error_report
    def show_databases(self):
        """
        列出所有现存数据库
        :return: 数据库名称列表
        """
        sql = root.find(sys._getframe().f_code.co_name).text
        self.cursor.execute(sql)
        return [ele[0] for ele in self.cursor.fetchall()]

    @error_report
    def use_database(self,
                     db_name = ''):
        """
        切换数据库
        :param db_name:数据库名称
        :return: 0为执行成功
        """
        sql = root.find(sys._getframe().f_code.co_name).text
        return self.cursor.execute(sql % db_name)

    @error_report
    def create_database(self,
                        db_name = ''):
        """
        创建新数据库
        :param db_name:数据库名称
        :return: 0为执行成功
        """
        sql = root.find(sys._getframe().f_code.co_name).text
        return self.cursor.execute(sql%db_name)

    @error_report
    def drop_database(self,
                      db_name =''):
        """
        删除数据库
        :param db_name:数据库名称
        :return: 0为执行成功
        """
        sql = root.find(sys._getframe().f_code.co_name).text
        return self.cursor.execute(sql % db_name)

    @error_report
    def show_tables(self):
        """
        列出数据库中所有现存表
        :return: 0为执行成功 
        """
        sql = root.find(sys._getframe().f_code.co_name).text
        self.cursor.execute(sql)
        return [ele[0] for ele in self.cursor.fetchall()]

    @error_report
    def desc_table(self,
                   table_name =''):
        """
        列出表的结构    
        :param table_name: 表名称 
        :return: 表的结构表
        """
        sql = root.find(sys._getframe().f_code.co_name).text
        self.cursor.execute(sql % table_name)
        return [ele for ele in self.cursor.fetchall()]

    @error_report
    def create_table(self,
                     table_name = '',pri_key_name = '',
                     engine = 'InnoDB', charset = 'utf8',
                     **value_dict):
        """
        创建新表
        :param table_name: 数据表名称 
        :param pri_key_name: 主键名称
        :param engine: 数据库引擎
        :param charset: 数据库字符集
        :param value_dict: 关键字与数据类型键值对字典
        :return: 0为执行成功
        """
        value_content = ''
        sql = root.find(sys._getframe().f_code.co_name).text
        for k, v in value_dict.items():
            value_content += k + ' ' + v + ' NOT NULL,'
        return self.cursor.execute(sql % (table_name, value_content, pri_key_name, engine, charset))

    @error_report
    def drop_table(self,
                   table_name = ''):
        """
        删除数据表
        :param table_name: 数据表名称
        :return: 0为执行成功
        """
        sql = root.find(sys._getframe().f_code.co_name).text
        return self.cursor.execute(sql % table_name)

    @error_report
    def select(self,
               table_name='', columns='*'):
        """
        选择
        :param table_name: 数据表名称 
        :param columns: 选择的关键字
        :return: 所选择的结果
        """
        sql = root.find(sys._getframe().f_code.co_name).text
        self.cursor.execute(sql%(columns, table_name))
        return [ele for ele in self.cursor.fetchall()]

    @error_report
    def select_where(self,
                     columns = '*', table_name = '', where_clause = ''):
        """
        带条件的选择
        :param columns: 选择的关键字 
        :param table_name: 数据表名称
        :param where_clause: 条件语句
        :return: 所选择的结果
        """
        sql = root.find(sys._getframe().f_code.co_name).text
        self.cursor.execute(sql % (columns, table_name, where_clause))
        return [ele for ele in self.cursor.fetchall()]

    @error_report
    def insert(self, table_name = '', fields = tuple(), values = tuple()):
        """
        插入数据
        :param table_name: 数据表名称 
        :param fields: 关键字元组
        :param values: 对应的值元组
        :return: 0表示执行成功
        """
        sql = root.find(sys._getframe().f_code.co_name).text
        str_fields = ''
        str_values = ''
        for i in range(len(fields) - 1):
            str_fields += str(fields[i]) + ','
        str_fields += str(fields[-1])
        for i in range(len(values) - 1):
            str_fields += str(values[i]) + ','
        str_values += str(values[-1])
        if self.cursor.execute(sql % (table_name, str_fields, str_values)):
            self.conn.commit()
            return 0
        else:
            return 1