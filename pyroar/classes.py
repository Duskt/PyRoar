import aiohttp, json, asyncio

class Room():
    def __init__(self, roomid):
        self.roomid = roomid

class Account():
    def __init__(self, username):
        if username.lower() != username:
            raise CreationError('Username cannot be a nickname.')
        else:
            for i in username:
                if not i in list('abcdefghijklmnopqrstuvwxyz1234567890'):
                    raise CreationError('Username cannot be a nickname.')
                    break
            else:
                self.username = username

class LoginAccount():
    def __init__(self, username, password):
        if username.lower() != username:
            raise CreationError('Username cannot be a nickname.')
        else:
            for i in username:
                if not i in list('abcdefghijklmnopqrstuvwxyz1234567890'):
                    raise CreationError('Username cannot be a nickname.')
                    break
            else:
                self.username = username
        self.password = password

class User(Account):
    def __init__(self, cmddict):
        self.username = cmddict['userid']
        self.avatar = cmddict['avatar']
        self.rooms = list(cmddict['rooms'].keys())
        self.ranks = dict()
        for index, room in enumerate(self.rooms):
            if room[0] in list('+%@*#&~'):
                rank = room[0]
                self.ranks[room[1:]] = rank
                self.rooms[index] = room[1:]
            else:
                rank = ''
                self.ranks[room] = rank
        self.global_rank = cmddict['group']

class Message():
    def __init__(self, text, author=None, roomid=None, timestamp=None):
        self.text = text
        self.author = author
        if roomid != None:
            self.room = Room(roomid)
        self.timestamp = timestamp
            
class Event():
    def __init__(self, eventid, func):
        self.eventid = eventid
        self.func = func

class Request():
    def __init__(self, request, info):
        self.request = request
        self.response = None
        if type(info) == tuple:
            self.info = [i for i in info]
        else:
            self.info = [info]

#is this is even used??
class Task():
    def __init__(self, func, info):
        self.func = func
        if type(info) == tuple:
            self.info = [i for i in info]
        else:
            self.info = [info]

class CreationError(Exception):
    pass

class SendError(Exception):
    pass
