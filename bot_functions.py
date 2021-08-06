#!/usr/bin/env python3

# Imports
import asyncio
import tweepy
import pprint
from datetime import datetime, date
import pytz
from random import randrange
import pymongo
from pymongo import MongoClient
from statistics import stdev
import secret_info
import csv
import random
import time
import discord
import math

# Tweepy api setup
TWEEPY_CONSUMER_KEY = secret_info.TWEEPY_CONSUMER_KEY
TWEEPY_CONSUMER_SECRET_KEY = secret_info.TWEEPY_CONSUMER_SECRET_KEY
TWEEPY_ACCESS_TOKEN = secret_info.TWEEPY_ACCESS_TOKEN
TWEEPY_ACCESS_TOKEN_SECRET = secret_info.TWEEPY_ACCESS_TOKEN_SECRET 

# Targeted twitter username
target_TWITTER_USERNAME = secret_info.TARGET_TWITTER_USERNAME
target_DISCORD_USER_ID = secret_info.TARGET_DISCORD_USER_ID

# Mongo api setup
MONGO_CONNECTION_URL = secret_info.MONGO_CONNECTION_URL
MONGO_DB = secret_info.MONGO_DB
MONGO_COLLECTION_USERS = secret_info.MONGO_COLLECTION_USERS
MONGO_COLLECTION_TIER_LIST = secret_info.MONGO_COLLECTION_TIER_LIST


# Information file
INFORMATION_FILE_NAME ="info/information.txt"

# Used for time calculations
epoch = datetime(1970,1,1)

# Voting refresh time 
vote_refresh_time = 180 # 3 minutes

# Help, update, intro, and bee facts documents
help_doc = "info/help.txt"
update_doc = "info/update_notes.txt"
intro_doc = "info/introduction.txt"
bee_facts_txt = "info/bee_facts.txt"

# Naughty jail oonfig
allowed_naughty_permit_time = secret_info.allowed_naughty_permit_time # one hour
naughty_jail_sentence_time = secret_info.naughty_jail_sentence_time # one hour
naughty_choices = secret_info.naughty_choices
naughty_jail_messages = secret_info.naughty_jail_messages
bonk_image = secret_info.bonk_image
naughty_jail_role = secret_info.naughty_jail_role
naughty_check_cooldown = secret_info.naughty_check_cooldown
permit_request_cooldown = secret_info.permit_request_cooldown
permit_request_chance = secret_info.permit_request_chance
naughty_strike_cooldown = secret_info.naughty_strike_cooldown

# Potential status of someone's dearest
mom_statuses = secret_info.mom_statuses

# Toggle for the bot to join the voice channel and mp3 files
r_join_file = secret_info.r_join_file
mp3_files = secret_info.mp3_files

# Source for dog fact
DOG_SOURCE = "https://www.criminallegalnews.org/news/2018/jun/16/doj-police-shooting-family-dogs-has-become-epidemic/"

# Mocks message
def mock(message):
    index = True
    mocked_message = ""
    for letter in message:
        if index:
            mocked_message += letter.upper()
        else:
            mocked_message += letter.lower()
        if letter != ' ':
            index  = not index
    return mocked_message


# Strips only the leading whitespace
def strip_command(message, command):
    return message[len(command):].lstrip()


################# Tweets #################

# grabs target's timeline
def retrieve_timeline( api, user ):
    return api.user_timeline(screen_name = user, include_rts = True)

