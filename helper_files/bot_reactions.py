'''
This file holds all methods related reaction listening
on_reaction_add_duel: updates the leaderboard accordingly
on_reaction_add_global_duel: updates global leaderboard accordingly
on_reaction_add_public: updates leaderboard accordingly
on_reaction_add_scrim: adds user to scrim
on_reaction_remove_scrim: removes user from scrim
on_reaction_add_scrim_results: assigns points to scrim users according to win or lose reaction
'''
import discord
import settings, file_updates, bot_commands, global_leaderboard, scrim
import re
import random


#checks to see if white check mark reaction was added to duel result
async def on_reaction_add_duel(reaction:discord.Reaction,user: discord.Member, bot) -> None:
    channel = bot.get_channel(settings.one_vs_one_id)
    if reaction.message.channel == channel and user != bot.user:
        if reaction.emoji == "✅":
            if user.get_role(settings.mod) is not None or user.get_role(settings.leader) is not None:
                message_string = reaction.message.content
                battle_result = re.search(r"(<@[0-9]+>[\s]*)+(>)[\s]*(<@[0-9]+>[\s]*)+", message_string)
                tie = re.search(r"(<@[0-9]+>[\s]*)+(=)[\s]*(<@[0-9]+>[\s]*)+", message_string)
                if battle_result or tie:
                    if len(reaction.message.mentions) == 2:
                        tie_game = False
                        message_string = reaction.message.content
                        winner_array = []
                        loser_array = []

                        if tie:
                            tie_game = True
                            members_winners = re.search(r"(<@[0-9]+>[\s]*)+(=)", message_string).group()[:-1].split()
                            members_losers = re.search(r"(=)[\s]*(<@[0-9]+>[\s]*)+", message_string).group()[1:].split()
                        else:
                            members_winners = re.search(r"(<@[0-9]+>[\s]*)+(>)", message_string).group()[:-1].split()
                            members_losers = re.search(r"(>)[\s]*(<@[0-9]+>[\s]*)+", message_string).group()[1:].split()

                        for winner in members_winners:
                            temp = winner[2:-1]
                            member = user.guild.get_member(int(temp))
                            if member is not None:
                                winner_array.append(member)
                            else:
                                print("Cannot find member for duel")
                        
                        for loser in members_losers:
                            temp = loser[2:-1]
                            member = user.guild.get_member(int(temp))
                            if member is not None:
                                loser_array.append(member)
                            else:
                                print("Cannot find member for duel")

                        await file_updates.update_leaderboard(bot, winner=winner_array,loser=loser_array,duel=True, is_tie=tie_game)

#checks to see if thumbs up  reaction was added to global duel result
async def on_reaction_add_global_duel(reaction:discord.Reaction,user: discord.Member, bot) -> None:
    channel = bot.get_channel(settings.one_vs_one_id)
    if reaction.message.channel == channel and user != bot.user:
        if reaction.emoji == "👍":
            if user.get_role(settings.mod) is not None or user.get_role(settings.leader) is not None:
                message_string = reaction.message.content
                battle_result = re.search(r"<@[0-9]+>[\s]+>[\s]+<@[0-9]+>", message_string)
                if battle_result:
                    if len(reaction.message.mentions) == 2:
                        first_mem = reaction.message.mentions[0]
                        second_mem = reaction.message.mentions[1]
                        message_string = reaction.message.content

                        message_string = message_string.replace('<', ' ')
                        message_string = message_string.replace('>',' ')
                        message_string = message_string.strip()
                        message_array = message_string.split(' ', 1)
                        message_array[0].strip()

                        if first_mem.get_role(settings.comp) is not None and second_mem.get_role(settings.comp) is not None:
                            if ('@' + str(first_mem.id)) == message_array[0]:
                                await global_leaderboard.battle(first_mem, second_mem, bot)
                            else:
                                await global_leaderboard.battle(second_mem, first_mem, bot)
                        else:
                            await channel.send("Both participants must be have the comp role to fight.")

