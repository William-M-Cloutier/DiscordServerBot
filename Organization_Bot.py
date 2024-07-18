
import sys
sys.path.append('helper_files')

import discord
from discord.ext import commands, tasks
import bot_reactions, settings, bot_commands, timed_events, inactive, bot_on_message
from typing import Optional
#allows bot to view messages and members
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


#------------------------Commands----------------------------#
#check to see if command came from user within #Roaster-Update
async def in_roaster_update(ctx) -> bool:
    return ctx.channel.id == settings.roaster_update_id

#check to see if command came from user within #owner
async def in_owner(ctx) -> bool:
    return ctx.channel.id == settings.owner_id

async def in_update_scrim(ctx) -> bool:
    return ctx.channel.id == settings.upcoming_scrim_id

@bot.command(name='add')
@commands.has_permissions(manage_roles=True)
@commands.check(in_roaster_update)
async def add_user(ctx, member: discord.Member, ingame_username, clan_name=None) -> None:
    await bot_commands.add_user(ctx, member,ingame_username, clan_name)

@bot.command(name='remove')
@commands.has_permissions(manage_roles=True)
@commands.check(in_roaster_update)
async def remove_user(ctx, member_input) -> None:
    await bot_commands.remove_user(ctx, member_input)

#changes a user's name in roaster/leaderboard
@bot.command(name='change')
@commands.check(in_roaster_update)
async def change_user(ctx, old_name, member:discord.Member) -> None:
    await bot_commands.change_user(old_name, member, ctx.bot)

@bot.command(name='createGL')
@commands.check(in_owner)
async def create_GL(ctx) -> None:
    await bot_commands.create_gl(ctx.bot)

@bot.command(name='update')
@commands.check(in_owner)
#Allows someone in the owner channel to manually change a member's score
async def manual_update_leaderboard(ctx, member:discord.Member, score:str) -> None:
    override_score = True
    if score[0] == '+':
        score = float(score[1:])
        override_score = False
    elif score[0] == '-':
        score = -1 * float(score[1:])
        override_score = False
    else:
        try:
            score = float(score)
        except:
            ctx.send("Error: Incorrect input. Either enter a number or +(num) or -(num).")
            score = float(0)
            override_score = False
    
    await bot_commands.manual_update_leaderboard(ctx, member, score, bot, override=override_score)

@bot.command(name='addscrim')
@commands.check(in_update_scrim)
async def addscrim(ctx, clan:str, time:str, date:str, timezone:str, password:Optional[str] = ' ', 
                   num_players:Optional[int] = 5, points:Optional[str] = None) -> None:
    settings.max_players = num_players
    settings.current_players = [] 
    flag = True

    if ',' in password:
        points = password
        password = ' '
    
    try:
        int(password)
    except ValueError:
        flag = False
    
    if flag:
        num_players = int(password)
        password = ' '

    if points is not None:
        point_arr = points.split(',')
        settings.winning_points = point_arr[0]
        settings.losing_points = point_arr[1]
    else:
        settings.winning_points = "40"
        settings.losing_points = "20"

    await bot_commands.add_scrim(clan, time, date, password, timezone, ctx.bot)    


#------------------------End Commands----------------------------#


#---------------------------Errors-------------------------------#

#error if someone tries to use the add in wrong channel
@add_user.error
async def add_user_error(ctx, error) -> None:
    if isinstance(error, commands.CheckFailure):
        await ctx.send('The add command can only be done in the channel: Roaster Update.')

#error if someone tries to use the remove in wrong channel
@remove_user.error
async def remove_user_error(ctx, error) -> None:
    if isinstance(error, commands.CheckFailure):
        await ctx.send('The remove command can only be done in the channel: Roaster Update.')

#error if someone tries to use the update in wrong channel
@manual_update_leaderboard.error
async def manual_update_leaderboard_error(ctx, error) -> None:
    if isinstance(error, commands.CheckFailure):
        await ctx.send('The update command can only be done in the channel: Owner.')

#-------------------------End Errors-----------------------------#


#---------------------------Events-------------------------------#

# #checks to see if a duel result has been posted
@bot.event
async def on_message(message: discord.Message) -> None:
    await bot_on_message.on_message_duel(message, bot)
    await bot_on_message.on_message_public(message, bot)
    await bot_on_message.on_message_active(message, bot)
    await bot_on_message.on_leaderboard_update(message, bot)
    await bot.process_commands(message)

#checks to see if white check mark reaction was added to message
@bot.event
async def on_reaction_add(reaction:discord.Reaction, user:discord.Member) -> None:
    await bot_reactions.on_reaction_add_duel(reaction, user, bot)
    await bot_reactions.on_reaction_add_scrim(reaction, user, bot)
    await bot_reactions.on_reaction_add_scrim_results(reaction, user, bot)
    await bot_reactions.on_reaction_add_public(reaction, user, bot)
    await bot_reactions.on_reaction_add_global_duel(reaction, user, bot)
    await bot.process_commands(reaction.message)

@bot.event
async def on_reaction_remove(reaction:discord.Reaction, user:discord.Member) -> None:
    await bot_reactions.on_reaction_remove_scrim(reaction, user, bot)
    await bot.process_commands(reaction.message)

@tasks.loop(hours=24)
async def check_name_change() -> None:
    if check_name_change.current_loop == 0:
        await timed_events.check_name_change(bot, first_run=True)
    else:
        await timed_events.check_name_change(bot)

@tasks.loop(hours=24)
async def start_daily_decay() -> None:
    if start_daily_decay.current_loop != 0:
        await timed_events.start_daily_decay(bot)

@tasks.loop(hours=24)
async def start_yearly_reset() -> None:
    if start_yearly_reset.current_loop != 0:
        await timed_events.start_yearly_reset(bot)

@tasks.loop(hours=24)
async def check_age() -> None:
    if check_age.current_loop != 0:
        await timed_events.check_age(bot)

@tasks.loop(hours=24)
async def add_to_inactive() -> None:
    if add_to_inactive.current_loop != 0:
        await inactive.add_to_inactive(bot)

@tasks.loop(hours=2190) #around 3 months
async def reset_global_ranks() -> None:
    if reset_global_ranks.current_loop != 0:
        await timed_events.reset_global_ranks(bot)


#-------------------------End Events-----------------------------#


@bot.event
async def on_ready() -> None:
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    start_daily_decay.start()
    start_yearly_reset.start()
    check_age.start()
    add_to_inactive.start()
    reset_global_ranks.start()
    check_name_change.start()

def run_discord_bot() -> None:
    token = ''
    bot.run(token)

if __name__ == '__main__':
    settings.init()
    run_discord_bot()