# grabs a target tweet
def grab_target_tweet():

    # create authenticator
    auth = tweepy.OAuthHandler(TWEEPY_CONSUMER_KEY, TWEEPY_CONSUMER_SECRET_KEY)
    auth.set_access_token(TWEEPY_ACCESS_TOKEN, TWEEPY_ACCESS_TOKEN_SECRET)

    # create api object
    api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

    # grab a tweet
    target_tweets = retrieve_timeline(api, target_TWITTER_USERNAME)
    number_of_tweets = len(target_tweets)
    tweet = target_tweets[randrange(number_of_tweets)]
    id = tweet._json['id']

    # Different text for rt vs tweet
    if "RT" in tweet._json['text']:
        text = api.get_status(id, tweet_mode = "extended").retweeted_status.full_text
        return f"This dickhead {target_DISCORD_USER_ID} retweeted \"{text}\""
    else:
        text = api.get_status(id, tweet_mode = "extended")
        return f"{text.full_text}"

################# Tweets #################


################# Tier List #################

def create_user(user_to_create_id, creator_id=None, name=""):

    # Grab the cluster, db, and collection
    cluster = MongoClient(MONGO_CONNECTION_URL)
    db = cluster[MONGO_DB]
    collection = db[MONGO_COLLECTION_USERS]
    print("got past collection")

    # Check if the user is alreayd in the rankings
    if collection.count_documents({"_id": user_to_create_id}) > 0:
        if creator_id is None:
            return f"<@{user_to_create_id}> is already in rankings."
        else:
            down_vote_message = downvote_user(downvoted_id=creator_id)
            return f"<@{user_to_create_id}> is already in  rankings. Minus one point for you <@{creator_id}>."
    current_time = int(current_time_in_seconds())

    # Create the post to insert into the rankings
    post = {"_id": user_to_create_id,
     "points": 0,
     "tier": "B",
     "most_recent_vote_time": 0,
     "last_user_voted_on": user_to_create_id,
     "is_naughty_jailer": 0,
     "has_naughty_permit": 0,
     "naughty_permit_start_time": 0,
     "naughty_warnings": 0,
     "naughty_strikes": 0,
     "in_naughty_jail": 0,
     "naughty_jail_sentence_start_time": 0,
     "last_naughty_check": 0,
     "last_permit_request": 0,
     "user_name": name
    }
    try:
        collection.insert_one(post)
    except Exception as e:
        print(e)
    set_update_needed()

    return f"<@{user_to_create_id}> added to cousin rankings."

# Upvotes a user
async def upvote_user(channel, upvoted_id, upvoter_id=None, name=""):

    # Edge cases
    if upvoted_id == None:
        await channel.send(f"Who do you want me to upvote?")
    if upvoted_id == upvoter_id:
        await channel.send(f"Go fuck yourself <@{upvoter_id}>.")
    else:
        # Get the cluster, db, and collection
        cluster = MongoClient(MONGO_CONNECTION_URL)
        db = cluster[MONGO_DB]
        collection = db[MONGO_COLLECTION_USERS]

        # Check that the user is in the database
        if collection.count_documents({"_id": upvoted_id}) != 1:
            user_created_message = create_user(user_to_create_id=upvoted_id, name=name)
            upvote_message = upvote_user(channel, upvoted_id = upvoted_id)
            await channel.send(f"<@{upvoted_id}> was created and upvoted.")
        
        if upvoter_id != None:

            # Get the time since last vote
            last_vote = collection.find_one({'_id':upvoter_id})['most_recent_vote_time']
            current_time = current_time_in_seconds()
            time_since_last_vote = get_time_since_last_vote(current_time, last_vote)

            # Get the last user voted on
            last_user_voted_on = collection.find_one({'_id':upvoter_id})['last_user_voted_on']

            # see if the user can vote
            voting_right = can_user_vote(last_user_voted_on, upvoted_id, time_since_last_vote)
            if voting_right != True:
                await channel.send(f"Call me a Republican, because I\'m taking away your right to vote <@{upvoter_id}>.\n[Voting on the same person too quickly]")
            else:

                # Add a point and update the database
                points = collection.find_one({'_id':upvoted_id})['points']
                points += 1
                # Add point to tier list date_checker
                set_update_needed()
                collection.update_one({"_id":upvoted_id}, {"$set": {"points": points}}) 
                set_vote_time_and_user(upvoted_id, upvoter_id)
                # Notification
                await channel.send(f"<@{upvoted_id}> was upvoted.")
        else:
            # Add a point and update the database
            points = collection.find_one({'_id':upvoted_id})['points']
            points += 1
            # add point to tier list date_checker
            set_update_needed()
            collection.update_one({"_id":upvoted_id}, {"$set": {"points": points}}) 
            set_vote_time_and_user(upvoted_id, upvoter_id)
            # Notification
            await channel.send(f"<@{upvoted_id}> was upvoted.")