#checks to see if white check mark reaction was added to public duel result
async def on_reaction_add_public(reaction:discord.Reaction,user: discord.Member, bot) -> None:
    channel = bot.get_channel(settings.media_id)
    if reaction.message.channel == channel and user != bot.user:
        if reaction.emoji == "✅":
            if user.get_role(settings.mod) is not None or user.get_role(settings.leader) is not None:
                message_string = reaction.message.content
                battle_result = re.search(r"<@[0-9]+>[\s]+[0-9]+", message_string)
                if battle_result:
                    message_string = reaction.message.content
                    message_array = message_string.split(' ', 1)
                    try:
                        score = float(message_array[1].strip())/10
                    except Exception as error:
                        print(error + ": On Reaction Add Public Method")


                    await bot_commands.manual_update_leaderboard(reaction.message.channel, user, score, bot, override=False)

#checks to see if white check mark reaction was added to scrim
async def on_reaction_add_scrim(reaction:discord.Reaction,user: discord.Member, bot) -> None:
    channel = bot.get_channel(settings.upcoming_scrim_id)
    if reaction.message.channel == channel and user != bot.user:        
        if reaction.emoji == "✅":
            if len(settings.current_players) < settings.max_players:
                name = user.nick
                if user.nick is None:
                    name = user.name
                settings.current_players.append(user)
                await scrim.add_to_scrim(name, reaction.message, bot)
                team_channel = bot.get_channel(settings.team_chat_id)
                await team_channel.send(name + " has joined the scrim!")

                if len(settings.current_players) == settings.max_players:
                    await team_channel.send("Attention everyone, all slots for the scrim have been filled! Best of luck to those participating. " +
                                            str(random.choice(settings.scrim_msg_array)))
            else:
                team_channel = bot.get_channel(settings.team_chat_id)
                await team_channel.send("All slots are aleady taken, if someone is listed who is not participating in the scrim, please contact a leader or moderator.")
                await reaction.clear()

#checks to see if white check mark reaction was added to scrim
async def on_reaction_remove_scrim(reaction:discord.Reaction, user:discord.Member, bot) -> None:
    channel = bot.get_channel(settings.upcoming_scrim_id)
    if reaction.message.channel == channel and user != bot.user:        
        if reaction.emoji == "✅":
            name = user.nick
            if user.nick is None:
                name = user.name
            await scrim.remove_from_scrim(name, reaction.message, bot)
            settings.current_players.remove(name)
            team_channel = bot.get_channel(settings.team_chat_id)
            await team_channel.send(name + " has left the scrim!")
            
#checks to see what result reaction was sent and assigns points accordingly
async def on_reaction_add_scrim_results(reaction:discord.Reaction,user: discord.Member, bot) -> None:
    channel = bot.get_channel(settings.upcoming_scrim_id)

    if reaction.message.channel == channel and user != bot.user and len(settings.current_players) > 0:
        if user.get_role(settings.mod) is not None or user.get_role(settings.leader) is not None:
            if reaction.emoji == "☑️":
                winning_sentence = random.choice(settings.scrim_win_msg_array)
                points = settings.winning_points
                end_sentence = random.choice(settings.scrim_end_msg_array)
                if end_sentence == "Hey some points have been awarded to ":
                    end_sentence = end_sentence + ','.join(settings.current_players) + "!"
                msg = winning_sentence + ' ' + points + ' points have been awarded for participating in the recent scrim. ' + end_sentence

                for player in settings.current_players:
                    await bot_commands.manual_update_leaderboard(reaction.message, player, float(points), bot, override=False)

                team_channel = bot.get_channel(settings.team_chat_id)
                await team_channel.send(msg)

                settings.current_players = []
                
            if reaction.emoji == "❎":
                losing_sentence = random.choice(settings.scrim_lose_msg_array)
                points = settings.losing_points
                end_sentence = random.choice(settings.scrim_end_msg_array)
                if end_sentence == "Hey some points have been awarded to ":
                    end_sentence = end_sentence + ','.join(settings.current_players) + "!"
                msg = losing_sentence + ' ' + points + ' points have been awarded for participating in the recent scrim. ' + end_sentence

                for player in settings.current_players:
                    await bot_commands.manual_update_leaderboard(reaction.message, player, float(points), bot, override=False)

                team_channel = bot.get_channel(settings.team_chat_id)
                await team_channel.send(msg)
            
                settings.current_players = []
