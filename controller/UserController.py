from db import UserDB


def getall_users():
    return UserDB.getall_users()


def update_user(id, username, email, password):
    return UserDB.update_user(id, username, email, password)

def update_password(email, password):
    return UserDB.update_password(email,password)

def createuser(username, email, password):
    return UserDB.createuser(username, email, password)


def delete_user(id):
    return UserDB.delete_user(id)


def login(email, password):
    return UserDB.login(email,password)

def logout(Custom_header):
    return UserDB.logout(Custom_header)


def checkuser(email):
    return UserDB.checkuser(email)