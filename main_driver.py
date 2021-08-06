#!/usr/bin/env python3

import asyncio
import pprint
import discord
from discord.ext import commands
# import pymongo
# from pymongo import MongoClient
import bot_functions
import secret_info
import random
from collections import Counter


### Test Channel Info ###
TOKEN = secret_info.TOKEN
CHANNEL_ID = secret_info.CHANNEL_ID
GUILD_ID = secret_info.GUILD_ID
VOICE_CHANNEL = secret_info.test_voice_channel

### Cousin Channel Info ###
# VOICE_CHANNEL = secret_info.cousin_dbd_voice_channel
# TOKEN = secret_info.OJ_TOKEN
# GUILD_ID = secret_info.CUZ_GUILD_ID
# CHANNEL_ID = secret_info.CUZ_CHANNEL_ID


error_message_bad_command = "Command doesn't fit. You must acquit!"
error_message_did_something_wrong = "Oh my God, Nicole is killed? Oh my God, she is dead? The errors in your command killed her?"

MARK_ID = secret_info.MARK_ID
TARGET_ID = secret_info.TARGET_ID
PATRICK_ADMIN_ID = secret_info.PATRICK_ADMIN_ID
CARL_ID = secret_info.CARL_ID
guilty_message_global = "I'm absolutely, l00 percent, not guilty."
naughty_message_global = "I'm absolutely, l00 percent, not naughty."
carl_quote = f"\"Hey Brian I'm done gassing up and heading out to the place at the other end of passbook just crossed Macgomery Road from Holbrook and just keep on going straight towards a house hot like you're going through Montgomery but on hospital road see\""
OJ_QUOTES = [f"The day you take complete responsibility for yourself, the day you stop making any excuses, that's the day you start to the top <@{MARK_ID}>.", f"I don\'t understand what I did wrong except live a life that everyone is jealous of."]
juice_is_loose_link = f"https://ca-times.brightspotcdn.com/dims4/default/f416c0f/2147483647/strip/true/crop/1201x675+0+0/resize/840x472!/quality/90/?url=https%3A%2F%2Fcalifornia-times-brightspot.s3.amazonaws.com%2Fbf%2Fb9%2Fcdb06ac65770f68c6b83ec7214d8%2Fla-1560697015-h8b49fdy31-snap-image"
nicole_video_link = f"https://youtu.be/IFzL7qSt8Gc"
oj_happy_image_link = f"https://s.abcnews.com/images/US/oj-simpson-las-vegas-2007-gty-mt-170713_16x9_992.jpg"
oj_glove_image_link = f"https://imgix.bustle.com/rehost/2016/9/13/cd95c588-1538-4f20-9ebe-a114d64de09c.jpg?w=800&fit=crop&crop=faces&auto=format%2Ccompress"
ford_bronco_links = ["https://static.onecms.io/wp-content/uploads/sites/20/2020/06/16/oj-simpson-bronco.jpg", "https://api.time.com/wp-content/uploads/2017/08/170810_white-ford-bronco.jpg?w=800&quality=85", "https://ca-times.brightspotcdn.com/dims4/default/c554689/2147483647/strip/true/crop/891x501+0+0/resize/840x472!/format/webp/quality/90/?url=https%3A%2F%2Fcalifornia-times-brightspot.s3.amazonaws.com%2F33%2Fd6%2F6dd098d16d9033ae12c724e9c9fd%2Fla-1560722644-ki1iohio46-snap-image"]
calculating_messages = [f"Calculating tier list...", f"Beating my wife...", f"Murdering my wife...", f"Evading the authorities..."]
oj_mad_link = f"https://cdn.vox-cdn.com/thumbor/fmaJOrr2EQNCj4SECstQ4t7xVa8=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/16108952/oj_simpson_38021484_2.jpg"
dick_sucker_fact = f"It has been 4 hours since I successfully sucked my own penis. Things are different now. As soon as mouth-to-penis contact was made I felt a shockwave through my body. I have reason to believe I have super strength and telekinesis now.. 3 hours after contact I noticed a van parked on my street but no one has entered or exited the car since its arrival. I fear for my safety, I'm not sure what sort of power I may have stumbled upon but it's possible that the government has found out. If I don't update this again please send help"
military_spending_link= f"https://media.nationalpriorities.org/uploads/discretionary_spending_pie%2C_2015_enacted.png"
send_to_naughty_jail_message = f"Go to naughty jail"
bonk_image = f"https://pbs.twimg.com/media/Eqzk4gKXAAU_Y0c?format=jpg&name=large"
naughty_choices = secret_info.naughty_choices
naughty_jail_images = secret_info.naughty_jail_images
naughty_jail_sentence_time = secret_info.naughty_jail_sentence_time
mom_statuses = secret_info.mom_statuses
forbidden_ids = secret_info.forbidden_ids


