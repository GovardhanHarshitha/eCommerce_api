import pymysql


def connect_db():
    try:
        # conn = pymysql.connect(host="localhost",
        #                        user="root",
        #                        password="root",
        #                        charset='utf8mb4',
        #                        db="ecommerce",
        #                        cursorclass=pymysql.cursors.DictCursor)
        conn = pymysql.connect(host="sql9.freesqldatabase.com",
                               user="sql9637478",
                               password="EmLlGwxJGx",
                               charset='utf8mb4',
                               db="sql9637478",
                               cursorclass=pymysql.cursors.DictCursor)
        print(conn)
        return conn
    except Exception as e:
        print(str(e))

def disconnect_db(conn):
    try:
        if conn != None:
            conn.commit()
            conn.close()
    except Exception as e:
        print(str(e))

#connect_db()