# Downvotes a User
def downvote_user(downvoted_id, downvoter_id=None, name=" "):
    
    # Edge cases
    if downvoted_id == None:
        return f"Who do you want me to downvote?"
    if downvoted_id == downvoter_id:
        return f"Go love yourself <@{downvoter_id}>."
    else:
        # Get the cluster, db, and collection
        cluster = MongoClient(MONGO_CONNECTION_URL)
        db = cluster[MONGO_DB]
        collection = db[MONGO_COLLECTION_USERS]

        # Check if the user exists
        if collection.count_documents({"_id": downvoted_id}) != 1:
            user_created_message = create_user(user_to_create_id=downvoted_id, name=name)
            downvote_message = downvote_user(downvoted_id = downvoted_id)
            return f"<@{downvoted_id}> was created and downvoted"
        
        # Check if the user can vote
        if downvoter_id != None:

            # Get the time since last vote
            last_vote = collection.find_one({'_id':downvoter_id})['most_recent_vote_time']
            current_time = current_time_in_seconds()
            time_since_last_vote = get_time_since_last_vote(current_time, last_vote)

            # Get the last user voted on
            last_user_voted_on = collection.find_one({'_id':downvoter_id})['last_user_voted_on']

            # see if they can vote
            voting_right = can_user_vote(last_user_voted_on, downvoted_id, time_since_last_vote)
            if voting_right != True:
                return f"Call me a Republican, because I\'m taking away your right to vote <@{downvoter_id}>.\n[Voting on the same person too quickly]"
        
        # Add a point and update the database
        points = collection.find_one({'_id':downvoted_id})['points']
        points -= 1
        # add point to tier list date_checker
        set_update_needed()
        collection.update_one({"_id":downvoted_id}, {"$set": {"points": points}})
        set_vote_time_and_user(downvoted_id, downvoter_id)
        # Notification
        return f"<@{downvoted_id}> was downvoted"

# Calculate the tier list
def calc_tier_list():

    # Get the cluster, db, and collection
    cluster = MongoClient(MONGO_CONNECTION_URL)
    db = cluster[MONGO_DB]
    cousins_collection = db[MONGO_COLLECTION_USERS]

    # Init point values
    total_points = 0
    total_members = 0
    stdev_collector = [0]

    # Get point values
    for member in list(cousins_collection.find({})):
        total_members += 1
        stdev_collector.append(member["points"])
        total_points += member["points"]

    average_points = total_points / total_members
    std_dev_points = stdev(stdev_collector)
    # Map users to tier list and set the tier list as being up-to-date
    map_to_tier_list(total_points, average_points, std_dev_points)
    set_tier_up_to_date()

