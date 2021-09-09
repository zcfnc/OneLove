import json
import pymysql
from dbutils.pooled_db import PooledDB, SharedDBConnection
from urllib.parse import urlparse
'''
数据库添加日志模块记录操作并定时清空
'''
class MysqlPool(object):

    def __init__(self, configFile):
        with open(configFile,'r') as file:
            confStr = file.read()
        conf = json.JSONDecoder().decode(confStr)
        self.POOL = PooledDB(
            creator=pymysql,
            maxconnections=10, # 连接池的最大连接数
            maxcached=10,
            maxshared=10,
            blocking=True,
            setsession=[],
            host=conf['hostname'],
            port=conf['port'],
            user=conf['username'],
            password=conf['password'],
            database=conf['database'],
            charset='utf8',
        )
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def connect(self):
        conn = self.POOL.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        return conn, cursor

    def connect_close(self,conn, cursor):
        cursor.close()
        conn.close()

    def fetch_one(self,sex) :
        '''
        :param args:
        :return:
        '''
        # sql = '''select * from userinfo where sex= '{}' limit 1'''.format(sex)
        sql = '''SELECT * FROM  userinfo WHERE sex = '{}' 
        and  id >= ((SELECT MAX(id) FROM userinfo )-(SELECT MIN(id) FROM userinfo )) * RAND() 
        + (SELECT MIN(id) FROM userinfo )  LIMIT 1'''.format(sex)

        print(sql)
        conn, cursor = self.connect()
        cursor.execute(sql)
        result = cursor.fetchone()
        # 取出的该条进行删除
        id =result['id']
        self.delete_one(id)
        return result['wechat']

    def delete_one(self,id):
        conn, cursor = self.connect()
        sql = '''delete from userinfo where id = {}'''.format(id)
        print(sql)
        row = cursor.execute(sql)
        conn.commit()
        self.connect_close(conn, cursor)
        return row


    def insert_one(self, sex,wechat,want_sex):
        '''
        :param args: (sex,wechat,want_sex)
        :return:
        '''
        conn, cursor = self.connect()
        sql = '''insert into userinfo(sex,wechat,want_sex) values ('{}','{}','{}')'''.format(sex,wechat,want_sex)
        print(sql)
        row = cursor.execute(sql)
        conn.commit()
        self.connect_close(conn, cursor)
        return row

if __name__ == '__main__':
    pool = MysqlPool('config.json')
    # result = pool.insert_one('man','ironman','female')
    result = pool.fetch_one('man')
    print(result)