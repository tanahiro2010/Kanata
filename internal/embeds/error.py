import discord


def error_embed(title: str = "Error", description: str = None):
    return discord.Embed(
        title=title,
        description=description,
        colour=discord.Colour.red()
    )