# Map to the tier list
def map_to_tier_list(total_points, average_points, std_dev_points):
    # Arbitrary mappings -- can be changed
    tier_mapping =    { 
        'S' : int(math.ceil(average_points + (std_dev_points))), # ge
        'A': round(average_points + (std_dev_points*0.4)), # ge
        'B': round(average_points), # ge
        'C': round(average_points - (std_dev_points*0.2)), # le 
        'D': round(average_points - (std_dev_points*0.4)), # le
        'Piss Dungeon': round(average_points - (std_dev_points)), # le
        'State of Florida': round(average_points - (std_dev_points*1.4)) # le
    }

    # Get the cluster, db, and collection
    cluster = MongoClient(MONGO_CONNECTION_URL)
    db = cluster[MONGO_DB]
    collection_members = db[MONGO_COLLECTION_USERS]
    collection_tier_list = db[MONGO_COLLECTION_TIER_LIST]

    #  Go through each tier (to map)
    for tier in tier_mapping:
        collection_tier_list.update_one({"_id":tier}, {"$set":{"members": []}})

    # Map each user to their respective tier list
    for member in list(collection_members.find({})):
        tier = ""
        if member["points"] >= tier_mapping['S']:
            tier = "S"
        elif member["points"] >= tier_mapping['A']:
            tier = "A"
        elif member["points"] >= tier_mapping['C']:
            tier = "B"
        elif member["points"] >= tier_mapping['D']:
            tier = "C"
        elif member["points"] >= tier_mapping['Piss Dungeon']:
            tier = "D"
        elif member["points"] >= tier_mapping['State of Florida']:
            tier = "Piss Dungeon"
        else: 
            tier = "State of Florida"

        # Update tier list and user
        collection_tier_list.update_one({"_id":tier}, {"$push":{"members": member['user_name']}})
        collection_members.update_one({"_id":member["_id"]}, {"$set": {"tier": tier}})


# Print tier list
def print_tier_list():
    # Grab cluster, db, and collection
    cluster = MongoClient(MONGO_CONNECTION_URL)
    db = cluster[MONGO_DB]
    collection_tier_list = db[MONGO_COLLECTION_TIER_LIST]

    # Loop through tier list
    for tier in collection_tier_list.find():
        yield f"__{tier['_id']} Tier:__"
        for member in tier['members']:
            yield f" \t**{member}** "
    pass

# Set tier list as up-to-date
def set_tier_up_to_date():
    # Open tier list file
    reader = csv.reader(open(INFORMATION_FILE_NAME))
    lines = list(reader)
    lines[1][0] = 0
    # Write to tier list file
    writer = csv.writer(open(INFORMATION_FILE_NAME, "w"))
    writer.writerows(lines)

def tier_list_is_up_to_date():
    # Open tier list file
    with open (INFORMATION_FILE_NAME, 'r') as csv_file:
        line_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_file:
            if line_count == 0:
                line_count += 1
            else:
                # Return that the tier list does not need an update (returns false if 1)
                return int(row[0]) == 0

# Set that an update is needed
def set_update_needed():
    # Open tier list file
    reader = csv.reader(open(INFORMATION_FILE_NAME))
    lines = list(reader)
    lines[1][0] = 1

    # Write to tier list file
    writer = csv.writer(open(INFORMATION_FILE_NAME, "w"))
    writer.writerows(lines)

# Check if a user can vote
def can_user_vote(last_user_voted_on, current_user_voted_on, time_since_last_vote):
    # If the user did not just vote on this other user
    if last_user_voted_on != current_user_voted_on:
        return True
    # Check if the user did just vote on the other user, if they voted long enough ago that the refresh time is past
    if (last_user_voted_on == current_user_voted_on) and  (time_since_last_vote <= vote_refresh_time):
        return False
    else:
        return True 

# Set vote time
def set_vote_time_and_user(voted_id, voter_id):
    # Get current time
    current_time = int(current_time_in_seconds())
    # Get cluster, db, and collection
    cluster = MongoClient(MONGO_CONNECTION_URL)
    db = cluster[MONGO_DB]
    collection = db[MONGO_COLLECTION_USERS]
    # Set vote time
    if voter_id != None:
        collection.update_one({"_id":voter_id}, {"$set": {"last_user_voted_on":voted_id}})
        collection.update_one({"_id":voter_id}, {"$set": {"most_recent_vote_time": current_time}})
        vote_time = collection.find_one({'_id':voted_id})['most_recent_vote_time']


################# Tier List #################




################# Dog Fact #################

