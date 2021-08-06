#!/usr/bin/env python3

# Imports
import asyncio
import pprint
import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import bot_functions
import secret_info
import random
from collections import Counter


###  Channel Info ###
TOKEN = secret_info.TOKEN
CHANNEL_ID = secret_info.CHANNEL_ID
GUILD_ID = secret_info.GUILD_ID
VOICE_CHANNEL = secret_info.test_voice_channel

# Message config
error_message_bad_command = "Command doesn't fit."
error_message_did_something_wrong = "Something went wrong with that command."
guilty_message_global = "I'm absolutely, l00 percent, not guilty."
naughty_message_global = "I'm absolutely, l00 percent, not naughty."
calculating_message = f"Calculating tier list..."
special_fact = f"Insert Special quote here."
send_to_naughty_jail_message = f"Go to naughty jail"


# IDs
TARGET_ID = secret_info.TARGET_ID
ADMIN_ID = secret_info.ADMIN_ID
forbidden_ids = secret_info.forbidden_ids # In case there are users who don't want to be part of the tier list/naughty checks

# Misc info
military_spending_link= f"https://media.nationalpriorities.org/uploads/discretionary_spending_pie%2C_2015_enacted.png"
bonk_image = f"https://pbs.twimg.com/media/Eqzk4gKXAAU_Y0c?format=jpg&name=large"
naughty_choices = secret_info.naughty_choices
naughty_jail_images = secret_info.naughty_jail_images
naughty_jail_sentence_time = secret_info.naughty_jail_sentence_time
mom_statuses = secret_info.mom_statuses

# VC setup
JOIN_CHANCE = secret_info.join_chance
JOIN_COOLDOWN = secret_info.join_cooldown
# mp3 files
mp3_files = secret_info.mp3_files



