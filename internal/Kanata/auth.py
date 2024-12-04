import discord
from internal.config import Config


def auth(member: discord.Member) -> bool:
    guild_id: str = str(member.guild.id)

    config: Config = Config('discord.config.json')

    conf: dict = config.load_config()
    guilds: dict = conf.get('guilds')
    guild: dict or bool = guilds.get(guild_id, False)

    if guild:
        admin_role_id: int = int(guild['role']['admin'])
        admin_role: discord.Role = member.guild.get_role(admin_role_id)
        if admin_role not in member.roles:
            return True

    return False
