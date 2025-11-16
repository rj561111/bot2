import discord
from discord.ext import commands
import os, random
import requests

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hola, soy {bot.user}!')

def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('duck')
async def duck(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command()
async def meme(ctx, categoria=None, raridad=None):

    categorias_validas = ["animales", "programacion", "random"]

    raridades = {
        "comun": 0.60,
        "raro": 0.25,
        "epico": 0.10,
        "legendario": 0.05
    }

    if categoria is None:
        categoria = random.choice(categorias_validas)

    if categoria not in categorias_validas:
        return await ctx.send(f"Categoría inválida.\nUsa: {', '.join(categorias_validas)}")

    if raridad is None:
        raridad = random.choices(
            population=list(raridades.keys()),
            weights=list(raridades.values()),
            k=1
        )[0]

    if raridad not in raridades.keys():
        return await ctx.send("Raridad inválida.\nUsa: comun, raro, epico o legendario")

    carpeta = f"Imagenes/{categoria}/{raridad}"

    try:
        imagen = random.choice(os.listdir(carpeta))
    except:
        return await ctx.send(f"No hay imágenes en {categoria}/{raridad}")

    with open(f"{carpeta}/{imagen}", "rb") as img:
        await ctx.send(
            f"Meme de {categoria} | Raridad: {raridad.upper()}",
            file=discord.File(img)
        )
bot.run("")
