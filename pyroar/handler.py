import aiohttp, json, re, asyncio
import pyroar.utils

class FormInfo():
    def __init__(self, raw):
        #raw is msgdata
        self.raw = raw
        self.info = [i.split('|') for i in raw.split('\n')]
        #This parses through data, splitting by \n and |
        nest = self.info
        #room will be the set the the first item in the split unless it is ''
        self.room = None
        #pun of nested lists
        for bird in nest:
            if bird[0] != '':
                self.room = bird[0]
            else:
                #the first item (usually empty) is destroyed
                bird.pop(0)
        try:
            for i in nest:
                if i[0] == 'pm' or i[0] == 'c:':
                    i[3] = '|'.join(i[3:])
        except:
            pass
        #e.g. [['updateuser','whatever','1','1']]
        self.data = nest
        

async def handle(bot, info):
    i = FormInfo(info)
    if bot.note_cond:
        #for debugging usually
        print(info)
    for piece in i.data:
        try:
            key = piece[0]
        except:
            key = None

        if key == 'challstr':
            #login
            bot.loop.create_task(bot.on_connect())
            user = bot.account.username
            resp = await pyroar.utils.login(user,
                                     bot.account.password,
                                     '|'.join(piece[1:3]))
            if resp is None:
                raise Exception('Unable to login.')
            else:
                await bot.send('|/trn {},0,{}'.format(user, resp))

        elif key == 'updateuser':
            username = piece[1]
            bot.loop.create_task(bot.on_login(username))
            if username == bot.account.username:
                bot.loop.create_task(bot.on_ready(username))
        elif key == 'queryresponse':
            user = json.loads(piece[2])
            for index, i in enumerate(bot.requests):
                try:
                    if i.info[0].username == user['userid']:
                        bot.requests[index].response = user                       
                except:
                    pass
        elif key == 'pm':
            username = piece[1]
            message = piece[3]
            bot.loop.create_task(bot.on_pm(username, message))

        elif key == 'c:':
            author = piece[2]
            msgid = piece[1]
            msgtxt = piece[3]
            room = i.room[1:]
            bot.loop.create_task(bot.on_chat(author, msgtxt, room, msgid))
            

        
