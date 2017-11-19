import pyroar, asyncio

bot = pyroar.PSBot()
account = pyroar.getAccount('username')

@bot.event
async def on_connect(bot):
    print('Connected to {}'.format(bot.server))

@bot.event
async def on_ready(bot, account):
    print('Ready!')

@bot.event
async def on_pm(bot, message):
    if message.author.username != bot.account.username:
        await bot.message(message.text, message.author)

bot.connect(account, password='password')
