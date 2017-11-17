from pyroar.classes import *

def getAccount(username, password=None):
    if password == None:
        return Account(username)
    else:
        return LoginAccount(username, password)

def getRoom(roomid):
    return Room(roomid)
