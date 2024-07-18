'''
This file holds all methods related message listening
on_message_duel: alerts moderators if a duel occurs
on_message_public: alerts moderators if a public duel occurs
on_message_active: adds active members to a list
on_leaderboard_update: copys the most recent leaderboard and posts it in the log channel
'''
import discord
import settings
import re


#checks to see if a duel result has been posted
async def on_message_duel(message: discord.Message, bot) -> None:
    if message.author != bot.user:
        if message.channel == bot.get_channel(settings.one_vs_one_id):
            message_string = message.content
            battle_result = re.search(r"(<@[0-9]+>[\s]*)+([=|>])[\s]*(<@[0-9]+>[\s]*)+", message_string)
            if battle_result:
                moderator_role = message.guild.get_role(settings.mod)
                leader_role = message.guild.get_role(settings.leader)

                await message.channel.send(f'{moderator_role.mention} and {leader_role.mention}, a new result has been posted!')


#checks to see if a public result has been posted
async def on_message_public(message: discord.Message, bot) -> None:
    if message.author != bot.user:
        if message.channel == bot.get_channel(settings.media_id):
            message_string = message.content
            battle_result = re.search(r"<@[0-9]+>[\s]+[0-9]+", message_string)
            if battle_result:
                moderator_role = message.guild.get_role(settings.mod)
                leader_role = message.guild.get_role(settings.leader)

                await message.channel.send(f'{moderator_role.mention} and {leader_role.mention}, a new public result has been posted!')

#checks activity of users
async def on_message_active(message: discord.Message, bot) -> None:
    auth = message.author
    if auth != bot.user:
        if isinstance(auth, discord.Member):
            if auth.get_role(settings.death) is not None:
                nick = message.author.nick
                if nick is None:
                    nick = message.author.name
                if nick not in settings.active_array:
                    settings.active_array.append(nick)
            else:
                guilds = auth.mutual_guilds
                for guild in guilds:
                    if guild.id == settings.server_id:
                        mem = guild.get_member(auth.id)
                        if mem.get_role(settings.death) is not None:
                            nick = mem.nick
                            if nick is None:
                                nick = mem.name
                            if nick not in settings.active_array:
                                settings.active_array.append(nick)

#Posts the last text file sent for leaderboard in the log channel
async def on_leaderboard_update(message: discord.Message, bot) -> None:
    if message.author == bot.user:
        if message.channel == bot.get_channel(settings.leaderboard_roaster_id) or message.channel == bot.get_channel(settings.global_leaderboard_id):
            if message.attachments:
                log_channel = bot.get_channel(settings.log_id)
                attach_file = await message.attachments[0].to_file()
                await log_channel.send(file=attach_file)


