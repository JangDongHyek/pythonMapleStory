import pymysql

class DB :
    cur = None

    def orgSql(self,sql,bool = False):
        # bool이 True면 복수검색
        self.cur.execute(sql)
        result = self.cur.fetchall() if bool else self.cur.fetchone()
        return result

    def dictSelect(self,table, dict, addQuery="", bool=False, sort="_id", order="desc"):
        # bool이 True면 복수검색

        sql = "select * from {} where ".format(table)

        index = 0
        for item in dict:
            if index < 1:
                sql += "{} = '{}'".format(item, dict[item])
            else:
                sql += " and {} = '{}'".format(item, dict[item])
            index += 1

        sql += addQuery

        if bool:
            sql += " order by {} {}".format(sort, order)

        self.cur.execute(sql)
        result = self.cur.fetchall() if bool else self.cur.fetchone()
        return result

    def __init__(self):
        db_host = "13.125.209.62"
        db_user = "test"
        db_password = "141215"
        db_name = "maple"

        # DB연결
        try:
            conn = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name, charset='utf8')
            self.cur = conn.cursor(pymysql.cursors.DictCursor)
        except:
            print("DB연결실패")
            exit()