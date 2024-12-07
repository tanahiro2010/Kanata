import discord
import time


def join_member(member: discord.Member):
    embed = discord.Embed(
        title="{}が参加しました".format(member.display_name),
        description="{}が参加しました。\nID: {}\nName: {}\nTime: {}".format(member.name, member.id, member.display_name,  member.joined_at),
        timestamp=member.joined_at
    )
    icon = member.avatar.url
    embed.set_thumbnail(
        url=icon
    )
    return embed

def leave_member(member: discord.Member):
    embed = discord.Embed(
        title="{}が脱退しました".format(member.display_name),
        description="{}が脱退しました。\nID: {}\nName: {}\nTime: {}".format(member.name, member.id, member.display_name,  member.joined_at),
        timestamp=member.joined_at,
    )
    icon = member.avatar.url
    embed.set_thumbnail(
        url=icon
    )
    return embed