# Print the source for dog fact
def dog_source():
    return f"{DOG_SOURCE}"

def dogs_killed():
    # Get the time since the start of the year
    current_year = datetime(datetime.today().year, 1, 1)
    current_date = datetime.today()
    seconds_since_year_start = (current_date - current_year).total_seconds() 
    # Calculate the dogs killed since that time
    dogs_killed_since_year_start = round(seconds_since_year_start/3600)

    # Return dog fact
    dog_quotes = ["Ruff world!", "Talk about puppy love!", "Man's best friend! Pig\'s worst enemy!"]
    return f"There have been approximately {dogs_killed_since_year_start} dogs killed by cops this year. " + random.choice(dog_quotes) + "\n\nType \'!dogs_source\' for source."

################# Dog Fact #################



################# Misc Functions #################

def print_help_message():
    lines = open(help_doc, encoding='utf-8').read().splitlines()
    for line in lines:
        yield line

def print_intro_message():
    lines = open(intro_doc, encoding='utf-8').read().splitlines()
    for line in lines:
        yield line

def current_time_in_seconds():
    current_time = datetime.today()
    time =  (current_time - epoch).total_seconds()
    return time

def get_time_since_last_vote(current_time, last_vote):
    time = current_time - last_vote
    return int(time)

# Returns difference in time
def get_time_since_last(current_time, last_time):
    time = current_time - last_time
    return int(time)

# Prints update notes
async def print_update_notes(channel):
    lines = open(update_doc, encoding='utf-8').read().splitlines()
    update_message = ""
    for line in lines:
        update_message += line + "\n"
    await channel.send(update_message)

################# Misc Functions #################


################# Bee Facts #################

def bee_facts():
    bee_facts = []
    lines = open(bee_facts_txt, encoding='utf-8').read().splitlines()
    for line in lines:
        bee_facts.append(line)
    return random.choice(bee_facts)

################# Bee Facts #################



################# Naughty Checks #################

# Check who is the most naughty
def naughty_check(members):
    # Get a random member
    random_member = random.choice(members)
    member_name = random_member.name
    member_id = random_member.id
    return member_id, member_name

# Generate a naughty quote
def naughty_quote_generator(chosen_naughtdog):
    # Get the naughtdog
    choice =  chosen_naughtdog
    return "Mirror, mirror on the wall — **" + choice + "** is the naughtiest of them all."


# Naughty warning config
def has_naughty_warning(naughty_offender):
    # Get cluster, db, and collection
    cluster = MongoClient(MONGO_CONNECTION_URL)
    db = cluster[MONGO_DB]
    collection = db[MONGO_COLLECTION_USERS]
    # Grab the naughty warnings
    naughty_warning = collection.find_one({'_id':naughty_offender})['naughty_warnings']
    return naughty_warning == 1

def give_naughty_warning(naughty_offender, collection):
    # Give naughty warning
    collection.update_one({"_id":naughty_offender}, {"$set": {"naughty_warnings": 1}}) 

def take_naughty_warning(naughty_offender, collection):
    # Take away nuaghty warning
    collection.update_one({"_id":naughty_offender}, {"$set": {"naughty_warnings": 0}})

# naughty strikes config
def naughty_strikes_count(naughty_offender):
    # Grab cluster, db, and collection
    cluster = MongoClient(MONGO_CONNECTION_URL)
    db = cluster[MONGO_DB]
    collection = db[MONGO_COLLECTION_USERS]
    # Grab naughty strikes
    return collection.find_one({'_id':naughty_offender})['naughty_strikes']

def give_naughty_strike(naughty_offender, collection):
    # Add one naughty strike
    naughty_strikes = collection.find_one({'_id':naughty_offender})['naughty_strikes']
    collection.update_one({"_id":naughty_offender}, {"$set": {"naughty_strikes": naughty_strikes + 1}})
    asyncio.create_task(remove_naughty_strike_async(naughty_offender, 1, collection, naughty_strike_cooldown))

