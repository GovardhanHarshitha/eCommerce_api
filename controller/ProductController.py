from db import ProductDB


def getall_products():
    return ProductDB.getall_products()


def createproduct(product_name, price, quantity):
    return ProductDB.createproduct(product_name, price, quantity)


def update_product(id, product_name, price, quantity):
    return ProductDB.update_product(id, product_name, price, quantity)


def delete_product(id):
    return ProductDB.delete_product(id)


