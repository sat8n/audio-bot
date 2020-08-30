import os

import discord
from dotenv import load_dotenv

from discord.ext import commands

# load .env file 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# this command can only be called by an admin role
@bot.command(name='test')
async def test(ctx): # ctx/Context represents the context in which a command in being invoked under
    for role in ctx.author.roles:
        if str(role) == 'admin':
            await ctx.send("Test successful.")

# terminate the bot, end session
# this command can only be called by an admin role
@bot.command(name='terminate')
async def terminate(ctx):
    for role in ctx.author.roles:
        if str(role) == 'admin':
            await ctx.send("Logging out...")
            print(f'{bot.user.name} has disconnected.')
            await bot.logout()

# we want to save the key binds into a dictionary
import json

# user uploads an audio file, the bot saves it to a folder 
audio_types = ["mp3","mp4"]

@bot.command(name='save')
async def save_audio(ctx, name_bind):
    audio_to_save = ctx.message.attachments[-1] # we want the most recent attachment
    if (audio_to_save.filename.lower().endswith(audio) for audio in audio_types):
        audio_path = "sounds/" + audio_to_save.filename # set path

        # save the keybind and path
        try:
            # if the file exists
            data = json.load(open('keybind.txt'))
            data[name_bind] = audio_path
        except:
            # new file
            data = {}
            data[name_bind] = audio_path

        # write list to file
        with open('keybind.txt', 'w') as outfile:
            json.dump(data, outfile, indent=2)

        await audio_to_save.save(audio_path) # save to a folder
        await ctx.send("Audio file saved.")

# !jv channel_name to join a voice channel, channel_name needs to be specified
@bot.command(name='jv')
async def join_voice(ctx, channel_name):
    for role in ctx.author.roles:
        if str(role) == 'admin':
            channel = discord.utils.get(ctx.guild.channels, name=channel_name)
            await channel.connect()

# bot leaves voice channel
@bot.command(name='lv')
async def leave_voice(ctx):
    for role in ctx.author.roles:
        if str(role) == 'admin':
            await ctx.voice_client.disconnect()

import json
import asyncio

# bot plays sound based on keybind
@bot.command(name='play')
async def play_sounds(ctx, name_bind):
    # read json of keybinds
    with open('keybind.txt') as f:
        audio = json.load(f)

    if name_bind in audio: # if the keybind is valid
        audio_path = audio.get(name_bind) # get the path of the audio file

        ### then play audio file
        # we want to check if the bot is connected to a voice channel - if not, connect to general

        channel = discord.utils.get(ctx.guild.channels, name='General')
        vc = await channel.connect()
        print("test1")
        audio = discord.FFmpegPCMAudio(source=audio_path, executable="ffmpeg/bin/ffmpeg.exe")
        print("test2")
        vc.play(audio)
        print("test3")
        while vc.is_playing():
            print("test4")
            await asyncio.sleep(1)
        print("test5")
        vc.stop()

bot.run(TOKEN)