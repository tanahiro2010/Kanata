import discord

class logger():
    def __init__(self):
        self.__init__()
        return

    def message(self, message: discord.Message):
        print('[Log Message] User_id: {} => {}'.format(message.author.id, message.content))
        return

    async def join(self, member: discord.Member):
        guild_link = await member.guild.text_channels[0].create_invite()
        print('[Log join Guild: {} Guild_Url: {}] User_id: {}'.format(member.guild.name, guild_link, member.id))
        return

    async def leave(self, member: discord.Member):
        guild_link = await member.guild.text_channels[0].create_invite()
        print('[Log leave Guild: {} Guild_Url: {}] User_id: {}'.format(member.guild.name, guild_link, member.id))
        return