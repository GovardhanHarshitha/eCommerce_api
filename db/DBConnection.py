import pymysql


def connect_db():
    try:
        conn = pymysql.connect(host="localhost",
                               user="root",
                               password="root",
                               charset='utf8mb4',
                               db="ecommerce",
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