from email import message

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
from internal.embeds.message import delete_message

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
async def on_guild_join(guild: discord.Guild):
    owner_id: int = guild.owner_id
    owner: discord.User = client.get_user(owner_id)

    f_result = await dis.add_guild(guild) # ロール作成などの初期設定

    if f_result:
        s_result = await dis.setup_roles(guild)
        if s_result:
            await Logger.join_guild(guild)
            return
        else:
            await guild.leave()
            pass
        pass

    await Logger.leave_guild(guild)

    return

@client.event
async def on_guild_remove(guild: discord.Guild): # ギルドから消されたら
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
    return await dis.join_member(member=member)

@client.event
async def on_member_remove(member: discord.Member):
    return await dis.leave_member(member)


@client.event
async def on_message(message: discord.Message): # メッセージが来た時
    if message.author.bot: # 送信者がボットなら
        return

    await Logger.message(message)
    return

@client.event
async def on_message_delete(message: discord.Message):
    conf = config.load_config()
    guild_conf = conf['guilds'][str(message.guild.id)]

    message_log_channel_id: int = guild_conf['log']['channels']['messages']
    message_log_channel: discord.TextChannel = client.get_channel(message_log_channel_id)

    embed = delete_message(message)

    await message_log_channel.send(embed=embed)
    return

# コマンド実装

@tree.command(name="verify", description="認証ボードを作成します")
@commands.describe(
    role="認証後に付けるロールを指定してください",
    title="認証ボードのタイトル",
    description="認証ボードの説明 #roleでロールメンション"
)
async def verify(interaction: discord.Interaction, role: discord.Role, title: str = "認証", description: str = "認証ボタンを押すと、#roleロールが付与されます") -> None:
    desc_content = description.replace("#role", "<@&{}>".format(role.id))

    await interaction.response.defere()


@client.event
async def on_ready(): # botが起動したとき
    print('Kanata is ready.')
    await tree.sync() # コマンドを同期
    return
client.run(token)