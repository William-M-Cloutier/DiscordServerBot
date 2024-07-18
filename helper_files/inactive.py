'''
This file holds all methods related to inactivity
add_to_inactive: adds [Death] members to inactive board
update_active: updates the active board accordingly
first_warning: warns user publically they need to be active
second_warning: warns user privately they need to be active
revoke: revokes a user's [Death] ranks and related items
get_score: grabs a user's inactive score from active board
sort_array: helper method to call quicksort on array
quick_sort: uses quick sort on array
partition: partitions array for quicksort
get_activity_board: returns the activity board
'''
import discord
import tempfile
import os
from datetime import date, datetime
import settings, bot_commands, member_helper



#adds new member to the activity board text file
#format:
#Name: DaysInactive, DateAddedToBoard
async def add_to_inactive(bot) -> None:
    activity_board_channel = bot.get_channel(settings.information_id)
    messages = activity_board_channel.history()
    activity_board_bytes = None

    guild = bot.get_guild(settings.server_id)
    member_list = []

    for clan in settings.clan_info_array:
        role = guild.get_role(clan[1])
        if role is not None:
            member_list.append(role.members.copy())

    async for message in messages:
        author = message.author
        if author.id == settings.bot_id and message.attachments:
            activity_board_bytes = await message.attachments[0].read()
            await message.delete()
            break

    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding='utf-8') as tmp:
        if activity_board_bytes is not None: #add member to exisiting activity_board
            activity_board_contents = activity_board_bytes.decode()
            activity_board_array = activity_board_contents.splitlines()
            await update_active(activity_board_array, member_list, bot)
            await sort_array(activity_board_array)
            activity_board_content = '\n'.join(activity_board_array)
            tmp.write(activity_board_content)

        else:#create new activity_board and add member
            activity_board_array = []
            await update_active(activity_board_array, member_list, bot)
            await sort_array(activity_board_array)
            activity_board_content = '\n'.join(activity_board_array)
            tmp.write(activity_board_content)

        tmp.close()
        file_name = "Activity_Board_" + str(date.today()) + ".txt"
        channel = bot.get_channel(settings.information_id)
        activity_board_file = discord.File(tmp.name, filename=file_name)
        await channel.send(file=activity_board_file)
        os.unlink(tmp.name)
        settings.active_array = []

#updates the activity board file
async def update_active(activity_board, member_list, bot) -> None:
    today = datetime.today().strftime('%d/%m')
    for index in range(len(member_list)):
        if member_list[index].id == settings.bot_id:
            continue
        if member_list[index].nick is None:
                member_list[index].nick = await member_helper.set_nick_prefix(member_list[index])

        member_info = [s for s in activity_board if member_list[index].nick in s]
        if member_list[index].nick in settings.active_array:
            if len(member_info) > 0:
                activity_board.remove(member_info[0])
        else:
            if len(member_info) > 0:
                active_board_index = activity_board.index(member_info[0])
                score = await get_score(activity_board[active_board_index])
                last_active_date = activity_board[active_board_index].split(str(score) + ", ")[1]
                score += 1
                activity_board[active_board_index] = member_list[index].nick + ": " + str(score) + ", "  + last_active_date
            else:
                info = member_list[index].nick + ": " + "1, " + today
                activity_board.append(info)


#publically warns user for being inactive
async def first_warning(member:discord.Member, bot) -> None:
    channel = bot.get_channel(settings.team_chat_id)
    await channel.send(f"{member.mention}, Attention! You've reached 10 points and are on the verge of removal. Increase your activity. Note: At 5 points, a private reminder will also be sent.")

#privately warns user for inactivity
async def second_warning(member:discord.Member) -> None:
    await member.send(f"{member.mention}, You've now reached 5 points. Critical warning: You're very close to removal. Take action now to secure your place. Further inactivity will lead to expulsion.")

#revokes user's clan related roles due to being inactive
async def revoke(member:discord.Member, bot) -> None:
    channel = bot.get_channel(settings.general_id)
    await channel.send(f'{member.mention} has been removed due to lack of activity.')
    channel = bot.get_channel(settings.roaster_update_id)
    msgs = channel.history(limit=1)
    msg = None
    async for message in msgs:
        msg = message
        break
    ctx = await bot.get_context(msg)
    await bot_commands.remove_user(ctx, str(member.id))

#gets a user's name and inactive score from inactive board file
async def get_score(member_info) -> int:
    name_else_arr = member_info.split(':',1)
    score = name_else_arr[1].strip().split(',',1)[0]

    return int(score)

#helper to call on quick_sort for array
async def sort_array(array) -> None:
    await quick_sort(array, 0, len(array)-1)

#quick sorts given array
async def quick_sort(array, low, high) -> None:
    if low < high:
        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = await partition(array, low, high)
        # Recursive call on the left of pivot
        await quick_sort(array, low, pi - 1)

        # Recursive call on the right of pivot
        await quick_sort(array, pi + 1, high)
 
#partitions the array for quicksort
async def partition(array, low, high) -> int:
    # choose the rightmost element as pivot
    pivot = await get_score(array[high])
 
    # pointer for greater element
    i = low - 1
 
    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if await get_score(array[j]) >= pivot:
 
            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1
 
            # Swapping element at i with element at j
            (array[j], array[i]) = (array[i], array[j])
 
    # Swap the pivot element with the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])
 
    # Return the position from where partition is done
    return i + 1

async def get_activity_board(bot) -> list:
    activity_board_channel = bot.get_channel(settings.information_id)
    messages = activity_board_channel.history()
    activity_board_bytes = None


    async for message in messages:
        author = message.author
        if author.id == settings.bot_id and message.attachments:
            activity_board_bytes = await message.attachments[0].read()
            break
    if activity_board_bytes is None:
        return []


    activity_board_contents = activity_board_bytes.decode()
    activity_board_array = activity_board_contents.splitlines()

    return activity_board_array