JOIN_CHANCE = secret_info.join_chance
JOIN_COOLDOWN = secret_info.join_cooldown

mp3_files = secret_info.mp3_files
michael_sounds = secret_info.michael_sounds

# async def free_from_naughty_jail(naughtdog, role, time_to_release):
#     await asyncio.sleep(time_to_release)
#     await naughtdog.remove_roles(role)


def main():
    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True
    client = discord.Client(intents=intents)
    # bot = commands.Bot(command_prefix='$')

    @client.event
    async def on_ready():
        # await client.login(TOKEN);
        channel = client.get_channel(CHANNEL_ID)
        vchannel = client.get_channel(VOICE_CHANNEL)
        #await channel.send("Hey twitter world, this is yours truly on random_changes.")
        print(f"{client.user} has connected to Discord.")
        # ctx = await bot.get_context()
        asyncio.create_task(bot_functions.random_join(vchannel, JOIN_CHANCE, JOIN_COOLDOWN))

        #naughty_jail_role_ = discord.utils.get(channel.guild.roles, name="Captain Naughty")
        #carl = channel.guild.get_member(616262200608292895)
        #await carl.add_roles(naughty_jail_role_)


    @client.event
    async def on_message(message):
        # guild_ = await client.fetch_guild(GUILD_ID)
        # print(guild_)
        # # channel_to_join = discord.utils.get(guild_.channels)
        # channel_to_join = client.get_channel(854399482350272547)
        # print(channel_to_join)
        vchannel = client.get_channel(VOICE_CHANNEL)
        naughty_jail_role = None
        try:
            naughty_jail_role = discord.utils.get(message.guild.roles, name="In Naughty Jail")
        except:
            pass
        if naughty_jail_role != None:
            # Check if the message is from Mark
            if message.author.id == MARK_ID and bot_functions.check_mark_mode() is True:
                await message.channel.send(f"Oh, hi Mark <@{MARK_ID}>\n{secret_info.oh_hi_mark_video}")
            
            # Check if the message is from TARGET
            if message.author.id == TARGET_ID:
                mocked_message = bot_functions.mock(message.content.lower())
                await message.channel.send(mocked_message)
            # Check if the author is in naughty jail
            if naughty_jail_role in message.author.roles:
            # bot_functions.is_in_jail(message.author.id):
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
                    # upvote_message = bot_functions.upvote_user(upvoted_id, upvoter_id)
                    # await message.channel.send(upvote_message)
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
                        # upvote_message = bot_functions.upvote_user(curr_id, upvoter_id)
                        # await message.channel.send(upvote_message)
            except:
                await message.channel.send(error_message_did_something_wrong)
        # elif message.content.lower().startswith("!voice"):
        #     await bot_functions.voice_message(message.channel, ctx, client)
        # Downvote a user
        elif message.content.lower().startswith("!downvote"):
            try:
                downvoted_id = message.mentions[0].id
                downvoter_id = message.author.id
                # Check for target
                # if downvoter_id == target_ID:
                #     downvote_message = bot_functions.downvote_user(downvoted_id = target_ID)
                #     await message.channel.send(downvote_message)
                #     await message.channel.send(f"Go fuck yourself <@{target_ID}>.")
                # Downvote and send message
                if downvoter_id != int(client.user.mention[2:-1]):
                    downvote_message = bot_functions.downvote_user(downvoted_id, downvoter_id, message.mentions[0].name)
                    await message.channel.send(downvote_message)
                    bot_functions.set_vote_time_and_user(downvoted_id, downvoter_id)
                # else:
                #     pass
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif "downvote" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try:
                downvoter_id = message.author.id
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                # if downvoter_id == target_ID:
                #     downvote_message = bot_functions.downvote_user(downvoted_id = target_ID)
                #     await message.channel.send(downvote_message)
                #     await message.channel.send(f"Go fuck yourself <@{target_ID}>.")
                if bot_mention_id in mention_ids and downvoter_id != bot_mention_id:
                    # mentions_map = Counter(mention_ids)
                    # print(mentions_map)
                    # if mentions_map.get(bot_mention_id, 0) == 1:
                    ids_to_downvote = (curr_id for curr_id in mention_ids if curr_id != bot_mention_id)
                    # elif mentions_map.get(bot_mention_id, 0) > 1:
                        # ids_to_downvote = [curr_id for curr_id in mention_ids if curr_id != bot_mention_id]
                        # ids_to_downvote.append(bot_mention_id)
                        # print(ids_to_downvote)
                    for curr_id in ids_to_downvote:
                        user_ = await client.fetch_user(curr_id)
                        downvote_message = bot_functions.downvote_user(curr_id, downvoter_id, name=user_.name)                        
                        await message.channel.send(downvote_message)
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif ("free my man" in message.content.lower()) and message.author.id != int(client.user.mention[2:-1]):
            if message.author.id != PATRICK_ADMIN_ID:
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

        # Naughty warning
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
        # naughty_strikes
        elif message.content.lower().startswith("!strike"):
            naughty_strikes = bot_functions.naughty_strikes_count(message.mentions[0].id)
            if naughty_strikes == 1:
                await message.channel.send(f"<@{message.mentions[0].id}> has {naughty_strikes} naughty strike.")
            else:
                await message.channel.send(f"<@{message.mentions[0].id}> has {naughty_strikes} naughty strikes.")

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
        

        # naughty permit
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
        
        # Naughty jail
        elif message.content.lower().startswith("!jail"):
            await bot_functions.print_jail(message.channel)
        elif ("jail" in message.content.lower() and ("whos" in message.content.lower() or "who's" in message.content.lower() or "whose" in message.content.lower() or "who" in message.content.lower())) and message.author.id != int(client.user.mention[2:-1]):
            await bot_functions.print_jail(message.channel)

        # elif "genesis" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
        #     if message.author.id != PATRICK_ADMIN_ID:
        #         await message.channel.send(f"You really think you\'re god @<{message.author.id}>?")
        #     else:
        #         list_ids = [260246978636677121, 258316428657033216, 328667649573781504, 216781924721623041, 141045034358145024, 198228030684921856, 353223013266882570, 616262200608292895, 439295714535669760, 761022613089943622, 414828586470473735, 674008886482698240, 610235781608374272, 775114232542003241, 769423928460312598, 152183100980461568, 681288576805109761 ] 
        #         for id_ in list_ids:
        #             creation_message = bot_functions.create_user(user_to_create_id = id_)
        #             await message.channel.send(" " + creation_message)
        #         intro_message = bot_functions.print_intro_message()
        #         intro_final = ''.join((line + '\n') for line in intro_message)
        #         await message.channel.send(intro_final)
        # Create member
        elif message.content.lower().startswith("!create"):
            try:
                user_to_create_id = message.mentions[0].id
                creator_id = message.author.id
                
                creation_message = bot_functions.create_user(user_to_create_id, creator_id, name=message.mentions[0].name)
                await message.channel.send(" " + creation_message)
            except Exception as e:
                print(e)
                # user_to_create = message.content()[len("!create"):].strip()
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
        # elif message.content.lower().startswith("!print_ids"):
        #     guild_ = await client.fetch_guild(secret_info.CUZ_GUILD_ID)
        #     for member in guild_.members:
        #         await message.channel.send(f"<@{member.id}>: {member.id}")
        # Tier list
        elif message.content.lower().startswith("!tier"):
            try:
                if not bot_functions.tier_list_is_up_to_date():
                    bot_functions.calc_tier_list()
                    await message.channel.send(random.choice(calculating_messages))
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
                        await message.channel.send(random.choice(calculating_messages))
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
        # mom status
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
                
        # Dogs killed by cops
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

        elif message.content.lower().startswith("!dc"):
            if len(client.voice_clients) == 1:
                vc = client.voice_clients[0]
                await vc.disconnect()


        elif message.content.lower().startswith("!michael"):
            if len(vchannel.members) > 0:
                vc = await vchannel.connect()
                vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(random.choice(michael_sounds)), volume=1.0))
                while vc.is_playing():
                    await asyncio.sleep(1)
                await asyncio.sleep(0.5)
                await vc.disconnect()

        elif message.content.lower().startswith("!join"):
            if len(vchannel.members) > 0:
                vc = await vchannel.connect()
                vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(random.choice(mp3_files)), volume=1.0))
                while vc.is_playing():
                    await asyncio.sleep(1)
                await asyncio.sleep(0.5)
                await vc.disconnect()

        elif message.content.lower().startswith("!rjoin"):
            bot_functions.toggle_rjoin_mode()

        elif message.content.lower().startswith("!lick the meat"):
            lick_the_meat = "mp3_files/lick_the_meat.mp3"
            if len(vchannel.members) > 0:
                vc = await vchannel.connect()
                vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(lick_the_meat)))
                while vc.is_playing():
                    await asyncio.sleep(1)
                await asyncio.sleep(0.5)
                await vc.disconnect()


        # Carl
        elif message.content.lower().startswith("!carl"):
            try:
                await message.channel.send(carl_quote)
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif "carl" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids:
                    await message.channel.send(carl_quote)
            except:
                await message.channel.send(error_message_did_something_wrong)
        
        # Stop
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
        # elif "guilt" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
        #     mention_ids = [mention.id for mention in message.mentions]
        #     bot_mention_id = int(client.user.mention[2:-1])
        #     if bot_mention_id in mention_ids:
        #         await message.channel.send(guilty_message_global)

        elif message.content.lower().startswith("!car"):
            await message.channel.send("Check out my ride!")
            await message.channel.send(random.choice(ford_bronco_links))
        elif ("car" in message.content.lower()  or "drive" in message.content.lower() or "driving" in message.content.lower()) and message.author.id != int(client.user.mention[2:-1]):
            mention_ids = [mention.id for mention in message.mentions]
            bot_mention_id = int(client.user.mention[2:-1])
            if bot_mention_id in mention_ids:
                await message.channel.send("Check out my ride!")
                await message.channel.send(random.choice(ford_bronco_links))
                    

        # Help messages
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

        # Annoy Mark Mode
        elif message.content.lower().startswith("!mark"):
            if message.author.id != PATRICK_ADMIN_ID:
                await message.channel.send("You really think you can stop me?")
            else:
                try:
                    bot_functions.toggle_mark_mode()
                    if bot_functions.check_mark_mode() is True:
                        loose_message = f"𝐓𝐇𝐄 𝐉𝐔𝐈𝐂𝐄 𝐈𝐒 𝐋𝐎𝐎𝐒𝐄 𝐎𝐍𝐂𝐄 𝐀𝐆𝐀𝐈𝐍 <@{MARK_ID}>"
                        await message.channel.send(loose_message)
                        await message.channel.send(juice_is_loose_link)
                    else:
                        await message.channel.send(random.choice(OJ_QUOTES))
                except:
                    await message.channel.send(error_message_did_something_wrong)
        elif "mark" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            if message.author.id != PATRICK_ADMIN_ID:
                await message.channel.send("You really think you can stop me?")
            else:
                try:
                    mention_ids = [mention.id for mention in message.mentions]
                    bot_mention_id = int(client.user.mention[2:-1])
                    if bot_mention_id in mention_ids:
                        bot_functions.toggle_mark_mode()
                        if bot_functions.check_mark_mode() is True:
                            loose_message = f"𝐓𝐇𝐄 𝐉𝐔𝐈𝐂𝐄 𝐈𝐒 𝐋𝐎𝐎𝐒𝐄 𝐎𝐍𝐂𝐄 𝐀𝐆𝐀𝐈𝐍 <@{MARK_ID}>"
                            await message.channel.send(loose_message)
                            await message.channel.send(juice_is_loose_link)
                        else:
                            await message.channel.send(random.choice(OJ_QUOTES))
                except:
                    await message.channel.send(error_message_did_something_wrong)

        # Someone says they hate OJ
        elif " hate" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids and len(mention_ids) == 1:
                    hate_message = f"Real tough guy <@{message.author.id}>? Know what I\'m capable of?"
                    await message.channel.send(hate_message)
                    await message.channel.send(nicole_video_link)
            except:
                await message.channel.send(error_message_did_something_wrong)

        # Someone says they love OJ
        elif message.content.lower().startswith("!glove"):
            try:
                glove_message = f"The glove doesn\'t fit. You must acquit!\n"
                await message.channel.send(glove_message)
                await message.channel.send(oj_glove_image_link)
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif " glove" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids and len(mention_ids) == 1:
                    glove_message = f"The glove doesn\'t fit. You must acquit!\n"
                    await message.channel.send(glove_message)
                    await message.channel.send(oj_glove_image_link)
            except:
                await message.channel.send(error_message_did_something_wrong)
            
        # Someone says they love OJ
        elif " love" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids and len(mention_ids) == 1:
                    love_message = f"{oj_happy_image_link}"
                    await message.channel.send(love_message)
            except:
                await message.channel.send(error_message_did_something_wrong)
        
        # Fuck
        elif "fuck" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids and len(mention_ids) == 1:
                    fuck_message = f"Oh I\'ll fuck you alright, <@{message.author.id}>"
                    await message.channel.send(fuck_message)
            except:
                await message.channel.send(error_message_did_something_wrong)

                # Fuck
        elif "nicole" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids and len(mention_ids) == 1:
                    nicole_message = f"I\'ll send you where I sent nicole, <@{message.author.id}>"
                    await message.channel.send(nicole_message)
                    await message.channel.send(oj_mad_link)
            except:
                await message.channel.send(error_message_did_something_wrong)
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

        elif message.content.lower().startswith("!bee"):
            try:
                bee_fact = bot_functions.bee_facts()
                if bee_fact == dick_sucker_fact:
                    bee_fact_final = f"{bee_fact} <@{CARL_ID}>"
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
                    if bee_fact == dick_sucker_fact:
                        bee_fact_final = f"{bee_fact} <@{CARL_ID}>"
                        await message.channel.send(bee_fact_final)
                    else:
                        await message.channel.send(bee_fact)
            except:
                await message.channel.send(error_message_did_something_wrong)

        elif  ((" modern" in message.content.lower() or " current" in message.content.lower()) and ("war" in message.content.lower() or "geopolitic" in message.content.lower())) and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids and len(mention_ids) == 1:
                    military_quote = f"Military–industrial complex go brrr"
                    # if bee_fact == dick_sucker_fact:
                    #     await message.channel.send(bee_fact, deleter_after=10)
                    # else: 
                    await message.channel.send(military_quote)
                    await message.channel.send(military_spending_link)
            except:
                await message.channel.send(error_message_did_something_wrong)



        elif message.content.lower().startswith("!"):
            try:
                await message.channel.send(error_message_bad_command)
            except:
                await message.channel.send(error_message_did_something_wrong)
        

    # @bot.command(name='voice')
    # async def voice_message(ctx):
    #     print("got here")
    #     await ctx.send("hello")

    #     user = ctx.message.user
    #     voice_channel = user.voice.voice_channel
    #     channel_ = None

    #     if voice_channel != None:
    #         channel_ = voice_channel.name
    #         await client.say('User is in channel: '+ channel_)
    #         vc = await client.join_voice_channel(voice_channel)
    #         player = vc.create_ffmpeg_player('oj.mp3', after=lambda: print('done'))
    #         player.start()
    #         while not player.is_done():
    #             await asyncio.sleep(1)
    #         # disconnect after the player has finished
    #         player.stop()
    #         await vc.disconnect()

    client.run(TOKEN)

if __name__ == "__main__":
    main()
