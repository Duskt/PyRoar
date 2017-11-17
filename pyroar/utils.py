import json, asyncio
import aiohttp

async def login(username, password, challstr):
    url = 'https://play.pokemonshowdown.com/action.php'
    values = {'act': 'login',
              'name': username,
              'pass': password,
              'challstr': challstr
              }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=values) as r:
            resp = await r.text()
            resp = json.loads(resp[1:])
            return resp['assertion']

def argParse(string, seperator=','):
    #Reads string and decides whether to incorporate whitespace.
    #This is not used in the PyRoar package, it is simply for utility
    '''
    Syntax Rules:
    - Spaces before an argument (after a seperator) will be ignored.
    - Spaces after an argument (before a seperator) will be ignored.
    - The first space will count as a seperator for the command name and
    arguments.
    e.g. echo_individually    ,    hello ,   hello there,,hi
    outputs:\nhello\nhello there\n\nhi
    '''
    cond = False
    command = ''
    arg = ''
    #seperate command
    for i in string:
        if i == ' ' and not cond:
            cond = True
            continue
        if cond:
            arg += i
        else:
            command += i
    args = []
    holder = ''
    space = True
    #seperate arguments, get rid of prefix whitespace
    for index, i in enumerate(arg):
        if space:
            space = False if i != ' ' else space
            if space:
                continue
        if i == seperator and arg[index-1] != '\\':
            space = True
            args.append(holder)
            holder = ''
        elif i == '\\' and arg[index+1] == seperator:
            continue
        else:
            holder += i
    args.append(holder)
    #note suffix whitespace
    newargs = []
    for item in args:
        space = True
        new = ''
        for letter in reversed(item):
            if space:
                space = False if letter != ' ' else space
                if space:
                    continue
            new += letter
        newargs.append(new[::-1])           
    return [command, newargs]

if __name__ == '__main__':
    print('This file should be imported.')
