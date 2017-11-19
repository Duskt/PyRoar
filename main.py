import pyroar, asyncio

bot = pyroar.PSBot()
account = pyroar.getAccount('USERNAME')

@bot.event
async def on_connect(bot):
    print('Connected to {}'.format(bot.server))

@bot.event
async def on_ready(bot, account):
    await bot.joinRoom(pyroar.getRoom('ROOMID'))
    print('Ready!')

@bot.event
async def on_pm(bot, message):
    #echoes message if it's not from the bot (otherwise infinite loop)
    if message.author.username != bot.account.username:
        await bot.message(message.text, message.author)

@bot.event
async def on_chat(bot, message, rank):
    #who needs browsers, this has it all
    print(message.content)

bot.connect(account, password='PASSWORD')
