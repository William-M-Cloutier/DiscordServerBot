'''
This file holds all methods related to scrims
create_scrim: creates the scrim text file
add_to_scrim: adds a member to the scrim
remove_from_scrim: removes a member to the scrim
'''
import discord
import tempfile
import os
from datetime import date
import settings

#creates scrim file
async def create_scrim(header, bot) -> None:
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding='utf-8') as tmp:
        tmp.write(header)
        tmp.close()
        file_name = "Scrim" + str(date.today()) + ".txt"
        channel = bot.get_channel(settings.upcoming_scrim_id)
        scrim_file = discord.File(tmp.name, filename=file_name)
        await channel.send(file=scrim_file)
        os.unlink(tmp.name)

#adds user to scrim file
async def add_to_scrim(nickname, message, bot) -> None:
    scrim_bytes = await message.attachments[0].read()

    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding='utf-8') as tmp:
        scrim_contents = scrim_bytes.decode()
        scrim_array = scrim_contents.splitlines()
        scrim_array.append(nickname)
        scrim_content = '\n'.join(scrim_array)
        tmp.write(scrim_content)

        tmp.close()
        file_name = "Scrim_" + str(date.today()) + ".txt"
        scrim_file = discord.File(tmp.name, filename=file_name)
        await message.edit(attachments=[scrim_file])
        os.unlink(tmp.name)

#removes user from scrim file
async def remove_from_scrim(nickname, message, bot) -> None:
    scrim_bytes = await message.attachments[0].read()

    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding='utf-8') as tmp:
        scrim_contents = scrim_bytes.decode()
        scrim_array = scrim_contents.splitlines()
        scrim_array.remove(nickname)
        scrim_content = '\n'.join(scrim_array)
        tmp.write(scrim_content)

        tmp.close()
        file_name = "Scrim_" + str(date.today()) + ".txt"
        scrim_file = discord.File(tmp.name, filename=file_name)
        await message.edit(attachments=[scrim_file])
        os.unlink(tmp.name)