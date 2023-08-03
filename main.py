import os
import uuid
import uvicorn
import socket
from fastapi import FastAPI, File, UploadFile, Header
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from controller import UserController, ProductController
from db.DBConnection import connect_db, disconnect_db

app = FastAPI()

# Enable Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# ------------------------------------------   IPAddress   -------------------------------------------------------------
"""
Get the IP address of the system:
--------------------------------
"""
@app.get("/getIPAddress", tags=["IP Address"])
async def get_system_ip():
    hostname = socket.gethostname()  # System Name
    ip_address = socket.gethostbyname(hostname)
    return {"ipaddress": ip_address}


# ------------------------------------------   TOKEN   -----------------------------------------------------------------

""" 
Get a token for authentication:
------------------------------
"""

@app.get("/getDBToken", tags=["TOKEN"])
def get_db_token():
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = "select * from token"
        cur.execute(query)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(e)
        return ""

# ------------------------------------------   TOKEN VALIDATION   ------------------------------------------------------


def validate_token(token):
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = "SELECT * FROM token WHERE auth_token=%s"
        resp = cur.execute(query, [token])
        if resp == 1:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

# ------------------------------------------   USERS   --------------------------------------------------------


""" 
Get all users:
-------------
"""
@app.get("/getallusers", tags=["USERS"])
async def getall_users():
    return UserController.getall_users()


""" 
Create a new user:
-----------------
"""
@app.post("/register", tags=["USERS"])
async def createuser(username: str, email: str, password: str):
    return UserController.createuser(username, email, password)


""" 
User login:
----------
"""
@app.get("/login", tags=["USERS"])
def is_login(email, password):
    return UserController.login(email, password)

""" 
User logout:
-----------
"""
@app.get("/logout", tags=["USERS"])
def is_logout(Custom_header: str = Header(...)):
    if validate_token(Custom_header):
        return UserController.logout(Custom_header)
    else:
        return {"status": 401, "data": "Invalid Authorization"}

""" 
Update Password:
-------------
"""
@app.post("/updatepassword", tags=["USERS"])
async def update_password(email: str, password: str):
    if UserController.checkuser(email):
        return UserController.update_password(email, password)
    else:
        return {"status": 401, "data": "User not Found"}



""" 
Update a user:
-------------
"""
@app.post("/updateuser", tags=["USERS"])
async def update_user(idx: int, username: str, email: str, password: str, Custom_header: str = Header(...)):
    if validate_token(Custom_header):
        return UserController.update_user(idx, username, email, password)
    else:
        return {"status": 401, "data": "Invalid Authorization"}

""" 
Delete a user:
-------------
"""
@app.post("/deleteuser", tags=["USERS"])
async def delete_user(idx: int, Custom_header: str = Header(...)):
    if validate_token(Custom_header):
        return UserController.delete_user(idx)
    else:
        return {"status": 401, "data": "Invalid Authorization"}

# ------------------------------------------   PRODUCTS   --------------------------------------------------------------

""" 
Get product information:
-----------------------
"""
@app.get("/getProductinfo", tags=["PRODUCTS"])
async def get_product_info(Custom_header: str = Header(...)):
    if validate_token(Custom_header):
        return {"status": 200, "data": ProductController.getall_products()}
    else:
        return {"status": 401, "data": "Invalid Authorization"}

""" 
Create a new product:
--------------------
"""
@app.post("/createproduct", tags=["PRODUCTS"])
async def createproduct(product_name: str, price: str, quantity: str, Custom_header: str = Header(...)):
    if validate_token(Custom_header):
        return ProductController.createproduct(product_name, price, quantity)
    else:
        return {"status": 401, "data": "Invalid Authorization"}

""" 
Update a product:
----------------
"""
@app.post("/updateproduct", tags=["PRODUCTS"])
async def update_product(idx: int, product_name: str, price: str, quantity: str, Custom_header: str = Header(...)):
    if validate_token(Custom_header):
        return ProductController.update_product(idx, product_name, price, quantity)
    else:
        return {"status": 401, "data": "Invalid Authorization"}

""" 
Delete a product:
----------------
"""
@app.post("/deleteproduct", tags=["PRODUCTS"])
async def delete_product(idx: int, Custom_header: str = Header(...)):
    if validate_token(Custom_header):
        return ProductController.delete_product(idx)
    else:
        return {"status": 401, "data": "Invalid Authorization"}

# ------------------------------------------   CUSTOMERS   -------------------------------------------------------------

IMAGEDIR = "static/images/"

""" 
Get customer information:
------------------------
"""
@app.get("/getcustomers", tags=["CUSTOMERS"])
async def get_customers(Custom_header: str = Header(...)):
    if validate_token(Custom_header):
        conn = connect_db()
        cur = conn.cursor()
        query = "select * from customers"
        cur.execute(query)
        rows = cur.fetchall()
        data_arr = []
        for i in range(0, rows.__len__()):
            data_dict = {
                'id': rows[i]["id"],
                'name': rows[i]["name"],
                'phone': rows[i]["phone"],
                'city': rows[i]["city"],
                'photo': "" if (rows[i]["photo"] == "") else "/static/images/" + rows[i]["photo"]

            }
            data_arr.append(data_dict)
        return {"status": 200, "data": data_arr}
    else:
        return {"status": 401, "data": "Invalid Authorization"}

