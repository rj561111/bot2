import discord
from discord.ext import commands
import os, random
import requests

# --------------------------------------------------
# CONFIGURACIÓN DEL BOT
# --------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

# --------------------------------------------------
# EVENTOS
# --------------------------------------------------
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# --------------------------------------------------
# COMANDOS BÁSICOS
# --------------------------------------------------
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

# --------------------------------------------------
# SISTEMA DE MEMES CON CATEGORÍA Y RARIDAD
# --------------------------------------------------
@bot.command()
async def meme(ctx, categoria=None, raridad=None):

    # Categorías permitidas
    categorias_validas = ["animales", "programacion", "random"]

    # Raridades y probabilidades por defecto
    raridades = {
        "comun": 0.60,
        "raro": 0.25,
        "epico": 0.10,
        "legendario": 0.05
    }

    # Si no dan categoría → elegir al azar
    if categoria is None:
        categoria = random.choice(categorias_validas)

    # Validar categoría
    if categoria not in categorias_validas:
        return await ctx.send(f"Categoría inválida.\nUsa: {', '.join(categorias_validas)}")

    # Si no dan raridad → se elige según probabilidades
    if raridad is None:
        raridad = random.choices(
            population=list(raridades.keys()),
            weights=list(raridades.values()),
            k=1
        )[0]

    # Validar raridad
    if raridad not in raridades.keys():
        return await ctx.send("Raridad inválida.\nUsa: comun, raro, epico o legendario")

    # Ruta final
    carpeta = f"Imagenes/{categoria}/{raridad}"

    # Verificar imágenes en carpeta
    try:
        imagen = random.choice(os.listdir(carpeta))
    except:
        return await ctx.send(f"No hay imágenes en {categoria}/{raridad}")

    # Enviar imagen
    with open(f"{carpeta}/{imagen}", "rb") as img:
        await ctx.send(
            f"Meme de {categoria} | Raridad: {raridad.upper()}",
            file=discord.File(img)
        )
bot.run("")
