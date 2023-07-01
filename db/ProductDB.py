from db.DBConnection import connect_db, disconnect_db


def getall_products():
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = "select * from products"
        cur.execute(query)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(e)
        return []


def createproduct(product_name, price, quantity):
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = "insert into products(product_name,price,quantity) values(%s,%s,%s)"
        args = [product_name, price, quantity]
        cur.execute(query, args)
        lastrowid = cur.lastrowid
        disconnect_db(conn)
        return lastrowid
    except Exception as e:
        print(str(e))


def update_product(id, product_name, price, quantity):
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = "update products set product_name=%s,price=%s,quantity=%s where id=%s"
        args = [product_name, price, quantity, id]
        result = cur.execute(query, args)
        disconnect_db(conn)
        if result > 0:
            return True
        else:
            return False
    except Exception as e:
        print(str(e))
        return False

def delete_product(id):
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = "delete from products where id=%s"
        args = [id]
        result = cur.execute(query, args)
        disconnect_db(conn)
        if result > 0:
            return True
        else:
            return False
    except Exception as e:
        print(str(e))





