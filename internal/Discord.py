import time

from internal.config import Config as cf
from internal.embeds.error import error_embed
import discord

class Discord:
    def __init__(self, config: cf, client: discord.Client):
        self.Config = config
        self.client = client
        return

    async def add_guild(self, guild: discord.Guild):
        ## 内容
        # ロール作成
        # 管理用チャンネル作成
        # ownerにDM

        guild_name = guild.name
        guild_id = guild.id

        # Bot用ロール作成
        permissions = discord.Permissions.administrator()
        try:
            bot_role = await guild.create_role(
                name="管理用ロール-bot",
                permissions=permissions,
                color=discord.Color.blurple()
            )
        except discord.Forbidden as e:
            embed = error_embed(
                description="KanataBot導入に必要な権限が存在しない可能性があります。\nKanataBotには管理者権限が必要です。\n再導入しなおしてください。\n"
                            "なお、このボットは自動的に脱退します\n\n### 詳細エラー\n" + str(e),
            )
            await guild.owner.dm_channel.send(embed=embed)

            time.sleep(5000)

            await guild.leave()
            return

        role_id = bot_role.id

        # KanataBot使用用権限ロール作成
        permissions = discord.Permissions.none()
        try:
            admin_role = await guild.create_role(
                name="KANATA",
                permissions=permissions,
                color=discord.Color.light_grey()
            )

        except discord.Forbidden as e:
            embed = error_embed(
                description="KanataBot導入に必要な権限が存在しない可能性があります。\nKanataBotには管理者権限が必要です。\n再導入しなおしてください。\n"
                            "なお、このボットは自動的に脱退します\n\n### 詳細エラー\n" + str(e),
            )
            await guild.owner.dm_channel.send(embed=embed)

            time.sleep(5000)

            await guild.leave()
            return

        return