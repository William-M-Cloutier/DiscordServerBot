'''
This file holds all methods related to updating a user rank.
update_rank: updates a user's rank in the leaderboard accordingly
find_currend_rank_index: finds rank of user
daily_decay: decay user's score and rank accordingly
yearly_reset: resets user's rank
member_duel: updates rank and score from duel result accordingly
set_tryout_manager: gives the top four members of leaderboard the tryout manager role
'''

import discord
import settings, member_helper, inactive

#updates a user's rank from given score
async def update_rank(member:discord.Member, current_score) -> None:
    index = await find_current_rank_index(member)
    if index == -1: #if -1, they have no rank so give them Gen None rank as precaution
        await member.add_roles(member.guild.get_role(settings.gen_none))
    
    current_role = member.get_role(settings.rank_list[index])

    new_rank_index = 0
    rank_mile_len = len(settings.rank_milestones)
    for rank_index in range(rank_mile_len):
        if current_score < settings.rank_milestones[rank_index]:
            if rank_index + 1 < rank_mile_len:
                new_rank_index = rank_index + 1
            else:
                new_rank_index = rank_index
        else:
            break
    new_role = member.guild.get_role(settings.rank_list[new_rank_index])

    if 'Captain' in new_role.name:
        if len(new_role.members) == 0:
            await member.remove_roles(current_role)
            await member.add_roles(new_role)
            if member.get_role(settings.cap_gen_1_8) is None:
                await member.add_roles(member.guild.get_role(settings.cap_gen_1_8))

    elif (new_role != member.guild.get_role(settings.gen_none) 
          and  new_role != member.guild.get_role(settings.gen_9) 
          and len(new_role.members) < 5):
        
        await member.remove_roles(current_role)
        await member.add_roles(new_role)
        if member.get_role(settings.cap_gen_1_8) is not None:
            await member.remove_roles(member.guild.get_role(settings.cap_gen_1_8))

    elif (new_role == member.guild.get_role(settings.gen_none)
          or new_role == member.guild.get_role(settings.gen_9)):
        await member.remove_roles(current_role)
        await member.add_roles(new_role)
        if member.get_role(settings.cap_gen_1_8) is not None:
            await member.remove_roles(member.guild.get_role(settings.cap_gen_1_8))

    elif current_role == member.guild.get_role(settings.gen_none):
        if current_score >= 90 and current_score <= 100:
            await member.remove_roles(current_role)
            await member.add_roles(member.guild.get_role(settings.gen_9))
            if member.get_role(settings.cap_gen_1_8) is not None:
                await member.remove_roles(member.guild.get_role(settings.cap_gen_1_8))

#gets the index of the rank list corresponding to member's role rank    
async def find_current_rank_index(member:discord.Member) -> int:
    for index in range(len(settings.rank_list)):
        if member.get_role(settings.rank_list[index]) is not None:
            return index
    return -1

#subtracts 1 from each member's score
async def daily_decay(leaderboard_array, member_list, bot) -> None:
    activity_board = await inactive.get_activity_board(bot)
    for index in range(len(leaderboard_array)):
        decay_score = -1
        
        if activity_board:
            member_info = [s for s in activity_board if await member_helper.get_member_name(leaderboard_array[index]) in s]
            if member_info:
                if await member_helper.get_member_score(leaderboard_array[index]) > 30:
                    inactive_score = await inactive.get_score(member_info[0])
                    inactive_score -= 6
                    if inactive_score > 0:
                        decay_score -= inactive_score

        leaderboard_array[index] = await member_helper.change_member_score(leaderboard_array[index], decay_score)

    for member in member_list:
        member_nick = member.nick
        if member_nick is None:
            member_nick = await member_helper.set_nick_prefix(member)

        for leaderboard_member in leaderboard_array:
            if await member_helper.get_member_name(leaderboard_member) == member_nick:
                score = await member_helper.get_member_score(leaderboard_member)
                if score <= 0:
                    await inactive.revoke(member, bot)
                    break
                elif score <= 5:
                    await inactive.second_warning(member)
                elif score <= 10:
                    await inactive.first_warning(member, bot)
                await update_rank(member, score)
                break

#sets every member's score to the base score (50 but can be changed at top of file)
async def yearly_reset(leaderboard_array) -> None:
    for index in range(len(leaderboard_array)):
        leaderboard_array[index] = await member_helper.change_member_score(leaderboard_array[index], 0, is_reset=True)
  
#adds the winning score to the winner and the losing score to the loser (score amounds can be changed at top of file)
async def member_duel(leaderboard_array, winner_array:list[discord.Member], loser_array:list[discord.Member], is_tie) -> None:
    for winner in winner_array:
        score = await get_score_amount(winner, won=True, tie=is_tie)
        for index in range(len(leaderboard_array)):
            current_member = await member_helper.get_member_name(leaderboard_array[index])
            if current_member == winner.nick:
                leaderboard_array[index] = await member_helper.change_member_score(leaderboard_array[index], score)
                await update_rank(winner, await member_helper.get_member_score(leaderboard_array[index]))
                break

    for loser in loser_array:
        score = await get_score_amount(loser, lose=True, tie=is_tie)
        for index in range(len(leaderboard_array)):
            current_member = await member_helper.get_member_name(leaderboard_array[index])
            if current_member == loser.nick:
                leaderboard_array[index] = await member_helper.change_member_score(leaderboard_array[index], score)
                await update_rank(loser, await member_helper.get_member_score(leaderboard_array[index]))
                break

#returns score to be added to member
async def get_score_amount(member:discord.Member, won=False, lose=False, tie=False) -> int:
    rank_index = await find_current_rank_index(member)
    if tie:
        return settings.rank_tie_score[rank_index]
    elif won:
        return settings.rank_win_score[rank_index]
    elif lose:
        return settings.rank_lose_score[rank_index]
    return 0

#gives the top four members of leaderboard the tryout manager role
async def set_tryout_manager(top_users_array, guild:discord.Guild, member_list: list[discord.Member]) -> None:
    tryout_role = guild.get_role(settings.tryout_manager)
    tryout_members = tryout_role.members

    for member in tryout_members:
        await member.remove_roles(tryout_role)

    users_name_array = []

    for entry in top_users_array:
        users_name_array.append(await member_helper.get_member_name(entry))
    
    for member in member_list:
        if member.nick in users_name_array:
            await member.add_roles(tryout_role)

    