""" 
Create a new customer :
---------------------
"""
@app.post("/createcustomer", tags=["CUSTOMERS"])
async def create_customer(name: str, phone: str, city: str, file: UploadFile = File(...), Custom_header: str = Header(...)):
    if validate_token(Custom_header):
        conn = connect_db()
        cursor = conn.cursor()

        file.filename = f"{uuid.uuid4()}.jpg"
        contents = await file.read()

        with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
            f.write(contents)

        sql = "INSERT INTO `customers` (`id`, `name`, `phone`, `city`, `photo`) VALUES (NULL, %s, %s, %s, %s)"
        args = (name, phone, city, file.filename)

        cursor.execute(sql, args)
        conn.commit()
        disconnect_db(conn)

        return {"name": name, "phone": phone, "city": city, "filename": file.filename}
    else:
        return {"status": 401, "data": "Invalid Authorization"}

""" 
Update customer photo:
---------------------
"""
@app.post("/updatephoto", tags=["CUSTOMERS"])
async def update_photo(idx: int, name: str, phone: str, city: str, file: UploadFile = File(...), Custom_header: str = Header(...)):
    if validate_token(Custom_header):
        conn = connect_db()
        cur = conn.cursor()
        query = "SELECT * FROM `customers` WHERE id = %s"
        args = idx
        cur.execute(query, args)
        resp = cur.fetchall()
        get_img = resp[0]['photo']

        folder_path = IMAGEDIR + get_img

        image_path = f"{folder_path}"

        if os.path.exists(image_path):
            if get_img != "":
                os.remove(image_path)

            file.filename = f"{uuid.uuid4()}.jpg"
            contents = await file.read()

            with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
                f.write(contents)

            query = "update customers set name=%s, phone=%s, city=%s, photo=%s where id=%s"
            args = (name, phone, city, file.filename, idx)

            cur.execute(query, args)
            conn.commit()
            disconnect_db(conn)

            return {"message": f"Image {get_img} updated successfully."}
        else:
            return {"message": f"Image {get_img} not found."}
    else:
        return {"status": 401, "data": "Invalid Authorization"}

""" 
Remove customer photo:
---------------------
"""
@app.post("/removephoto", tags=["CUSTOMERS"])
async def remove_photo(idx: int,Custom_header: str = Header(...)):
    if validate_token(Custom_header):
        conn = connect_db()
        cur = conn.cursor()
        query = "SELECT * FROM `customers` WHERE id = %s"
        args = idx
        cur.execute(query, args)
        resp = cur.fetchall()
        get_img = resp[0]['photo']

        folder_path = IMAGEDIR + get_img

        image_path = f"{folder_path}"

        if os.path.exists(image_path):
            os.remove(image_path)  # Remove image from the folder.
            query = "DELETE FROM customers WHERE `customers`.`id` = %s"
            args = idx
            cur.execute(query, args)
            disconnect_db(conn)
            return {"message": f"Image {get_img} deleted successfully."}
        else:
            return {"message": f"Image {get_img} not found."}
    else:
        return {"status": 401, "data": "Invalid Authorization"}

@app.get("/getIdx", tags=["TEST"])
def getIdx(number: int):
    myArray = [
        331, 611, 422, 551, 521, 541, 331, 542, 442, 544, 542, 542, 643, 332, 432, 653,
        533, 421, 621, 662, 543, 643, 541, 532, 521, 543, 654, 431, 432, 621, 531, 322,
        611, 661, 611, 664, 553, 621, 665, 551, 665, 553, 311, 665, 642, 541, 644, 543,
        651, 631, 631, 442, 611, 421, 621, 441, 443, 322, 411, 643, 541, 542, 644, 531,
        663, 221, 442, 522, 655, 511, 643, 666, 411, 643, 641, 661, 542, 543, 421, 541,
        532, 321, 222, 641, 642, 633, 662, 654, 543, 541, 611, 332, 521, 632, 551, 441,
        422, 322, 663, 653, 652, 431, 643, 521, 641, 433, 633, 651, 521, 641, 643, 431,
        611, 322, 511, 552, 442, 632, 643, 655, 553, 111, 621, 543, 641, 633, 533, 432,
        541, 551, 541, 543, 654, 641, 531, 662, 662, 644, 521, 653, 651, 541, 221, 654,
        431, 522, 551, 432, 655, 521, 221, 351, 411, 652, 663, 653, 652, 421, 642, 551,
        333, 431, 422, 622, 553, 642, 666, 621, 531, 222, 663, 653, 633, 652, 643, 542,
        543, 654, 652, 431, 633, 551, 555, 522, 311, 542, 652, 441, 666, 611, 521, 532,
        522, 432, 222, 331, 321, 651, 666, 665, 654, 441, 544, 432, 533, 331, 652, 664,
        554, 542, 662, 653, 621, 633, 442, 542, 521, 654, 444, 653, 553, 433, 641, 531,
        431, 653, 221, 433, 443, 542, 431, 633, 631, 542, 541, 621, 553, 641, 633, 221,
        651, 443, 661, 652, 552, 653
    ]

    my_list = []
    for index,num in enumerate(myArray):
        if check_same_digits(num):
            my_list.append(myArray[index + 1])
        if num == number:
            my_list.append(myArray[index + 1])
    return my_list

def check_same_digits(number):
    number_str = str(number)
    first_digit = number_str[0]
    for digit in number_str:
        if digit != first_digit:
            return False

    return True


# Run the FastAPI application using Uvicorn server when the script is executed directly


if __name__ == '__main__':
    uvicorn.run(app)
