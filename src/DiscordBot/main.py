import sys
sys.path.append('../')
import discord
from discord.ext import commands
import asyncio
from config import TOKEN
from BotClass.bot import OneCoin, MultiCoin

intents = discord.Intents.default()
intents.typing = False
intents.message_content = True  # message content intenti ekleniyor

bot = commands.Bot(command_prefix="/", intents=intents)

analiz_devam_ediyor = False  # Analizin durumunu tutan bayrak
@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready!")


@bot.command()
async def multiple_coin(ctx):
    global analiz_devam_ediyor
    if analiz_devam_ediyor:
        await ctx.send("Analiz zaten devam ediyor.")
        return
    
    analiz_devam_ediyor = True
    multicoin = MultiCoin()

    while analiz_devam_ediyor:
        for symbol in multicoin.coins.values():
            result = multicoin.analyze(symbol)
            if not analiz_devam_ediyor:
                break  # Analizi durdurmak için döngüden çık
            elif result != None:
                await ctx.send(result)
        
        #await asyncio.sleep(60)
    
    await ctx.send("Analiz durduruldu.")

@bot.command()
async def stop(ctx):
    global analiz_devam_ediyor
    if analiz_devam_ediyor:
        analiz_devam_ediyor = False
        await ctx.send("Analiz durduruldu.")
    else:
        await ctx.send("Analiz zaten durdurulmuş.")



        
import datetime
import asyncio

analiz_devam_ediyor = False  # Analizin durumunu tutan bayrak

@bot.command()
async def send_embed(ctx, symbol):
    global analiz_devam_ediyor
    if analiz_devam_ediyor:
        await ctx.send("Analiz zaten devam ediyor.")
        return

    analiz_devam_ediyor = True
    onecoin = OneCoin(symbol)

    async def send_result(result):
        if result:
            embed = discord.Embed(
                title=symbol,
                description=f"Saat -- {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",
                color=discord.Color.blue()
            )
            embed.set_author(name="EA-TradeBot", icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url="https://en.higer.com/uploadfiles/2021/01/20210113180925577.png?NjE0MlMucG5n")
            embed.add_field(name="Tavsiye edilen işlem", value=result[0], inline=False)
            embed.add_field(name="Olasılık", value=result[1], inline=False)
            await ctx.send(embed=embed)
        else:
            await asyncio.sleep(150)  # 150 saniye beklemek
            if analiz_devam_ediyor:
                await ctx.send(f"Analiz devam ediyor: {symbol}")

    while analiz_devam_ediyor:
        result = onecoin.analyze()
        if result and len(result) == 4:  # Doğru sayıda eleman içeriyorsa
            recomandation, signal1, signal2, signal3 = result
            signals = f'Al:{signal1} - Sat:{signal2} - Bekle:{signal3}'
            await send_result((recomandation, signals))
        
    await ctx.send("Analiz durduruldu.")
    
@bot.command()
async def send_embed_multi(ctx):
    global analiz_devam_ediyor
    if analiz_devam_ediyor:
        await ctx.send("Analiz zaten devam ediyor.")
        return

    analiz_devam_ediyor = True
    multicoin = MultiCoin()
    
    async def send_result(symbol, result):
        if result:
            embed = discord.Embed(
                title=symbol,
                description=f"Saat -- {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",
                color=discord.Color.blue()
            )
            embed.set_author(name="EA-TradeBot", icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url="https://en.higer.com/uploadfiles/2021/01/20210113180925577.png?NjE0MlMucG5n")
            embed.add_field(name="Tavsiye edilen işlem", value=result[0], inline=False)
            embed.add_field(name="Olasılık", value=result[1], inline=False)
            await ctx.send(embed=embed)

        else:
            await asyncio.sleep(150)  # 150 saniye beklemek
            if analiz_devam_ediyor:
                await ctx.send(f"Analiz devam ediyor: {symbol}")
    
    while analiz_devam_ediyor:
        for symbol in multicoin.coins.values():
            result = multicoin.analyze(symbol)
            if result and len(result) == 4:
                recomandation, signal1, signal2, signal3 = result
                signals = f'Al:{signal1} - Sat:{signal2} - Bekle:{signal3}'
                await send_result(symbol, (recomandation, signals))

    await ctx.send("Analiz durduruldu.")


# # Yardım komutu özelleştirilmiş bir yardım menüsü sunar
# bot.remove_command("help")  # Varsayılan yardım komutunu kaldırır

# @bot.command()
# async def custom_help(ctx):
#     embed = discord.Embed(
#         title="Özel Yardım Menüsü",
#         description="Aşağıda mevcut komutların listesi bulunmaktadır:",
#         color=discord.Color.blue()
#     )
    
#     embed.add_field(name="!hello", value="Bir selam gönderir.", inline=False)
#     # Diğer komutları da buraya ekleyebilirsiniz

#     await ctx.send(embed=embed)


bot.run(TOKEN)
