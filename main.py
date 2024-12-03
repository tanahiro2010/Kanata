import discord
import discord.app_commands as commands
import requests
import os
from dotenv import load_dotenv
import json
from internal.logger import logger
from internal.config import Config
from internal.Discord import Discord

# トークンなどの読み込み
load_dotenv('.env')
token = os.getenv('token')
admin_user_id = os.getenv('admin_user')

# DiscordBot用のオブジェクトなどの作成
intents: discord.Intents = discord.Intents.all()
client: discord.Client = discord.Client(intents=intents)
tree: commands.CommandTree = commands.CommandTree(client=client)

# logger作成
Logger = logger()
config = Config('discord.config.json')
dis = Discord(config=config, client=client)

@client.event
async def on_ready(): # botが起動したとき
    print('Kanata is ready.')
    return

@client.event
async def on_guild_join(guild: discord.Guild):
    owner_id: int = guild.owner_id
    owner: discord.User = client.get_user(owner_id)

    await dis.add_guild(guild)



@client.event
async def on_member_join(member: discord.Member): # サーバーに誰か入ってきたなら
    if member.bot: # 参加したのがbotなら
        return


@client.event
async def on_message(message: discord.Message): # メッセージが来た時
    if message.author.bot: # 送信者がボットなら
        return

    Logger.message(message)
    return

client.run(token)