def take_naughty_strikes(naughty_offender, strikes_to_take, collection):
    # Take one naughty strike
    naughty_strikes = collection.find_one({'_id':naughty_offender})['naughty_strikes']
    collection.update_one({"_id":naughty_offender}, {"$set": {"naughty_strikes": naughty_strikes - strikes_to_take}})

# naughty permit config
def has_valid_naughty_permit(naughty_offender):
    # Grab cluster, db, and collection
    cluster = MongoClient(MONGO_CONNECTION_URL)
    db = cluster[MONGO_DB]
    collection = db[MONGO_COLLECTION_USERS]

    # Check if the naughty permit is valid
    naughty_permit = collection.find_one({'_id':naughty_offender})['has_naughty_permit']
    naughty_permit_time = collection.find_one({'_id':naughty_offender})['naughty_permit_start_time']
    current_time = current_time_in_seconds()
    time_since_permit_given = get_time_since_last(current_time, naughty_permit_time)
    # Return naughty permit status
    return naughty_permit == 1 and time_since_permit_given <= allowed_naughty_permit_time

# Take naughty permit
def take_naughty_permit(naughty_offender):
    # Grab cluster, db, and collection
    cluster = MongoClient(MONGO_CONNECTION_URL)
    db = cluster[MONGO_DB]
    collection = db[MONGO_COLLECTION_USERS]
    # Reset naughty permit
    collection.update_one({"_id":naughty_offender}, {"$set": {"has_naughty_permit": 0}})

# naughty jail config
def send_to_naughty_jail(naughty_offender, collection):
    # Grab current time
    current_time = int(current_time_in_seconds())
    # Send to naughty jail and reset strikes+warnings
    collection.update_one({"_id":naughty_offender}, {"$set": {"in_naughty_jail": 1}})
    collection.update_one({"_id":naughty_offender}, {"$set": {"naughty_jail_sentence_start_time": current_time}})
    take_naughty_strikes(naughty_offender, 2, collection)
    take_naughty_warning(naughty_offender, collection)

# Check if a user is in jail (unnecessary if you use the discrod roles)
def is_in_jail(naughty_offender):
    # Grab current time
    current_time = int(current_time_in_seconds())
    # Grab cluster, db, and collection
    cluster = MongoClient(MONGO_CONNECTION_URL)
    db = cluster[MONGO_DB]
    collection = db[MONGO_COLLECTION_USERS]

    # Check if their naughty sentence is over
    in_naughty_jail = collection.find_one({'_id':naughty_offender})['in_naughty_jail']
    naughty_jail_time = collection.find_one({'_id':naughty_offender})['naughty_jail_sentence_start_time']
    current_time = current_time_in_seconds()
    time_in_jail = get_time_since_last(current_time, naughty_jail_time)
    return in_naughty_jail == 1 and time_in_jail <= naughty_jail_sentence_time

# Free user from naughty jail
async def free_from_jail_immediate(channel, naughty_offender):
    # Grab cluster, db, and collection
    cluster = MongoClient(MONGO_CONNECTION_URL)
    db = cluster[MONGO_DB]
    collection = db[MONGO_COLLECTION_USERS]

    # Reset naughty jail status
    collection.update_one({"_id":naughty_offender}, {"$set": {"in_naughty_jail": 0}})
    naughty_jail_role_ = discord.utils.get(channel.guild.roles, name="In naughty Jail")
    # Remove naughtdog status
    naughtdog_member = channel.guild.get_member(naughty_offender)
    await naughtdog_member.remove_roles(naughty_jail_role_)
    await channel.send(f"Oh god hide the children <@{naughty_offender}> is out of naughty jail.")

