import discord


def delete_message(message: discord.Message) -> discord.Embed:
    embed: discord.Embed = discord.Embed(
        title="メッセージが削除されました",
        description="Message\nAuthor: {}\n### Content\n```text\n{}\n```".format(message.author.mention, message.content),
        color=discord.Color.red()
    )
    embed.set_thumbnail(
        url=message.author.avatar.url
    )

    return embed
