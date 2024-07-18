'''
This file holds all methods related to getting member information
get_member_score: gets a member's score from the leaderboard
get_member_name: gets a member's name from the leaderboard
change_member_score: changes a member's score in the leaderboard
change_member_name: changes a member's name in the leaderboard
set_nick_prefix: sets the nickname clan prefix of user
'''
import discord
import settings


#returns score of given user entry of leaderboard
async def get_member_score(leaderboard_name) -> float:
    cut_index = leaderboard_name.find(':') + 1
    score = leaderboard_name[cut_index:]
    return float(score)

#returns name of given user entry of leaderboard
async def get_member_name(leaderboard_name) -> str:
    cut_index = leaderboard_name.find(':')
    name = leaderboard_name[:cut_index]
    return name

#returns user entry for leaderboard with updated score value
async def change_member_score(member_name, amount, is_reset=False, is_override=False) -> str:
    split_member = member_name.split(':')
    score = float(split_member[1][1:])
    if is_reset:
        new_score = settings.base_score
    elif is_override:
        new_score = float(amount)
    else:
        new_score = score + float(amount)

    updated_member = split_member[0] + ": " + ("%.2f" % new_score)
    return updated_member


#returns user entry for leaderboard with updated name
async def change_member_name(member_name, desired_name) -> str:
    split_member = member_name.split(':')
    score = float(split_member[1][1:])
    
    # split_name = split_member[0].split(' ')


    updated_member = desired_name + ": " + ("%.2f" % score)
    return updated_member

#sets the nickname clan prefix of user
async def set_nick_prefix(member: discord.Member) -> str:
    for clan in settings.clan_info_array:
        if member.get_role(clan[1]) is not None:
            member_nick = "[f{clan[0]}] " + member.name
            return member_nick
