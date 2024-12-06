import discord
import discord.app_commands as commands
import requests
import os
from dotenv import load_dotenv
import json
from internal.logger import logger
from internal.config import Config
from internal.Discord import Discord
from internal.Kanata.auth import Auth

# トークンなどの読み込み
load_dotenv('.env')
token = os.getenv('token')
admin_user_id = os.getenv('admin_user')

# DiscordBot用のオブジェクトなどの作成
intents: discord.Intents = discord.Intents.all()
client: discord.Client = discord.Client(intents=intents)
tree: commands.CommandTree = commands.CommandTree(client=client)

# その他作成
config = Config('discord.config.json')
Logger = logger(config)
dis = Discord(config=config, client=client)
auth = Auth(config=config)

@client.event
async def on_ready(): # botが起動したとき
    print('Kanata is ready.')
    return

@client.event
async def on_guild_join(guild: discord.Guild):
    owner_id: int = guild.owner_id
    owner: discord.User = client.get_user(owner_id)

    f_result = await dis.add_guild(guild) # ロール作成などの初期設定

    if f_result:
        s_result = await dis.setup_roles(guild)
        await Logger.join_guild(guild)

    else:
        await Logger.leave_guild(guild)
    return

@client.event
async def on_guild_remove(guild: discord.Guild):
    try:
        result = dis.leave_guild(guild)
    except:
        result = False

    if result:
        await Logger.leave_guild(guild)
    else:
        print("Error")



@client.event
async def on_member_join(member: discord.Member): # サーバーに誰か入ってきたなら
    if member.bot: # 参加したのがbotなら
        dis_config = config.load_config()

        await member.roles
        return


@client.event
async def on_message(message: discord.Message): # メッセージが来た時
    if message.author.bot: # 送信者がボットなら
        return

    # await Logger.message(message)


    return

client.run(token)