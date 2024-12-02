import discord
import discord.app_commands as commands
import requests
import os
from internal.logger import logger
from dotenv import load_dotenv
import json

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

@client.event
async def on_ready(): # botが起動したとき
    print('Kanata is ready.')
    return

@client.event
async def on_guild_join(guild: discord.Guild):
    owner_id: int = guild.owner_id
    owner: discord.User = client.get_user(owner_id)

    # サーバーに管理用ロール作成
    try:
        permissions: discord.Permissions = discord.Permissions.administrator()
        bot_role = await guild.create_role(
            name='Bot',
            permissions=permissions,
            color=discord.Color.dark_purple()
        )



    except discord.Forbidden as e:
        embed = discord.Embed( # エラーメッセージを作成
            title="Error",
            description="Bot用ロールを作成時に失敗しました。\nサーバーへの参加時には管理者権限が必要です。\n管理者権限をつけて再試行してください。\nなお、自動的にサーバーは脱退されます",
            color=discord.Color.red()
        )

        await guild.leave() # サーバーを脱退
        await owner.dm_channel.send(embed=embed) # サーバーのownerに送信
        return



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