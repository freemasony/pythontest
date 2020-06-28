import pymysql as pymysql


class DataBase:
    def __index__(self, host, port, username, password, database):
        self.db = pymysql.connect(host=host, port=port, user=username, password=password, db=database,
                                  charset='utf8')
        # 设置游标字典
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
