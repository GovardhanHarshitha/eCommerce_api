import secrets

from db.DBConnection import connect_db, disconnect_db
from jose import jwt, JWTError
from datetime import datetime
# from datetime import datetime, timedelta

import binascii
import os

# ------------------------------------------   AUTHENTICATION   --------------------------------------------------------

SECRET_KEY = binascii.hexlify(os.urandom(32)).decode()
ALGORITHM = "HS256"

# Encode the USER details
# def get_user_token(email, password):
#     hostname = socket.gethostname()  # System Name
#     ip_address = socket.gethostbyname(hostname)
#
#     data = {
#         'username': email,
#         'password': password,
#         "ipaddress": ip_address
#     }
#     to_encode = data.copy()
#
#     # expire time of the token
#     # expire = datetime.utcnow() + timedelta(minutes=15)
#     # to_encode.update({"exp": expire})
#
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#
#     token = encoded_jwt
#     return token # {'token': token}


def get_user_token():
    return secrets.token_hex(16)


# Decript USER Details
def verify_token(token: str):
    try:
        # try to decode the token, it will
        # raise error if the token is not correct
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        return str(e)


def getall_users():
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = "select * from users"
        cur.execute(query)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(e)
        return []


def update_user(idx, username, email, password):
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = "update users set username=%s,email=%s,password=%s where id=%s"
        args = [username, email, password, idx]
        result = cur.execute(query, args)
        disconnect_db(conn)
        if result > 0:
            return True
        else:
            return False
    except Exception as e:
        print(str(e))
        return False

def update_password(email, password):
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = "update users set password=%s where email=%s"
        args = [password, email]
        result = cur.execute(query, args)
        disconnect_db(conn)
        if result >= 0:
            return {"status": 200, "data": "New Password updated Successfully."}
        else:
            return False
    except Exception as e:
        print(str(e))
        return False

def createuser(username, email, password):
    try:
        chk1 = email
        chk2 = password

        conn = connect_db()
        cursor = conn.cursor()

        if (chk1 != "" and chk2 != ""):
            # Verification for Email Alredy Exist or not.
            query_string = "SELECT * FROM users WHERE email LIKE %s"
            cursor.execute(query_string, email)
            isEmail = cursor.fetchall()

            # Verification for Phone Number Alredy Exist or not.
            query_string = "SELECT * FROM users WHERE password LIKE %s"
            cursor.execute(query_string, password)
            isPwd = cursor.fetchall()

            if (isEmail.__len__() == 1 and isPwd.__len__() == 1):
                return {"status": 422, "data": "User Already Exists with " + chk1 + " Email and " + chk2 + " Password."}
            elif (isEmail.__len__() == 1):
                return {"status": 422, "data": "User Already Exists with " + chk1 + " Email."}
            elif (isPwd.__len__() == 1):
                return {"status": 422, "data": "User Already Exists with " + chk2 + " Password."}
            else:
                sql = "INSERT INTO `users` (`id`,`username`, `email`,`password`) VALUES (%s, %s, %s, %s)"
                args = ("NULL", username, email, password)

                cursor.execute(sql, args)
                conn.commit()

                return {"status": 200, "data": "New User added Successfully."}
    except Exception as e:
        print(str(e))


def delete_user(id):
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = "delete from users where id=%s"
        args = [id]
        result = cur.execute(query, args)
        disconnect_db(conn)
        if result > 0:
            return True
        else:
            return False
    except Exception as e:
        print(str(e))


def login(email, password):
    conn = connect_db()
    cursor = conn.cursor()

    query_string = "SELECT * FROM users WHERE email LIKE %s AND password LIKE %s"

    cursor.execute(query_string, [email, password])
    resp = cursor.fetchall()

    if (resp.__len__() > 0):
        getToken = get_user_token()
        saveToken(email, getToken)
        return {"status": 200, "auth_token": getToken}
    else:
        return {"status": 401, "data": "Invalid User Credentials."}

def saveToken(username, getToken):
    # current_datetime = datetime.now()
    # formatted_datetime = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
    # print(formatted_datetime)

    conn = connect_db()
    cursor = conn.cursor()


    query_string = "INSERT INTO `token` (`id`,`username`,`date`, `auth_token`) VALUES (%s, %s, %s, %s)"
    cursor.execute(query_string, ['NULL',username, datetime.now(), getToken])
    conn.commit()


def logout(Custom_header):
    conn = connect_db()
    cursor = conn.cursor()

    query_string = "DELETE FROM `token` WHERE `auth_token` = %s"
    cursor.execute(query_string, [Custom_header])
    conn.commit()
    return {"status": 200, "data": "Logout Successfully."}


def checkuser(email):
    conn = connect_db()
    cursor = conn.cursor()

    query_string = "SELECT * FROM users WHERE email=%s"

    cursor.execute(query_string, [email])
    resp = cursor.fetchall()

    return True if (resp.__len__() > 0) else False