def main():
    # Setup
    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        # Connect to discord
        channel = client.get_channel(CHANNEL_ID)
        vchannel = client.get_channel(VOICE_CHANNEL)
        print(f"{client.user} has connected to Discord.")
        asyncio.create_task(bot_functions.random_join(vchannel, JOIN_CHANCE, JOIN_COOLDOWN))

    @client.event
    async def on_message(message):
        # get vchannel
        vchannel = client.get_channel(VOICE_CHANNEL)
        naughty_jail_role = None

        # Check if the user is in naughty jail
        try:
            naughty_jail_role = discord.utils.get(message.guild.roles, name="In Naughty Jail")
        except:
            pass
        if naughty_jail_role != None:
            # Check if the message is from TARGET
            if message.author.id == TARGET_ID:
                mocked_message = bot_functions.mock(message.content.lower())
                await message.channel.send(mocked_message)
            # Check if the author is in naughty jail
            if naughty_jail_role in message.author.roles:
                naughty_message = bot_functions.naughty_jail_message(message.author.id)
                downvote_message = f"{bot_functions.downvote_user(downvoted_id=message.author.id)} for being a sinner."
                naughty_message += downvote_message

                await message.channel.send(naughty_message)
                await message.channel.send(random.choice(naughty_jail_images))
    
        # !mock command
        if message.content.lower().lower().startswith("!mock"):
            try:
                stripped_message = bot_functions.strip_command(message.content.lower(), "!mock")
                if len(stripped_message) == 0:
                    mocker =  message.author.id
                    mocked_message_buf_1 =  bot_functions.mock("My name is ")
                    mocked_message_buf_2 =  bot_functions.mock(" and I don't know how to use \'!mock\'")
                    mocker_format = "<@" + str(mocker) +">"
                    mocked_message_final = mocked_message_buf_1 + mocker_format + mocked_message_buf_2   
                    await message.channel.send(mocked_message_final)
                else:
                    mocked_message = bot_functions.mock(stripped_message)
                    await message.channel.send(mocked_message)
            except:
                await message.channel.send(error_message_did_something_wrong)
        
        # TARGET tweet
        elif message.content.lower().startswith("!tweet"):
            try:
                await message.channel.send(bot_functions.grab_target_tweet())
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif "tweet" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids:
                    await message.channel.send(bot_functions.grab_target_tweet())
            except:
                await message.channel.send(error_message_did_something_wrong)
        
        # Upvote a user
        elif message.content.lower().startswith("!upvote"):
            try:
                # Grab upvoter and upvoted info
                upvoted_id = message.mentions[0].id
                upvoter_id = message.author.id
            # Upvote and send message
                if upvoter_id != int(client.user.mention[2:-1]):
                    await bot_functions.upvote_user(message.channel, upvoted_id, upvoter_id, name=message.mentions[0].name)
                else:
                    pass
            except Exception as e:
                print(str(e))
                await message.channel.send(error_message_did_something_wrong)
        elif "upvote" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try:
                upvoter_id = message.author.id
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids and upvoter_id != bot_mention_id:
                    ids_to_upvote = (curr_id for curr_id in mention_ids if curr_id != bot_mention_id)
                    for curr_id in ids_to_upvote:
                        user_ = await client.fetch_user(curr_id)
                        await bot_functions.upvote_user(message.channel, curr_id, upvoter_id, name=user_.name)
            except:
                await message.channel.send(error_message_did_something_wrong)

        # Downvote a user
        elif message.content.lower().startswith("!downvote"):
            try:
                downvoted_id = message.mentions[0].id
                downvoter_id = message.author.id
                # Downvote and send message
                if downvoter_id != int(client.user.mention[2:-1]):
                    downvote_message = bot_functions.downvote_user(downvoted_id, downvoter_id, message.mentions[0].name)
                    await message.channel.send(downvote_message)
                    bot_functions.set_vote_time_and_user(downvoted_id, downvoter_id)
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif "downvote" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try:
                downvoter_id = message.author.id
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids and downvoter_id != bot_mention_id:
                    ids_to_downvote = (curr_id for curr_id in mention_ids if curr_id != bot_mention_id)
                    for curr_id in ids_to_downvote:
                        user_ = await client.fetch_user(curr_id)
                        downvote_message = bot_functions.downvote_user(curr_id, downvoter_id, name=user_.name)                        
                        await message.channel.send(downvote_message)
            except:
                await message.channel.send(error_message_did_something_wrong)

        # Free someone from naughty jail
        elif ("free my man" in message.content.lower()) and message.author.id != int(client.user.mention[2:-1]):
            if message.author.id != ADMIN_ID:
                await message.channel.send(f"You really think you\'re god @<{message.author.id}>?")
                downvote_message = bot_functions.downvote_user(downvoted_id=message.author.id)                       
                await message.channel.send(downvote_message)
            else:
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids:
                    jailed_ids = (curr_id for curr_id in mention_ids if curr_id != bot_mention_id)
                    for curr_id in jailed_ids:
                        await bot_functions.free_from_jail_immediate(message.channel, curr_id)

        # Naughty warning count
        elif message.content.lower().startswith("!warning"):
            naughty_warnings = bot_functions.has_naughty_warning(message.mentions[0].id)
            if naughty_warnings == 1:
                await message.channel.send(f"<@{message.mentions[0].id}> has been warned for being too naughty.")
            else:
                await message.channel.send(f"<@{message.mentions[0].id}> has no naughty warnings.")
        elif ("warning" in message.content.lower() or "warned" in message.content.lower()) and message.author.id != int(client.user.mention[2:-1]):
            mention_ids = [mention.id for mention in message.mentions]
            bot_mention_id = int(client.user.mention[2:-1])
            if bot_mention_id in mention_ids:
                warning_ids = (curr_id for curr_id in mention_ids if curr_id != bot_mention_id)
                for curr_id in warning_ids:
                    naughty_warnings = bot_functions.has_naughty_warning(curr_id)
                    if naughty_warnings == 1:
                        await message.channel.send(f"<@{curr_id}> has been warned for being too naughty.")
                    else:
                        await message.channel.send(f"<@{curr_id}> has no naughty warnings.")

        # Get a user's naughty strikes
        elif message.content.lower().startswith("!strike"):
            naughty_strikes = bot_functions.naughty_strikes_count(message.mentions[0].id)
            if naughty_strikes == 1:
                await message.channel.send(f"<@{message.mentions[0].id}> has {naughty_strikes} naughty strike.")
            else:
                await message.channel.send(f"<@{message.mentions[0].id}> has {naughty_strikes} naughty strikes.")

        # Update notes
        elif message.content.lower().startswith("!update"):
            await bot_functions.print_update_notes(message.channel)

        # Naughty permit
        elif message.content.lower().startswith("!permit please"):
            await bot_functions.give_naughty_permit(message.channel, message.author.id)
        elif ("permit" in message.content.lower() and ("please" in message.content.lower() or "pls" in message.content.lower() or "plz" in message.content.lower()) ) and message.author.id != int(client.user.mention[2:-1]):
            mention_ids = [mention.id for mention in message.mentions]
            bot_mention_id = int(client.user.mention[2:-1])
            if bot_mention_id in mention_ids:
                await bot_functions.give_naughty_permit(message.channel, message.author.id)

        # See if someone has a naughty permit
        elif message.content.lower().startswith("!permit"):
            naughty_permit = bot_functions.has_valid_naughty_permit(message.mentions[0].id)
            if naughty_permit == True:
                await message.channel.send(f"<@{message.mentions[0].id}> has a permit to be naughty.")
            else:
                await message.channel.send(f"<@{message.mentions[0].id}> is not permitted to be naughty.")
        elif ("permit" in message.content.lower() and ("has" in message.content.lower() or "have" in message.content.lower() or "to be" in message.content.lower())) and message.author.id != int(client.user.mention[2:-1]):
            mention_ids = [mention.id for mention in message.mentions]
            bot_mention_id = int(client.user.mention[2:-1])
            if bot_mention_id in mention_ids:
                strike_ids = (curr_id for curr_id in mention_ids if curr_id != bot_mention_id)
                for curr_id in strike_ids:
                    naughty_permit = bot_functions.has_valid_naughty_permit(curr_id)
                    if naughty_permit == True:
                        await message.channel.send(f"<@{curr_id}> has a permit to be naughty.")
                    else:
                        await message.channel.send(f"<@{curr_id}> is not permitted to be naughty.")
        
        # Check if a user is in naughty jail
        elif message.content.lower().startswith("!jail"):
            await bot_functions.print_jail(message.channel)
        elif ("jail" in message.content.lower() and ("whos" in message.content.lower() or "who's" in message.content.lower() or "whose" in message.content.lower() or "who" in message.content.lower())) and message.author.id != int(client.user.mention[2:-1]):
            await bot_functions.print_jail(message.channel)

        # Create someone in the database
        elif message.content.lower().startswith("!create"):
            try:
                user_to_create_id = message.mentions[0].id
                creator_id = message.author.id
                
                creation_message = bot_functions.create_user(user_to_create_id, creator_id, name=message.mentions[0].name)
                await message.channel.send(" " + creation_message)
            except Exception as e:
                print(e)
                await message.channel.send("Who(m) do you want me to create?")
        elif "create" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try:
                creator_id = message.author.id
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids:
                    ids_to_create = (curr_id for curr_id in mention_ids if curr_id != bot_mention_id)
                    for curr_id in ids_to_create:
                        user_ = await client.fetch_user(curr_id)
                        creation_message = bot_functions.create_user(curr_id, creator_id, name=user_.name)
                        await message.channel.send(" " + creation_message)
            except:
                await message.channel.send(error_message_did_something_wrong)

        # Print the tier list
        elif message.content.lower().startswith("!tier"):
            try:
                if not bot_functions.tier_list_is_up_to_date():
                    bot_functions.calc_tier_list()
                    await message.channel.send(calculating_message)
                tier_list = bot_functions.print_tier_list()
                tier_list = ''.join((line + '\n') for line in tier_list if line != "")
                await message.channel.send(tier_list)
            except Exception as e:
                print(str(e))
                await message.channel.send(error_message_did_something_wrong)
        elif "tier" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            mention_ids = [mention.id for mention in message.mentions]
            bot_mention_id = int(client.user.mention[2:-1])
            if bot_mention_id in mention_ids:
                try:
                    if not bot_functions.tier_list_is_up_to_date():
                        bot_functions.calc_tier_list()
                        await message.channel.send(calculating_message)
                    tier_list = bot_functions.print_tier_list()
                    tier_list = ''.join((line + '\n') for line in tier_list)
                    await message.channel.send(tier_list)
                except:
                    await message.channel.send(error_message_did_something_wrong)

        # Naughtiest (naughty check)
        elif ("naughtiest" in message.content.lower() or "naughtdog" in message.content.lower() or "naught dog" in message.content.lower())  and message.author.id != int(client.user.mention[2:-1]):
            try: 
                members = client.get_guild(GUILD_ID).members
                final_members = [member for member in members if member.id not in forbidden_ids]
                chosen_naughtdog_id, chosen_naughtdog_name = bot_functions.naughty_check(final_members)
                final_message = bot_functions.naughty_quote_generator(chosen_naughtdog_name)
                await message.channel.send(final_message)
                await bot_functions.give_naughty_strike_or_warning_or_jail(client.get_channel(CHANNEL_ID), chosen_naughtdog_id, naughty_offender_name=chosen_naughtdog_name)
            except TypeError as e:
                print("all is well:" + str(e))
                pass
            except:
                await message.channel.send(error_message_did_something_wrong)

        # Get the status of someone's dearest
        elif (("mom" in message.content.lower() or "mother" in message.content.lower()) and "how" in message.content.lower()  and message.author.id != int(client.user.mention[2:-1])):
            try:
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids and message.author.id != bot_mention_id:

                    ids_of_moms = (curr_id for curr_id in mention_ids if curr_id != bot_mention_id)

                    for curr_id in ids_of_moms:
                        mom_or_mother = [f"mom", "mother"]
                        mom_message = f"<@{curr_id}>'s {random.choice(mom_or_mother)} {random.choice(mom_statuses)}"                    
                        await message.channel.send(mom_message)
            except TypeError as e:
                print("all is well:" + str(e))
                pass
            except:
                await message.channel.send(error_message_did_something_wrong)
                
        # Get a dog fact
        elif message.content.lower().startswith("!dogs_source") or message.content.lower().startswith("!dog_source"):
            try:
                await message.channel.send(bot_functions.dog_source())
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif message.content.lower().startswith("!dog"):
            try:
                await message.channel.send(bot_functions.dogs_killed())
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif "dog" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids:
                    await message.channel.send(bot_functions.dogs_killed())
            except:
                await message.channel.send(error_message_did_something_wrong)

        # Tell the bot to dc from vc (just in case)
        elif message.content.lower().startswith("!dc"):
            if len(client.voice_clients) == 1:
                vc = client.voice_clients[0]
                await vc.disconnect()

        # Tell the bot to join the vc
        elif message.content.lower().startswith("!join"):
            if len(vchannel.members) > 0:
                vc = await vchannel.connect()
                vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(random.choice(mp3_files)), volume=1.0))
                while vc.is_playing():
                    await asyncio.sleep(1)
                await asyncio.sleep(0.5)
                await vc.disconnect()

        # Toggle bot's random join function
        elif message.content.lower().startswith("!rjoin"):
            bot_functions.toggle_rjoin_mode()
        
        # Tell the bot to stop
        elif message.content.lower().startswith("!stop"):
            try:
                video_link = "https://youtu.be/P4PgrY33-UA?t=42"
                await message.channel.send(video_link)
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif "stop" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids:
                    video_link = "https://youtu.be/P4PgrY33-UA?t=42"
                    await message.channel.send(video_link)
            except:
                await message.channel.send(error_message_did_something_wrong)

        # Get a user's naughty strike count
        elif "strike" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            mention_ids = [mention.id for mention in message.mentions]
            bot_mention_id = int(client.user.mention[2:-1])
            if bot_mention_id in mention_ids:
                strike_ids = (curr_id for curr_id in mention_ids if curr_id != bot_mention_id)
                for curr_id in strike_ids:
                    naughty_strikes = bot_functions.naughty_strikes_count(curr_id)
                    if naughty_strikes == 1:
                        await message.channel.send(f"<@{curr_id}> has {naughty_strikes} naughty strike.")
                    else:
                        await message.channel.send(f"<@{curr_id}> has {naughty_strikes} naughty strikes.")

        # Naughty Check
        elif message.content.lower().startswith("!naughty"):
            try:
                members = client.get_guild(GUILD_ID).members
                final_members = [member for member in members if member.id not in forbidden_ids]
                chosen_naughtdog_id, chosen_naughtdog_name = bot_functions.naughty_check(final_members)
                final_message = bot_functions.naughty_quote_generator(chosen_naughtdog_name)
                await message.channel.send(final_message)
                await bot_functions.give_naughty_strike_or_warning_or_jail(client.get_channel(CHANNEL_ID), chosen_naughtdog_id, naughty_offender_name=chosen_naughtdog_name)
            except TypeError as e:
                print("all is well:" + str(e))
                pass
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif "naughty" in message.content.lower() and ("anyone" in message.content.lower() or "who" in message.content.lower() or "whos" in message.content.lower() or "who\'s" in message.content.lower() or "who is" in message.content.lower() or "whose" in message.content.lower()) and message.author.id != int(client.user.mention[2:-1]):
            try:
                members = client.get_guild(GUILD_ID).members
                final_members = [member for member in members if member.id not in forbidden_ids]
                chosen_naughtdog_id, chosen_naughtdog_name = bot_functions.naughty_check(final_members)
                final_message = bot_functions.naughty_quote_generator(chosen_naughtdog_name)
                await message.channel.send(final_message)
                await bot_functions.give_naughty_strike_or_warning_or_jail(client.get_channel(CHANNEL_ID), chosen_naughtdog_id, naughty_offender_name=chosen_naughtdog_name)
            except TypeError as e:
                print("all is well:" + str(e))
                pass
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif "naughty" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            mention_ids = [mention.id for mention in message.mentions]
            bot_mention_id = int(client.user.mention[2:-1])
            if bot_mention_id in mention_ids:
                if len(message.mentions) == 1:
                    await message.channel.send(naughty_message_global)
                else:
                    naughty_ids_not_oj = [mention_id for mention_id in mention_ids if mention_id != bot_mention_id]
                    for naughty_id in naughty_ids_not_oj:
                        is_naughty_or_not = bot_functions.is_naughty()
                        naughty_name = message.guild.get_member(naughty_id).name
                        naughty_message = f"**{naughty_name}** {is_naughty_or_not}"
                        await message.channel.send(naughty_message)
                        if naughty_choices.get(is_naughty_or_not, 0) == 1:
                            await bot_functions.give_naughty_strike_or_warning_or_jail(client.get_channel(CHANNEL_ID), naughty_id, naughty_offender_name=naughty_name)                         

        # Guilty check
        elif message.content.lower().startswith("!guilty"):
            await message.channel.send(guilty_message_global)
        elif "guilt" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            mention_ids = [mention.id for mention in message.mentions]
            bot_mention_id = int(client.user.mention[2:-1])
            if bot_mention_id in mention_ids:
                if len(message.mentions) == 1:
                    await message.channel.send(guilty_message_global)
                else:
                    guilty_ids_not_oj = [mention_id for mention_id in mention_ids if mention_id != bot_mention_id]
                    guilty_or_not = [" is guilty.\n", " is not guilty.\n"]
                    guilty_message = ""
                    guilty_message = "".join(("<@" + str(guilty_id) + ">" + random.choice(guilty_or_not)) for guilty_id in guilty_ids_not_oj)
                    await message.channel.send(guilty_message)

        # Get bot's commands
        elif message.content.lower().startswith("!commands") or message.content.lower().startswith("!about"):
            try:
                help_message = bot_functions.print_help_message()
                help_final = ''.join((line + '\n') for line in help_message)
                await message.channel.send(help_final)
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif ("command" in message.content.lower() in message.content.lower() ) and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids:
                    help_message = bot_functions.print_help_message()
                    help_final = ''.join((line + '\n') for line in help_message)
                    await message.channel.send(help_final)
            except:
                await message.channel.send(error_message_did_something_wrong)
        
        # Help command
        elif message.content.lower().startswith("!help"):
            try:
                help_message = f"𝐆𝐨 𝐟𝐮𝐜𝐤 𝐲𝐨𝐮𝐫𝐬𝐞𝐥𝐟 <@{message.author.id}>. \n\nᵗʳʸ \'!ᶜᵒᵐᵐᵃⁿᵈˢ\'"
                await message.channel.send(help_message)
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif "help" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids:
                    help_message = f"𝐆𝐨 𝐟𝐮𝐜𝐤 𝐲𝐨𝐮𝐫𝐬𝐞𝐥𝐟 <@{message.author.id}>. \n\nᵗʳʸ \'!ᶜᵒᵐᵐᵃⁿᵈˢ\'"
                    await message.channel.send(help_message)
            except:
                await message.channel.send(error_message_did_something_wrong)

        # Joke command
        elif message.content.lower().startswith("!joke"):
            try:
                joke_message = f"<@{TARGET_ID}>"
                await message.channel.send(joke_message)
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif " joke" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids and len(mention_ids) == 1:
                    joke_message = f"<@{TARGET_ID}>"
                    await message.channel.send(joke_message)
            except:
                await message.channel.send(error_message_did_something_wrong)

        # Get a bee fact
        elif message.content.lower().startswith("!bee"):
            try:
                bee_fact = bot_functions.bee_facts()
                if bee_fact == special_fact:
                    bee_fact_final = f"{bee_fact} <@{TARGET_ID}>"
                    await message.channel.send(bee_fact_final)
                else: 
                    await message.channel.send(bee_fact)
            except:
                await message.channel.send(error_message_did_something_wrong)

        elif  (" bee" in message.content.lower() or "bee " in message.content.lower() or " bees" in message.content.lower()) and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids and len(mention_ids) == 1:
                    bee_fact = bot_functions.bee_facts()
                    if bee_fact == special_fact:
                        bee_fact_final = f"{bee_fact} <@{TARGET_ID}>"
                        await message.channel.send(bee_fact_final)
                    else:
                        await message.channel.send(bee_fact)
            except:
                await message.channel.send(error_message_did_something_wrong)

        # Get the bot's opinion on current geopolitical politics
        elif  ((" modern" in message.content.lower() or " current" in message.content.lower()) and ("war" in message.content.lower() or "geopolitic" in message.content.lower())) and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids and len(mention_ids) == 1:
                    military_quote = f"Military–industrial complex go brrr"
                    await message.channel.send(military_quote)
                    await message.channel.send(military_spending_link)
            except:
                await message.channel.send(error_message_did_something_wrong)

        # Catch-all
        elif message.content.lower().startswith("!"):
            try:
                await message.channel.send(error_message_bad_command)
            except:
                await message.channel.send(error_message_did_something_wrong)

    client.run(TOKEN)

if __name__ == "__main__":
    main()
