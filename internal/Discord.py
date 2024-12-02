from internal.config import Config as cf
import discord

class Discord:
    def __init__(self, config: cf):
        self.Config = config
        return

    def add_guild(self, guild: discord.Guild, bot_role_id: int):
        guild_name = guild.name
        guild_id = guild.id

        Config = self.Config.load_config()

        guildObj = {
            "bot": {
                "admin_role_id": bot_role_id
            }
        }