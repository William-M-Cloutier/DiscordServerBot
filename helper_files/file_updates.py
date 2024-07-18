'''
This file holds all methods related to updating leaderboard/roaster files
update_files: calls on methods to update files
update_roaster: updates the roaster file
add_to_leaderboard: adds member to leaderboard
update_leaderboard: updates leaderboard scores
change_user_name: changes a user's name on leaderboard
remove_file: removes last attachment from channel in discord
'''
import discord
import tempfile
import os
from datetime import date
import settings, sort_helper, rank_updates, member_helper

#------------------------Files----------------------------#
#updates both roaster and leaderboard files by adding new member
async def update_files(ctx, member: discord.Member, remove_from_roaster=False) -> None:
    guild = ctx.guild
    member_list = []

    for clan in settings.clan_info_array:
        role = guild.get_role(clan[1])
        if role is not None:
            member_list += role.members.copy()

    #sort member list alphabetically
    for index in range(len(member_list)):
        if member_list[index].nick is None:
            member_list[index].nick = await member_helper.set_nick_prefix(member_list[index])

    sorted_member_list = sorted(member_list.copy(),key=lambda x: x.nick)
    await update_roaster(sorted_member_list, ctx.bot)
    if not remove_from_roaster:
        await add_to_leaderboard(member, sorted_member_list, ctx.bot)

#updates/creates the member roaster from a list of sorted members   
async def update_roaster(sorted_member_list, bot) -> None:
    channel = bot.get_channel(settings.roaster_id)
    await remove_file(channel)
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding='utf-8') as tmp:
        for member in sorted_member_list:
            info = member.nick + '; ' + member.name + '\n'
            try:
                tmp.write(info)
            except Exception as error:
                print(error)
        tmp.close()
        file_name = "Member_" + str(date.today()) + ".txt"
        roaster_file = discord.File(tmp.name, filename=file_name)
        await channel.send(file=roaster_file)
        os.unlink(tmp.name)

#adds new member to the leaderboard text file and places them in sorted order
async def add_to_leaderboard(member: discord.Member, sorted_member_list, bot) -> None:
    leaderboard_channel = bot.get_channel(settings.leaderboard_roaster_id)
    messages = leaderboard_channel.history(limit=500)
    leaderboard_bytes = None

    async for message in messages:
        author = message.author
        if author.id == settings.bot_id and message.attachments:
            leaderboard_bytes = await message.attachments[0].read()
            await message.delete()
            break

    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding='utf-8') as tmp:
        if leaderboard_bytes is not None: #add member to exisiting leaderboard
            leaderboard_contents = leaderboard_bytes.decode()
            leaderboard_array = leaderboard_contents.splitlines()
            info = member.nick + ": " + str(settings.base_score)
            await sort_helper.add_to_sorted_leaderboard(leaderboard_array, info)
            leaderboard_content = '\n'.join(leaderboard_array)
            tmp.write(leaderboard_content)
        else:#create new leaderboard and add member
            for existing_member in sorted_member_list:
                leaderboard_content = existing_member.nick + ": " + str(settings.base_score) + "\n"
                tmp.write(leaderboard_content)
        tmp.close()
        file_name = "Leaderboard_" + str(date.today()) + ".txt"
        channel = bot.get_channel(settings.leaderboard_roaster_id)
        leaderboard_file = discord.File(tmp.name, filename=file_name)
        await channel.send(file=leaderboard_file)
        os.unlink(tmp.name)

#Updates the leaderboard after a battle, daily decay, or yearly reset takes place
async def update_leaderboard(bot, winner:list[discord.Member]=None, loser:list[discord.Member]=None, daily=False, yearly=False, 
                             duel=False, is_tie=False, remove_user=False, remove_member_name=None, user_name_update=False, 
                             old_name=None, man_update=False, override=True, update_score=0) -> None:
    leaderboard_channel = bot.get_channel(settings.leaderboard_roaster_id)
    messages = leaderboard_channel.history(limit=500)
    leaderboard_bytes = None
    guild = leaderboard_channel.guild
    member_list = []
    old_msg = None

    for clan in settings.clan_info_array:
        role = guild.get_role(clan[1])
        if role is not None:
            member_list += role.members.copy()

    async for message in messages:
        author = message.author
        if author.id == settings.bot_id and message.attachments:
            leaderboard_bytes = await message.attachments[0].read()
            old_msg = message
            break

    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding='utf-8') as tmp:
        if leaderboard_bytes is not None:
            leaderboard_contents = leaderboard_bytes.decode()
            leaderboard_array = leaderboard_contents.splitlines()
            if daily:
                await rank_updates.daily_decay(leaderboard_array, member_list, bot)
            if yearly:
                await rank_updates.yearly_reset(leaderboard_array)
                for member in member_list:
                    await rank_updates.update_rank(member, settings.base_score)
            if duel:
                await rank_updates.member_duel(leaderboard_array, winner, loser, is_tie)
            if user_name_update:
               await change_user_name(leaderboard_array, member_list, winner[0], old_name, bot)
            if man_update:
                for index in range(len(leaderboard_array)):
                    current_member = await member_helper.get_member_name(leaderboard_array[index])
                    if current_member == winner[0].nick:
                        current_member = await member_helper.change_member_score(leaderboard_array[index], update_score, is_override=override)
                        leaderboard_array[index] = current_member
                        await rank_updates.update_rank(winner[0], await member_helper.get_member_score(leaderboard_array[index]))
                        break
            if remove_user:
                for index in range(len(leaderboard_array)):
                    current_member = await member_helper.get_member_name(leaderboard_array[index])
                    if remove_member_name in current_member:
                        leaderboard_array.pop(index)
                        break
            await sort_helper.sort_array(leaderboard_array)
            await rank_updates.set_tryout_manager(leaderboard_array[:4], guild, member_list)

            leaderboard_content = '\n'.join(leaderboard_array)

        else:
            await leaderboard_channel.send("Leaderboard not found. Cannot update.")
            return    

        tmp.write(leaderboard_content)
        tmp.close()
        file_name = "Leaderboard_" + str(date.today()) + ".txt"
        channel = bot.get_channel(settings.leaderboard_roaster_id)
        leaderboard_file = discord.File(tmp.name, filename=file_name)
        try:
            await old_msg.delete()
        except:
            print("Error. Tried to delete file that doesn't exist. Message might have been deleted already.")
        await channel.send(file=leaderboard_file)
        os.unlink(tmp.name)

#change users name on leaderboard
async def change_user_name(leaderboard_array, member_list, member:discord.Member, old_name, bot) -> None:
    nick_name = member.nick
    if nick_name is None:
        nick_name = ''
    for clan in settings.clan_info_array:
        if member.get_role(clan[1]):
            prefix = f"[{clan[0]}]"
            if prefix not in nick_name:
                nick_name = prefix + ' ' + nick_name
                await member.edit(nick=nick_name)
                break
            
    for index in range(len(leaderboard_array)):
        current_member = await member_helper.get_member_name(leaderboard_array[index])
        if old_name in current_member:
            current_member = await member_helper.change_member_name(leaderboard_array[index], nick_name)
            leaderboard_array[index] = current_member
            break
    sorted_member_list = sorted(member_list.copy(),key=lambda x: x.nick)
    await update_roaster(sorted_member_list=sorted_member_list, bot=bot)

#deletes last attachment file
async def remove_file(channel) -> None:
    messages = channel.history(limit=500)

    async for message in messages:
        author = message.author
        if author.id == settings.bot_id and message.attachments:
            await message.delete()
            break