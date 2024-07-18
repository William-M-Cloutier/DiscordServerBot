'''
This file holds all methods related any timed events
start_daily_decay: creates daily decay on leaderboards
start_yearly_reset: resets leaderboards every year
reset_global_ranks: resets everyones global rank
check_age: assigns a role to each user based on time in server
check_name_change: checks to see if a user's nickname has changed recently, if it has it updates leaderboard accordingly
'''

import discord
import settings, file_updates, global_leaderboard, member_helper
from datetime import datetime, timezone, timedelta

#starts the daily score decay
async def start_daily_decay(bot) -> None:
    message_channel = bot.get_channel(settings.leaderboard_roaster_id)
    await file_updates.update_leaderboard(bot, daily=True)
    await message_channel.send("Daily Decay! All ranks go down a point!")

#resets all scores to 50
async def start_yearly_reset(bot) -> None:
    target_date = '01-01'
    current_date = datetime.today().strftime('%m-%d')
    if target_date == current_date:
        message_channel = bot.get_channel(settings.leaderboard_roaster_id)
        await file_updates.update_leaderboard(bot, yearly=True)
        await message_channel.send("It's been a whole year! Time to reset the ranks!")

#resets global ranks
async def reset_global_ranks(bot) -> None:
    await global_leaderboard.reset_ranks(bot)
    channel = bot.get_channel(settings.information_id)
    await channel.send("It has been three months. Global ranks have now reset. Everyone is now comp rank")

#assigns role from duration in server
async def check_age(bot) -> None:
    guild = bot.get_guild(settings.server_id)
    member_list = guild.members
    today = datetime.now(timezone.utc)
    age_roles = []
    for index in range(len(settings.age_roles)):
        age_roles.append(guild.get_role(settings.age_roles[index]))

    for member in member_list:
        join_time = member.joined_at
        diff = today - join_time
        total_months = int(diff.days)

        for index in range(len(settings.age_roles)):
            role = member.get_role(settings.age_roles[index])
            if role is not None:
                await member.remove_roles(role)
                break
 

        if total_months < 30 * 1:
            await member.add_roles(age_roles[0])
        elif total_months < 30 * 2:
            await member.add_roles(age_roles[1])
        elif total_months < 30 * 3:
            await member.add_roles(age_roles[2])
        elif total_months < 30 * 6:
            await member.add_roles(age_roles[3])
        elif total_months < 30 * 9:
            await member.add_roles(age_roles[4])
        elif total_months < 30 * 12: #1 year
            await member.add_roles(age_roles[5])
        elif total_months < 30 * 24: #2 years
            await member.add_roles(age_roles[6])
        elif total_months < 30 * 36: #3 years
            await member.add_roles(age_roles[7])
        elif total_months < 30 * 48: #4 years
            await member.add_roles(age_roles[8])
        elif total_months < 30 * 60: #5 years
            await member.add_roles(age_roles[9])
        elif total_months < 30 * 72: #6 years
            await member.add_roles(age_roles[10])
        elif total_months < 30 * 84: #7 years
            await member.add_roles(age_roles[11])
        elif total_months < 30 * 96: #8 years
            await member.add_roles(age_roles[12])
        elif total_months < 30 * 108: #9 years
            await member.add_roles(age_roles[13])
        else: #9+ years
            await member.add_roles(age_roles[14])

#checks to see if a user's nickname has changed recently, if it has it updates leaderboard accordingly
async def check_name_change(bot, first_run=False) -> None:
    guild = bot.get_guild(settings.server_id)
    member_list = []
    current_info = []
    for clan in settings.clan_info_array:
        role = guild.get_role(clan[1])
        if role is not None:
            member_list += role.members.copy()
    
    for index in range(len(member_list)):
        if member_list[index].nick is None:
            member_list[index].nick = await member_helper.set_nick_prefix(member_list[index])
        current_info.append((member_list[index], member_list[index].nick))

    if first_run:
        settings.member_name_array = current_info.copy()
    else:
        for global_index in range(len(settings.member_name_array)):
            for member_info in current_info:
                if settings.member_name_array[global_index][0] == member_info[0]:
                    if settings.member_name_array[global_index][1] != member_info[1]:
                        old_name = settings.member_name_array[global_index][1]
                        member = settings.member_name_array[global_index][0]
                        await file_updates.update_leaderboard(bot, winner=[member], user_name_update=True, old_name = old_name)
                        temp_tuple = (member, member.nick)
                        settings.member_name_array[global_index] = temp_tuple

