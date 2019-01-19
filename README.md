# PyRoar
Very unofficial Python Pokemon Showdown API. Only initially uploaded to add a clearer documentation for myself.
Not intended for full usage just yet.

## Dependencies
* aiohttp

`pip install aiohttp`

## Documentation
Look at the [wiki](https://github.com/Zeitocrab/PyRoar/wiki#pyroar-documentation) for documentation.

## Usage
The main.py file contains a working example of usage.
```Python
#imports
import pyroar, asyncio

#create the bot
bot = pyroar.PSBot()

#create your account
me = pyroar.getAccount("MY_NAME")

#@bot.event is a decorator which lets the bot know it's an event
#on_ready is called when the bot logs in to its account. See events for more information
@bot.event
async def on_ready(bot, account):
    print('Ready!')
    
#connect to the account
bot.connect(me, password="ENTERPASSWORD")
```

## Contribution
lol