# Give a strike, warning, or send the user to naughty jail
async def give_naughty_strike_or_warning_or_jail(channel, naughty_offender, naughty_offender_name):
    # Grab cluster, db, and collection
    cluster = MongoClient(MONGO_CONNECTION_URL)
    db = cluster[MONGO_DB]
    collection = db[MONGO_COLLECTION_USERS]

    #  Check cool down
    if naughty_cooldown_check(naughty_offender) is True:
        await channel.send(f"**{naughty_offender_name}** was given temporary naughty amnesty. Quit asking and maybe <@{naughty_offender}> will calm down.")
    # If the offender is in naughty jail
    elif is_in_jail(naughty_offender):
        await channel.send(f"**{naughty_offender_name}** is already in naughty jail. Give **{naughty_offender_name}** some alone-time for self-reflection")
        set_naughty_cool_down(channel, naughty_offender)
    # Otherwise, if the offender has a permit
    elif has_valid_naughty_permit(naughty_offender):
        await channel.send(f"Not to worry. **{naughty_offender_name}** has a permit to be this naughty.")
        set_naughty_cool_down(channel, naughty_offender)
    # If the offender has a naughty warning
    elif has_naughty_warning(naughty_offender) == False:
        give_naughty_warning(naughty_offender, collection)
        await channel.send(f"**{naughty_offender_name}** was given a warning for execessive naughtiness.")
        set_naughty_cool_down(channel, naughty_offender)
    elif naughty_strikes_count(naughty_offender) < 2:
        give_naughty_strike(naughty_offender, collection)
        await channel.send(f"**{naughty_offender_name}** was given a naughty strike.")
        set_naughty_cool_down(channel, naughty_offender)
    # If the naughty offender already has 2 naughty strikes, send them to jail upon the third
    elif naughty_strikes_count(naughty_offender) >= 2:
        send_to_naughty_jail(naughty_offender, collection)
        await channel.send(f"Go to naughty jail **{naughty_offender_name}**.")
        naughty_jail_role_ = discord.utils.get(channel.guild.roles, name="In naughty Jail")
        naughtdog_member = channel.guild.get_member(naughty_offender)
        await naughtdog_member.add_roles(naughty_jail_role_)
        await channel.send(bonk_image)
        asyncio.create_task(free_from_naughty_jail(channel, naughtdog_member, naughty_jail_role_, naughty_jail_sentence_time))

# Check if a user is naughty
def is_naughty():
    return random.choice(list(naughty_choices))

# Returns a naughty jail message
def naughty_jail_message(naughtdog):
    naughty_message = f"{random.choice(naughty_jail_messages)} <@{naughtdog}>.\n" 
    return naughty_message

# Print users in naughty jail
async def print_jail(channel):
    role = discord.utils.get(channel.guild.roles, name=naughty_jail_role)
    naughty_jail_text = f"𝐇𝐎𝐑𝐍𝐘 𝐉𝐀𝐈𝐋:\n"
    for member in channel.members:
        if role in member.roles:
            naughty_jail_text += f"<@{member.id}>\n"
    await channel.send(naughty_jail_text)

# Check naughty cooldown
def naughty_cooldown_check(naughty_offender):
    # Grab cluster, db, and collection
    cluster = MongoClient(MONGO_CONNECTION_URL)
    db = cluster[MONGO_DB]
    collection = db[MONGO_COLLECTION_USERS]

    # Check cooldown time
    naughty_check_time = collection.find_one({'_id':naughty_offender})['last_naughty_check']
    current_time = current_time_in_seconds()
    time_since_poked = get_time_since_last(current_time, naughty_check_time)
    return time_since_poked <= naughty_check_cooldown

# Set naughty cooldown
def set_naughty_cool_down(channel, naughty_offender):
    # Grab cluster, db, and collection
    cluster = MongoClient(MONGO_CONNECTION_URL)
    db = cluster[MONGO_DB]
    collection = db[MONGO_COLLECTION_USERS]

    current_time = current_time_in_seconds()
    collection.update_one({"_id":naughty_offender}, {"$set": {"last_naughty_check": current_time}}) 

