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

        owner = guild.owner

        # Bot用ロール作成
        permissions = discord.Permissions(administrator=True)
        print(permissions)
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
            await owner.dm_channel.send(embed=embed)

            time.sleep(5000)

            await guild.leave()
            return

        role_id = bot_role.id

        # KanataBot使用用権限ロール作成
        try:
            admin_role = await guild.create_role(
                name="管理用-KanataMember",
                color=discord.Color.light_grey(),
            )

        except discord.Forbidden as e:
            embed = error_embed(
                description="KanataBot導入に必要な権限が存在しない可能性があります。\nKanataBotには管理者権限が必要です。\n再導入しなおしてください。\n"
                            "なお、このボットは自動的に脱退します\n\n",
            )
            await owner.dm_channel.send(embed=embed)

            time.sleep(5000)

            await guild.leave()
            return

        await guild.owner.add_roles(
            admin_role
        )

        # ログ用チャンネルのカテゴリ作成
        try:
            log_category = await guild.create_category(
                name="管理用-KanataLog",
                overwrites={
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    admin_role: discord.PermissionOverwrite(read_messages=True),
                }
            )

        except discord.Forbidden as e:
            embed = error_embed(
                description="チャンネル作成用の権限がありません\n再導入してください"
            )

            await owner.dm_channel.send(embed=embed)

            time.sleep(5000)

            await guild.leave()
            return

        try: # メンバーの出入りログ用チャンネル
            member_channel = await guild.create_text_channel(
                name="管理用-MembersLog",
                category=log_category
            )

        except discord.Forbidden as e:
            embed = error_embed(
                description="チャンネル作成用の権限がありません\n再導入してください"
            )

            await owner.dm_channel.send(embed=embed)

            time.sleep(5000)

            await guild.leave()
            return

        try: # メッセージ系ログチャンネル作成
            message_channel = await guild.create_text_channel(
                name="管理用-MessagesLog",
                category=log_category
            )

        except discord.Forbidden as e:
            embed = error_embed(
                description="チャンネル作成用の権限がありません\n再導入してください"
            )

            await owner.dm_channel.send(embed=embed)

            time.sleep(5000)

            await guild.leave()
            return

        try: # 使うかわからないその他のログ
            other_role = await guild.create_text_channel(
                name="管理用-OtherLog",
                category=log_category
            )

        except discord.Forbidden as e:
            embed = error_embed(
                description="チャンネル作成用の権限がありません\n再導入してください"
            )

            await owner.dm_channel.send(embed=embed)

            time.sleep(5000)

            await guild.leave()
            return

        try:
            invite_url = (await guild.text_channels[0].create_invite()).url
            print(invite_url)
        except discord.Forbidden as e:
            embed = error_embed(
                description="InviteUrlが作成できません\n再導入してください"
            )

            await owner.dm_channel.send(embed=embed)

            time.sleep(5000)

            await guild.leave()
            return


        guildObj = {
            "info": {
                "name": guild_name,
                "id": guild_id,
                "owner_id": owner.id,
                "invite_url": invite_url
            },

            "role": {
                "bot": bot_role.id,
                "admin": admin_role.id
            },
            "log": {
                "category": log_category.id,
                "channels": {
                    "members": member_channel.id,
                    "messages": message_channel.id,
                    "other": other_role.id
                }
            }
        }

        config = self.Config.load_config()
        config['guilds'][guild_id] = guildObj

        return self.Config.save_config(data=config)

    async def leave_guild(self, guild: discord.Guild):
        guild_id = guild.id

        config = self.Config.load_config()
        config['guilds'].pop(str(guild_id))

        return self.Config.save_config(data=config)

    async def setup_roles(self, guild: discord.Guild):
        conf = self.Config.load_config()
        dev_role_id: int = int(conf['role']['admin'])
        dev_role: discord.Role = guild.get_role(dev_role_id)
        bot_role_id: int = int(conf['role']['bot'])
        bot_role: discord.Role = guild.get_role(bot_role_id)
        for member in guild.members:
            try:
                if member.bot:
                    await member.add_roles(bot_role) # bot専用管理ロール追加
                else:
                    member_id = member.id
                    if member_id in conf['members']:
                        await member.add_roles(dev_role)
                    pass
                pass
            except discord.Forbidden as e:
                return False
        return True

    async def join_member(self, member: discord.Member):
        conf = self.Config.load_config()
        dev_role_id: int = int(conf['role']['admin'])
        bot_role_id: int = int(conf['role']['bot'])

        if member.bot: # ロールなどの付与処理
            bot_role = member.guild.get_role(bot_role_id)
            await member.add_roles(bot_role)
        else:
            member_id = member.id
            if member_id in conf['members']:
                dev_role = member.guild.get_role(dev_role_id)
                await member.add_roles(dev_role)
            pass


        # Logに送信
        members_log_channel_id: int = int(conf['guilds'][str(member.guild.id)]['log']['channels']['members'])
        members_log_channel: discord.TextChannel = guild.get_channel(members_log_channel_id)
        return