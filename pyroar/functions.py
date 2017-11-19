from pyroar.classes import *

def getAccount(username, password=None):
    if password != None:
        raise CreationError('An Account with a password cannot be created.')
    return Account(username)

def getRoom(roomid):
    return Room(roomid)
