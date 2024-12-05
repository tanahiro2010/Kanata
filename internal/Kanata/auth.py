import discord
from internal.config import Config

class Auth(Config):
    def __init__(self, config: Config) -> None:
        self.Config = config
        return

    def auth_role(self, member: discord.Member) -> bool:
        guild_id: str = str(member.guild.id)

        config: Config = self.Config

        conf: dict = config.load_config()
        guilds: dict = conf.get('guilds')
        guild: dict or bool = guilds.get(guild_id, False)

        if guild:
            admin_role_id: int = int(guild['role']['admin'])
            admin_role: discord.Role = member.guild.get_role(admin_role_id)
            if admin_role not in member.roles:
                return True

        return False

    def auth_config_member(self, member: discord.Member) -> bool:
        config = self.Config
        conf: dict = config.load_config()

        member_id = member.id

        if member_id in conf.get('members', []):
            return True

        return False

    def auth_config_developer(self, member: discord.Member) -> bool:
        config = self.Config
        conf: dict = config.load_config()

        member_id = member.id

        if member_id in conf.get('developers', []):
            return True

        return False