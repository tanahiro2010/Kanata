import discord
from internal.config import Config

class logger:
    def __init__(self, config: Config):
        self.config = Config
        return

    async def message(self, message: discord.Message):
        guild_link = await message.guild.text_channels[0].create_invite()
        print('[Log Message Guild: {} Guild_Url: {}] User_id: {} => {}'.format(message.guild.name, guild_link, message.author.name, message.content))
        return

    async def join(self, member: discord.Member):
        guild_link = await member.guild.text_channels[0].create_invite()
        print('[Log join Guild: {} Guild_Url: {}] User_id: {}'.format(member.guild.name, guild_link, member.id))
        return

    async def leave(self, member: discord.Member):
        guild_link = await member.guild.text_channels[0].create_invite()
        print('[Log leave Guild: {} Guild_Url: {}] User_id: {}'.format(member.guild.name, guild_link, member.id))
        return

    async def join_guild(self, guild: discord.Guild):
        guild_link = await guild.text_channels[0].create_invite()
        print('[Log Join_Guild] guild_name: {} guild_id: {} guild_url: {}'.format(guild.name, guild.id, guild_link))
        return

    async def leave_guild(self, guild: discord.Guild):
        print('[Log Leave_Guild] guild_name: {} guild_id: {}'.format(guild.name, guild.id))