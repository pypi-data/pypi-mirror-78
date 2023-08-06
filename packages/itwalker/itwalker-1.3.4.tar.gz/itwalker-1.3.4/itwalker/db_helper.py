import pymysql
from DBUtils.PooledDB import PooledDB

Log = None


class Singleton(object):
    def __new__(cls, conf, log):
        db = conf.get("db", "")
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            obj = orig.__new__(cls)
            obj.POOL = PooledDB(pymysql, maxconnections=10, setsession=["SET GLOBAL time_zone = '+8:00'"], **conf)
            cls._instance = {db: obj}
        else:
            if db not in cls._instance:
                orig = super(Singleton, cls)
                obj = orig.__new__(cls)
                obj.POOL = PooledDB(pymysql, maxconnections=10, setsession=["SET GLOBAL time_zone = '+8:00'"], **conf)
                cls._instance[db] = obj
        return cls._instance[db]


class MysqlHelper(Singleton):
    def __new__(cls, conf, log):
        return super(MysqlHelper, cls).__new__(cls, conf, log)

    def __init__(self, conf, log):
        self.Log = log

    def createConn(self):
        # 创建引擎
        conn = self.POOL.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cursor

    def executeParam(self, cursor, sql, Param):
        if Param:
            Param = Param[0]
        else:
            Param = None
        if isinstance(Param, dict):
            return cursor.execute(sql, Param)
        elif isinstance(Param, tuple):
            return cursor.execute(sql % Param)
        else:
            return cursor.execute(sql)

    def Query(self, sql, *Param):
        try:
            self.Log.debug(sql)
            conn, cursor = self.createConn()
            # print(Param)
            self.executeParam(cursor, sql, Param)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            if len(result) > 0:
                flag = False
                for k, v in result[0].items():
                    if not v is None:
                        flag = True
                        break
                if flag:
                    return result
                else:
                    return None
            else:
                return None
        except Exception as e:
            self.Log.error(e.args[:])
            raise Exception(e.args[:])

    def QuerySingle(self, sql, *Param):
        try:
            self.Log.debug(sql)
            conn, cursor = self.createConn()
            self.executeParam(cursor, sql, Param)
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result:
                flag = False
                for k, v in result.items():
                    if not v is None:
                        flag = True
                        break
                if flag:
                    return result
                else:
                    return None
            else:
                return None
        except Exception as e:
            self.Log.error(e.args[:])
            raise Exception(e.args[:])

    def ExcuteSql(self, sql, *Param):
        conn = None
        try:
            self.Log.debug(sql)
            conn, cursor = self.createConn()
            result = self.executeParam(cursor, sql, Param)
            conn.commit()
            cursor.close()
            conn.close()
            if result > 0:
                return True
            else:
                return False
        except Exception as e:
            conn.rollback()
            self.Log.error(e.args[:])
            raise Exception(e.args[:])

    def ExecuteMany(self, sql, Param):
        conn = None
        try:
            self.Log.debug(sql)
            if not isinstance(Param, list):
                raise Exception("Param must is list")
            else:
                conn, cursor = self.createConn()
                result = cursor.executemany(sql, Param)
                conn.commit()
                cursor.close()
                conn.close()
                if result > 0:
                    return True
                else:
                    return False
        except Exception as e:
            conn.rollback()
            self.Log.error(e.args[:])
            raise Exception(e.args[:])