# Check how recently a user has requested a permi
def permit_request_time_check(asker):
    # Grab cluster, db, and collection
    cluster = MongoClient(MONGO_CONNECTION_URL)
    db = cluster[MONGO_DB]
    collection = db[MONGO_COLLECTION_USERS]

    request_time = collection.find_one({'_id':asker})['last_permit_request']
    current_time = current_time_in_seconds()
    time_since_asked = get_time_since_last(current_time, request_time)

    return time_since_asked >= permit_request_cooldown

# Give a user a naughty permit
async def give_naughty_permit(channel, asker):
    # Grab cluster, db, and collection
    cluster = MongoClient(MONGO_CONNECTION_URL)
    db = cluster[MONGO_DB]
    collection = db[MONGO_COLLECTION_USERS]

    # If the user has not asked again too quickly:
    if permit_request_time_check(asker) is True:
        if random.randint(0, 100) < permit_request_chance:
            # If the user is lucky, they get the permit
            current_time = int(current_time_in_seconds())
            collection.update_one({"_id":asker}, {"$set": {"has_naughty_permit": 1}})
            collection.update_one({"_id":asker}, {"$set": {"naughty_permit_start_time": current_time}})
            await channel.send(f"You have my permission to be naughty for just a little bit <@{asker}>.")
            collection.update_one({"_id":asker}, {"$set": {"last_permit_request": current_time}})
        else:
            # Otherwise, the user is donwvoted for unluckiness
            await channel.send(f"No permit for you, sinner <@{asker}>.")
            await channel.send(f"{downvote_user(asker)} for unluckiness")
            current_time = int(current_time_in_seconds())
            collection.update_one({"_id":asker}, {"$set": {"last_permit_request": current_time}})
    else:
        # Downvote for impatience
        await channel.send(f"No permit for you, sinner <@{asker}>.")
        await channel.send(f"{downvote_user(asker)} for impatience")
        current_time = int(current_time_in_seconds())
        collection.update_one({"_id":asker}, {"$set": {"last_permit_request": current_time}})

# Frees user from naughty jail
async def free_from_naughty_jail(channel, naughtdog, role, time_to_release):
    await asyncio.sleep(time_to_release)
    await naughtdog.remove_roles(role)
    await channel.send(f"Oh god hide the children <@{naughtdog.id}> is out of naughty jail.")

# Allows naughty strikes to have a duration (rather than being permanent until a user is sent to jail where the strkes are then reset)
async def remove_naughty_strike_async(naughty_offender, strikes_to_take, collection, cooldown_time):
    await asyncio.sleep(cooldown_time)
    take_naughty_strikes(naughty_offender, strikes_to_take, collection)



################# VC Joins #################

# Bot randomly joins the vc
async def random_join(vchannel, chance, cooldown):
    while True:
        # If there are uses in the selected vc
        if len(vchannel.members) > 0 and check_rjoin_mode() is True:
            # Chance
            if random.randint(0, 100) < chance:
                # Join the vc and play an mp3 file
                vc = await vchannel.connect()
                vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(random.choice(mp3_files)), volume=1.0))
                while vc.is_playing():
                    await asyncio.sleep(1)
                await asyncio.sleep(0.5)
                # DC from the vc
                await vc.disconnect()
        await asyncio.sleep(cooldown)

# Toggles vc join mode
def toggle_rjoin_mode():
    reader = csv.reader(open(r_join_file))
    lines = list(reader)
    if int(lines[1][0]) == 1:
        lines[1][0] = 0
    else:
        lines[1][0] = 1
    writer = csv.writer(open(r_join_file, "w"))
    writer.writerows(lines)

# Checks vc join mode
def check_rjoin_mode():
    with open (r_join_file, 'r') as csv_file:
        line_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_file:
            if line_count == 0:
                line_count += 1
            else:
                return int(row[0]) == 1
################# VC Joins #################
