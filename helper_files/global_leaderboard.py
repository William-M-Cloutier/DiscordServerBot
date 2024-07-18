'''
This file holds all methods related to global leaderboard
create_global_leaderboard: creates the global leaderboard accordingly
battle: updates the global leaderboard ranks according to battle result
update_rank_roles: updates the ranks
demote: demotes a member and all members below them
get_league: determine what league group a rank is in
reset_ranks: resets all global leaderboard ranks
'''
import discord
import tempfile
import os
from datetime import date
import settings, file_updates, member_helper

#creates a global leaderboard
async def create_global_leaderboard(bot) -> None:
    guild = bot.get_guild(settings.server_id)
    channel = bot.get_channel(settings.global_leaderboard_id)
    await file_updates.remove_file(channel)

    leaderboard_array = []

    for role_id in settings.global_rank_list:
        role = guild.get_role(role_id)
        if len(role.members) < 1:
            member = 'Empty'
        else:
            member = role.members[0].nick
            if member is None:
                member = role.members[0].name
        info = role.name + ": " + member
        leaderboard_array.append(info)
    
    leaderboard_content = '\n'.join(leaderboard_array)

    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding='utf-8') as tmp:
        tmp.write(leaderboard_content)
        tmp.close()
        file_name = "Global_Leaderboard_" + str(date.today()) + ".txt"
        leaderboard_file = discord.File(tmp.name, filename=file_name)
        await channel.send(file=leaderboard_file)
        os.unlink(tmp.name)

#updates leaderboard from battle results
#league index: 0, 1-4, 5-8, 9-12, 13-16, 17-20, 21-24    25
            #  0   1    2    3      4      5      6      7
async def battle(winner:discord.Member, loser:discord.Member, bot) -> None:
    winner_index = 25 #default 25 for 'comp' role only
    loser_index = 25
    winner_league = 7 
    loser_league = 7

    for index in range(len(settings.global_rank_list)):
        if winner.get_role(settings.global_rank_list[index]) is not None:
            winner_league = await get_league(index)
            winner_index = index
        if loser.get_role(settings.global_rank_list[index]) is not None:
            loser_league = await get_league(index)
            loser_index = index

    if winner_league == loser_league or winner_league+1 == loser_league or winner_league-1 == loser_league:
        await update_rank_roles(winner,loser, winner_index, loser_index)
        await create_global_leaderboard(bot)
    else:
        channel = bot.get_channel(settings.one_vs_one_id)
        await channel.send("Sorry, but participants must be within the same league or one below/above to battle.")

#updates the global rank roles
async def update_rank_roles(winner:discord.Member, loser:discord.Member, winner_index, loser_index) -> None:
    #both comps
    #winner comp loser rank
    #both ranks
    if winner_index == 25 and loser_index == 25:
        for index in range(len(settings.global_rank_list)):
            role = winner.guild.get_role(settings.global_rank_list[index])
            if len(role.members) < 1:
                await winner.add_roles(role)
                break

        for index in range(len(settings.global_rank_list)):
            role = loser.guild.get_role(settings.global_rank_list[index])
            if len(role.members) < 1:
                await loser.add_roles(role)
                break
    
    if loser_index < winner_index: #lower index = higher rank
        if winner_index != 25:
            await winner.remove_roles(winner.get_role(settings.global_rank_list[winner_index]))

        await winner.add_roles(loser.get_role(settings.global_rank_list[loser_index]))
        await loser.remove_roles(loser.get_role(settings.global_rank_list[loser_index]))
        if loser_index != 24: #last rank, so loser just gets comp
            await demote(loser, loser_index)

#demotes user and everyone below them
async def demote(member:discord.Member, index) -> None:
    guild = member.guild
    curr_member = member
    prev_member = member
    for role_id in settings.global_rank_list[index+1:]:
        member_list = guild.get_role(role_id).members
        if len(member_list) < 1 :
            await prev_member.add_roles(guild.get_role(role_id))
            break
        else:
            curr_member = member_list[0]
            await prev_member.add_roles(guild.get_role(role_id))
            await curr_member.remove_roles(guild.get_role(role_id))
            prev_member = curr_member

#gets league number from rank index
async def get_league(index) -> int:
    if index == 0:
        return 0
    if index >= 1 and index <= 4:
        return 1
    if index >= 5 and index <= 8:
        return 2
    if index >= 9 and index <= 12:
        return 3
    if index >= 13 and index <= 16:
        return 4
    if index >= 17 and index <= 20:
        return 5
    if index >= 21 and index <= 24:
        return 6

#resets all user's ranks
async def reset_ranks(bot) -> None:
    guild = bot.get_guild(settings.server_id)
    for role_id in settings.global_rank_list:
        member_list = guild.get_role(role_id).members
        for member in member_list:
            await member.remove_roles(guild.get_role(role_id))
    await create_global_leaderboard(bot)



