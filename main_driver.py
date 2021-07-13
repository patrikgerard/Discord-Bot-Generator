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

# TOKEN = secret_info.TOKEN
TOKEN = secret_info.OJ_TOKEN
# CHANNEL_ID = secret_info.CHANNEL_ID
CHANNEL_ID = secret_info.CUZ_CHANNEL_ID
error_message_bad_command = "Command doesn't fit. You must acquit!"
error_message_did_something_wrong = "Oh my God, Nicole is killed? Oh my God, she is dead? The errors in your command killed her?"
# GUILD_ID = secret_info.GUILD_ID
GUILD_ID = secret_info.CUZ_GUILD_ID
MARK_ID = secret_info.MARK_ID
SEARS_ID = secret_info.SEARS_ID
PATRICK_ADMIN_ID = secret_info.PATRICK_ADMIN_ID
CARL_ID = secret_info.CARL_ID
guilty_message_global = "I'm absolutely, l00 percent, not guilty."
horny_message_global = "I'm absolutely, l00 percent, not horny."
carl_quote = f"\"Hey Brian I'm done gassing up and heading out to the place at the other end of passbook just crossed Macgomery Road from Holbrook and just keep on going straight towards a house hot like you're going through Montgomery but on hospital road see\""
OJ_QUOTES = [f"The day you take complete responsibility for yourself, the day you stop making any excuses, that's the day you start to the top <@{MARK_ID}>.", f"I don\'t understand what I did wrong except live a life that everyone is jealous of."]
juice_is_loose_link = f"https://cutt.ly/BmTER5b"
nicole_video_link = f"https://youtu.be/IFzL7qSt8Gc"
oj_happy_image_link = f"https://cutt.ly/DmTPSvF"
oj_glove_image_link = f"https://cutt.ly/xmTPBUo"
ford_bronco_links = ["https://static.onecms.io/wp-content/uploads/sites/20/2020/06/16/oj-simpson-bronco.jpg", "https://api.time.com/wp-content/uploads/2017/08/170810_white-ford-bronco.jpg?w=800&quality=85", "https://ca-times.brightspotcdn.com/dims4/default/c554689/2147483647/strip/true/crop/891x501+0+0/resize/840x472!/format/webp/quality/90/?url=https%3A%2F%2Fcalifornia-times-brightspot.s3.amazonaws.com%2F33%2Fd6%2F6dd098d16d9033ae12c724e9c9fd%2Fla-1560722644-ki1iohio46-snap-image"]
calculating_messages = [f"Calculating tier list...", f"Beating my wife...", f"Murdering my wife...", f"Evading the authorities..."]
oj_mad_link = f"https://cdn.vox-cdn.com/thumbor/fmaJOrr2EQNCj4SECstQ4t7xVa8=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/16108952/oj_simpson_38021484_2.jpg"
dick_sucker_fact = f"It has been 4 hours since I successfully sucked my own penis. Things are different now. As soon as mouth-to-penis contact was made I felt a shockwave through my body. I have reason to believe I have super strength and telekinesis now.. 3 hours after contact I noticed a van parked on my street but no one has entered or exited the car since its arrival. I fear for my safety, I'm not sure what sort of power I may have stumbled upon but it's possible that the government has found out. If I don't update this again please send help"
military_spending_link= f"https://media.nationalpriorities.org/uploads/discretionary_spending_pie%2C_2015_enacted.png"
def main():
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        channel = client.get_channel(CHANNEL_ID)
        # await client.get_channel(CHANNEL_ID).send("Hey twitter world, this is yours truly.")
        print(f"{client.user} has connected to Discord.")


    @client.event
    async def on_message(message):
        # Check if the message is from Mark
        if message.author.id == MARK_ID and bot_functions.check_mark_mode() is True:
            await message.channel.send(f"Oh, hi Mark <@{MARK_ID}>\n{secret_info.oh_hi_mark_video}")
        
        # Check if the message is from sears
        if message.author.id == SEARS_ID:
            mocked_message = bot_functions.mock(message.content.lower())
            await message.channel.send(mocked_message)
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
        
        # Sears tweet
        elif message.content.lower().startswith("!sears"):
            try:
                await message.channel.send(bot_functions.grab_sears_tweet())
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif "sears" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids:
                    await message.channel.send(bot_functions.grab_sears_tweet())
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
                    upvote_message = bot_functions.upvote_user(upvoted_id, upvoter_id)
                    await message.channel.send(upvote_message)
                else:
                    pass
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif "upvote" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try:
                upvoter_id = message.author.id
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids and upvoter_id != bot_mention_id:
                    ids_to_upvote = (curr_id for curr_id in mention_ids if curr_id != bot_mention_id)
                    for curr_id in ids_to_upvote:
                        upvote_message = bot_functions.upvote_user(curr_id, upvoter_id)
                        await message.channel.send(upvote_message)
            except:
                await message.channel.send(error_message_did_something_wrong)

        # Downvote a user
        elif message.content.lower().startswith("!downvote"):
            try:
                downvoted_id = message.mentions[0].id
                downvoter_id = message.author.id
                # Check for sears
                if downvoter_id == SEARS_ID:
                    downvote_message = bot_functions.downvote_user(downvoted_id = SEARS_ID)
                    await message.channel.send(downvote_message)
                    await message.channel.send(f"Go fuck yourself <@{SEARS_ID}>.")
                # Downvote and send message
                elif downvoter_id != int(client.user.mention[2:-1]):
                    downvote_message = bot_functions.downvote_user(downvoted_id, downvoter_id)
                    await message.channel.send(downvote_message)
                    bot_functions.set_vote_time_and_user(downvoted_id, downvoter_id)
                else:
                    pass
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif "downvote" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try:
                downvoter_id = message.author.id
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if downvoter_id == SEARS_ID:
                    downvote_message = bot_functions.downvote_user(downvoted_id = SEARS_ID)
                    await message.channel.send(downvote_message)
                    await message.channel.send(f"Go fuck yourself <@{SEARS_ID}>.")
                elif bot_mention_id in mention_ids and downvoter_id != bot_mention_id:
                    ids_to_downvote = (curr_id for curr_id in mention_ids if curr_id != bot_mention_id)
                    for curr_id in ids_to_downvote:
                        downvote_message = bot_functions.downvote_user(curr_id, downvoter_id)                        
                        await message.channel.send(downvote_message)
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif "genesis" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            if message.author.id != PATRICK_ADMIN_ID:
                await message.channel.send(f"You really think you\'re god @<{message.author.id}>?")
            else:
                list_ids = [260246978636677121, 258316428657033216, 328667649573781504, 216781924721623041, 141045034358145024, 198228030684921856, 353223013266882570, 616262200608292895, 439295714535669760, 761022613089943622, 414828586470473735, 674008886482698240, 610235781608374272, 775114232542003241, 769423928460312598, 152183100980461568, 681288576805109761 ] 
                for id_ in list_ids:
                    creation_message = bot_functions.create_user(user_to_create_id = id_)
                    await message.channel.send(" " + creation_message)
                intro_message = bot_functions.print_intro_message()
                intro_final = ''.join((line + '\n') for line in intro_message)
                await message.channel.send(intro_final)
        # Create member
        elif message.content.lower().startswith("!create"):
            try:
                user_to_create_id = message.mentions[0].id
                creator_id = message.author.id

                creation_message = bot_functions.create_user(user_to_create_id, creator_id)
                await message.channel.send(" " + creation_message)
            except:
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
                        creation_message = bot_functions.create_user(curr_id, creator_id)
                        await message.channel.send(" " + creation_message)
            except:
                await message.channel.send(error_message_did_something_wrong)

        # Tier list
        elif message.content.lower().startswith("!tier"):
            try:
                if not bot_functions.tier_list_is_up_to_date():
                    bot_functions.calc_tier_list()
                    await message.channel.send(random.choice(calculating_messages))
                tier_list = bot_functions.print_tier_list()
                tier_list = ''.join((line + '\n') for line in tier_list)
                await message.channel.send(tier_list)
            except:
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

        # Horniest (horny check)
        elif ("horniest" in message.content.lower() or "horndog" in message.content.lower() or "horn dog" in message.content.lower())  and message.author.id != int(client.user.mention[2:-1]):
            try: 
                members = client.get_guild(GUILD_ID).members
                chosen_horndog = bot_functions.horny_check(members)
                final_message = bot_functions.horny_quote_generator(chosen_horndog)
                await message.channel.send(final_message)
                bot_functions.downvote_user(downvoted_id=chosen_horndog)
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

        # Horny Check
        elif message.content.lower().startswith("!horny"):
            members = client.get_guild(GUILD_ID).members
            chosen_horndog = bot_functions.horny_check(members)
            final_message = bot_functions.horny_quote_generator(chosen_horndog)
            await message.channel.send(final_message)
            bot_functions.downvote_user(downvoted_id=chosen_horndog)
        elif "horny" in message.content.lower() and ("anyone" in message.content.lower() or "who" in message.content.lower() or "whos" in message.content.lower() or "who\'s" in message.content.lower() or "who is" in message.content.lower() or "whose" in message.content.lower()):
            members = client.get_guild(GUILD_ID).members
            chosen_horndog = bot_functions.horny_check(members)
            final_message = bot_functions.horny_quote_generator(chosen_horndog)
            await message.channel.send(final_message)
            bot_functions.downvote_user(downvoted_id=chosen_horndog)
        elif "horny" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            mention_ids = [mention.id for mention in message.mentions]
            bot_mention_id = int(client.user.mention[2:-1])
            if bot_mention_id in mention_ids:
                if len(message.mentions) == 1:
                    await message.channel.send(horny_message_global)
                else:
                    horny_ids_not_oj = [mention_id for mention_id in mention_ids if mention_id != bot_mention_id]
                    horny_or_not = [" is horny.\n", " is not horny.\n", " is aggressively horny.\n", " is in heat.\n"]
                    horny_message = ""
                    horny_message = "".join(("<@" + str(horny_id) + ">" + random.choice(horny_or_not)) for horny_id in horny_ids_not_oj)
                    await message.channel.send(horny_message)
                         

    

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
                joke_message = f"<@{SEARS_ID}>"
                await message.channel.send(joke_message)
            except:
                await message.channel.send(error_message_did_something_wrong)
        elif " joke" in message.content.lower() and message.author.id != int(client.user.mention[2:-1]):
            try: 
                mention_ids = [mention.id for mention in message.mentions]
                bot_mention_id = int(client.user.mention[2:-1])
                if bot_mention_id in mention_ids and len(mention_ids) == 1:
                    joke_message = f"<@{SEARS_ID}>"
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
        


    client.run(TOKEN)

if __name__ == "__main__":
    main()