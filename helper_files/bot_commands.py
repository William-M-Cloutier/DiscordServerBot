'''
This file holds all methods related any user commands
add_user: adds a user to the roaster and leaderboard
remove_user: removes a user from the roaster and leaderboard
change_user: changes a users name in the leaderboard and roaster
manual_update_leaderboard: changes the score of a user in the leaderboard
add_scrim: creates a scrim event
crete_gl: creates the global leaderboard
'''
import discord
import re
from datetime import date
import settings, file_updates, rank_updates, scrim, global_leaderboard

#Add user command
async def add_user(ctx, member: discord.Member, ingame_username, clan_name=None) -> None:
    guild = ctx.guild
    gen_none_role = guild.get_role(settings.gen_none)
    clan_role = guild.get_role(settings.death)
    if clan_name is None:
        clan_name = "Death"
    else:
        for clan in settings.clan_info_array:
            if clan[0].lower() == clan_name.lower():
                clan_name = clan[0]
                clan_role = guild.get_role(clan[1])
                break

    member_role = guild.get_role(settings.member_id)
    nickname = f"[{clan_name}] " + ingame_username
    await member.add_roles(gen_none_role)
    await member.add_roles(clan_role)
    await member.remove_roles(member_role)
    await member.edit(nick=nickname)
    await file_updates.update_files(ctx, member)

#remove user
async def remove_user(ctx, member_input) -> None:
    id = re.search(r"[0-9]+", member_input)
    if id is not None:
        member = ctx.guild.get_member(int(id[0]))

        if  isinstance(member, discord.Member):
            guild = ctx.guild
            role_index = await rank_updates.find_current_rank_index(member)
            if role_index == -1:
                await ctx.send("Member has no found rank")
            else:
                role = guild.get_role(settings.rank_list[role_index])
                await member.remove_roles(role)

            if member.get_role(settings.cap_gen_1_8) is not None:
                await member.remove_roles(member.get_role(settings.cap_gen_1_8))
                
            clan_role = None
            for clan in settings.clan_info_array:
                clan_role = member.get_role(clan[1])
                if member.get_role(clan[1]) is not None:
                    break
            member_role = guild.get_role(settings.member_id)
            index = member.nick.find(' ')
            game_name = member.nick[index:]
            old_name = member.nick

            await member.remove_roles(clan_role)
            await member.add_roles(member_role)
            await member.edit(nick=game_name)
            await file_updates.update_leaderboard(ctx.bot, remove_user=True, remove_member_name=old_name)
            await file_updates.update_files(ctx, member,remove_from_roaster=True)

    else:
        await file_updates.update_leaderboard(ctx.bot, remove_user=True, remove_member_name=member_input)
        await file_updates.update_files(ctx, member_input, remove_from_roaster=True)

#change user
async def change_user(old_name, member:discord.Member, bot) -> None:
    await file_updates.update_leaderboard(bot, winner=[member], user_name_update=True, old_name = old_name)


#update
async def manual_update_leaderboard(ctx, member:discord.Member, score:float, bot, override=True) -> None:
    await file_updates.update_leaderboard(bot, winner=[member], man_update=True, override=override, update_score=score)

#adds a scrim file
async def add_scrim(clan:str, time:str, date:str, password:str, timezone:str, bot) -> None:
    header = clan + " vs. Death" + "\n"
    date_line = "Date:      " + date + " " + timezone + "\n"
    time_line = "Time:      " + time + " " + timezone + "\n"
    pass_line = "Pass:      " + password + "\n"
    header_combined = header + date_line + time_line + pass_line
    await scrim.create_scrim(header_combined, bot)

#creates the global leaderboard
async def create_gl(bot) -> None:
    await global_leaderboard.create_global_leaderboard(bot)


