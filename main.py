import pyroar, asyncio

bot = pyroar.PSBot()
account = pyroar.getAccount('USERNAME',password='ENTERPASSWORD')

@bot.event
async def on_connect(bot):
    print('Connected to {}'.format(bot.server))

@bot.event
async def on_ready(bot, account):
    print('Ready!')

@bot.event
async def on_pm(bot, message):                           
    #echoes back to author
    await bot.message(message.text, message.author)

bot.connect(account)
