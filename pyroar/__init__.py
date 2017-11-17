import aiohttp, json, asyncio, time
import pyroar.handler, pyroar.utils
from pyroar.classes import *
from pyroar.functions import *

#This is a package designed to make PS bots much simpler
#import pyroar

URL = 'ws://sim.smogon.com:8000/showdown/websocket'

'''
Outer: used by the main script, a script made by the importer of the module
Inner: can be used by the main script, but generally should not
'''

class PSBot():
    def __init__(self, server=URL):
        #outer attributes
        self.connected = False
        self.account = None
        #inner attributes
        self.server = server
        self.note_cond = False
        self.events = dict()
        self.ws = None
        self.requests = []
    #INNER BOT PROCESSES
    #handler
    def process(self, info):
        self.loop.create_task(handler.handle(self, info))
    #send
    async def send(self, message):
        await asyncio.sleep(0.05)
        r = await self.ws.send_str(message)
        return r
    def connect(self, account):
        self.account = account
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(run(self))

    def event(self, func):
        self.addEvent(Event(func.__name__, func))
    def addEvent(self, event):
        self.events[event.eventid] = event
    def note(self, cond):
        self.note_cond = True if cond else False

    #OUTER
    #events
    async def on_connect(self):
        if 'on_connect' in self.events.keys():
            #passes bot and bot's account
            await self.events['on_connect'].func(self)
    async def on_login(self, username):
        if 'on_login' in self.events.keys():
            #Passes an account with only the username
            account = getAccount(username)
            await self.events['on_login'].func(self, account)
    async def on_ready(self, username):
        if 'on_ready' in self.events.keys():
            #Passes an account with only the username
            account = getAccount(username)
            await self.events['on_ready'].func(self, account)
    async def on_pm(self, username, messagetxt):
        if 'on_pm' in self.events.keys():
            newname = ''
            for i in username[1:]:
                if i.lower() in list('qwertyuiopasdfghjklzxcvbnm1234567890'):
                    newname += i.lower()
            account = getAccount(newname)
            message = Message(messagetxt, author=account)
            await self.events['on_pm'].func(self, message)
    async def on_chat(self, username, messagetxt, roomid, msgid):
        if 'on_chat' in self.events.keys():
            newname = ''
            for i in username[1:]:
                if i.lower() in list('qwertyuiopasdfghjklzxcvbnm1234567890'):
                    newname += i.lower()
            account = getAccount(newname)
            rank = username[0]
            message = Message(messagetxt, account, roomid, msgid)
            await self.events['on_chat'].func(self, message, rank)

    #not sure what to call these
    async def getUser(self, account):
        if type(account) != Account:
            errortext = 'Invalid destination: Cannot get user from type {}'
            raise SendError(errortext.format(type(account)))
        else:
            request = Request('getUser',(account))
            self.requests.append(request)
            await self.send('|/cmd userdetails {}'.format(account.username))
            while request.response == None:
                await asyncio.sleep(0.05)
            r = request.response
            self.requests.remove(request)
            return User(r)

    async def message(self, msgtxt, dest):
        if type(dest) == User or type(dest) == Account:
            await self.send('|/msg {}, {}'.format(dest.username, msgtxt))
        elif type(dest) == Room:
            await self.send('{}|{}'.format(dest.roomid, msgtxt))
        else:
            raise SendError('Invalid destination.')

    async def joinRoom(self, room):
        if type(room) != Room:
            text = 'Invalid destination: Cannot join {}'.format(type(room))
            raise SendError(text)
        else:
            await self.send('|/join {}'.format(room.roomid))

async def run(bot):
    try:
        async with aiohttp.ClientSession() as session:
            ws = await session.ws_connect(bot.server)
            bot.connected = True
            bot.ws = ws
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    bot.process(str(msg.data))
    except aiohttp.ClientConnectorError as e:
        print('Connection error:',e)
        
        
    
