import discord
from internal.config import Config
import json

class logger:
    def __init__(self, config: Config):
        self.config = config
        return

    def get_invite_url(self, guild_id: str) -> None or str:
        conf: dict = self.config.load_config()
        guilds: dict = conf["guilds"]
        guild: dict or None = guilds.get(guild_id, None)

        if guild is None:
            return None
        else:
            return guild['info']['invite_url']

    async def message(self, message: discord.Message):
        guild_link = self.get_invite_url(str(message.guild.id))
        print('[Log Message Guild: {} Guild_Url: {}] User_id: {} => {}'.format(message.guild.name, guild_link, message.author.name, message.content))
        return

    async def join(self, member: discord.Member):
        guild_link = self.get_invite_url(str(member.guild.id))
        print('[Log join Guild: {} Guild_Url: {}] User_id: {}'.format(member.guild.name, guild_link, member.id))
        return

    async def leave(self, member: discord.Member):
        guild_link = self.get_invite_url(str(member.guild.id))
        print('[Log leave Guild: {} Guild_Url: {}] User_id: {}'.format(member.guild.name, guild_link, member.id))
        return

    async def join_guild(self, guild: discord.Guild):
        guild_link = self.get_invite_url(str(guild.id))
        print('[Log Join_Guild] guild_name: {} guild_id: {} guild_url: {}'.format(guild.name, guild.id, guild_link))
        return

    async def leave_guild(self, guild: discord.Guild):
        print('[Log Leave_Guild] guild_name: {} guild_id: {}'.format(guild.name, guild.id))