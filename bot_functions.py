#!/usr/bin/env python3

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

CONSUMER_KEY = secret_info.CONSUMER_KEY
CONSUMER_SECRET_KEY = secret_info.CONSUMER_SECRET_KEY

ACCESS_TOKEN = secret_info.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = secret_info.ACCESS_TOKEN_SECRET 

SEARS_TWITTER_USERNAME = secret_info.SEARS_TWITTER_USERNAME
SEARS_DISCORD_USER_ID = secret_info.SEARS_DISCORD_USER_ID

CONNECTION_URL = secret_info.CONNECTION_URL

DOG_SOURCE = "https://www.criminallegalnews.org/news/2018/jun/16/doj-police-shooting-family-dogs-has-become-epidemic/"

INFORMATION_FILE_NAME ="information.txt"
ANNOY_MARK_FILE_NAME = "annoy_mark_mode.txt"
epoch = datetime(1970,1,1)
vote_refresh_time = 40
republican_voting_url = "https://rb.gy/wih8jw"
help_doc = "help.txt"
intro_doc = "introduction.txt"

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


# grabs sears' timeline
def retrieve_timeline( api, user ):
    return api.user_timeline(screen_name = user, include_rts = True)

# grabs a sears tweet
def grab_sears_tweet():

    # create authenticator
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # create api object
    api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

    # grab a tweet
    sears_tweets = retrieve_timeline(api, SEARS_TWITTER_USERNAME)
    number_of_tweets = len(sears_tweets)
    tweet = sears_tweets[randrange(number_of_tweets)]
    id = tweet._json['id']

    if "RT" in tweet._json['text']:
        text = api.get_status(id, tweet_mode = "extended").retweeted_status.full_text
        return f"This dickhead {SEARS_DISCORD_USER_ID} retweeted \"{text}\""
    else:
        text = api.get_status(id, tweet_mode = "extended")
        return f"{text.full_text}"

def create_user(user_to_create_id, creator_id=None):

    cluster = MongoClient(CONNECTION_URL)
    db = cluster["cousins"]
    collection = db["cousins_users"]

    if collection.count_documents({"_id": user_to_create_id}) > 0:
        if creator_id is None:
            return f"<@{user_to_create_id}> is already in rankings."
        else:
            down_vote_message = downvote_user(downvoted_id=creator_id)
            return f"<@{user_to_create_id}> is already in  cousin rankings. Minus one point for you <@{creator_id}>."
    current_time = int(current_time_in_seconds())
    post = {"_id": user_to_create_id,
     "points": 0,
     "tier": "B",
     "most_recent_vote_time": 0,
     "last_user_voted_on": user_to_create_id
    }
    collection.insert_one(post)
    set_update_needed()
    # add point to tier list date_checker
    # TODO: CALC TIER LIST AND TAKE POINT FROM DATE_CHECKER
    return f"<@{user_to_create_id}> added to cousin rankings."

# Upvotes a user
def upvote_user(upvoted_id, upvoter_id=None):
    if upvoted_id == None:
        return f"Who do you want me to upvote?"
    if upvoted_id == upvoter_id:
        return f"Go fuck yourself <@{upvoter_id}>."
    else:
        cluster = MongoClient(CONNECTION_URL)
        db = cluster["cousins"]
        collection = db["cousins_users"]

        # check that the user is in the database
        if collection.count_documents({"_id": upvoted_id}) != 1:
            user_created_message = create_user(user_to_create_id=upvoted_id)
            upvote_message = upvote_user(upvoted_id = upvoted_id)
            return f"<@{upvoted_id}> was created and upvoted."
        
        if upvoter_id != None:
            # Get the time since last vote
            last_vote = collection.find_one({'_id':upvoter_id})['most_recent_vote_time']
            current_time = current_time_in_seconds()
            time_since_last_vote = get_time_since_last_vote(current_time, last_vote)

            # Get the last user voted on
            last_user_voted_on = collection.find_one({'_id':upvoter_id})['last_user_voted_on']

            # see if they can vote
            voting_right = can_user_vote(last_user_voted_on, upvoted_id, time_since_last_vote)
            if voting_right != True:
                return f"Call me a Republican, because I\'m taking away your right to vote <@{upvoter_id}>.\n[Voting on the same person too quickly]"
        
        # Add a point and update the database
        points = collection.find_one({'_id':upvoted_id})['points']
        points += 1
        # add point to tier list date_checker
        set_update_needed()
        collection.update_one({"_id":upvoted_id}, {"$set": {"points": points}}) 
        set_vote_time_and_user(upvoted_id, upvoter_id)
        return f"<@{upvoted_id}> was upvoted."


# Downvotes a User
def downvote_user(downvoted_id, downvoter_id=None):

    if downvoted_id == None:
        return f"Who do you want me to downvote?"
    if downvoted_id == downvoter_id:
        return f"Go love yourself <@{downvoter_id}>."
    else:
        cluster = MongoClient(CONNECTION_URL)
        db = cluster["cousins"]
        collection = db["cousins_users"]

        # Check if the account exists
        if collection.count_documents({"_id": downvoted_id}) != 1:
            user_created_message = create_user(user_to_create_id=downvoted_id)
            downvote_message = downvote_user(downvoted_id = downvoted_id)
            return f"<@{downvoted_id}> was created and downvoted."
        
        # Check if they can vote
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
        
        # check that the user is in the database

        
        # Add a point and update the database
        points = collection.find_one({'_id':downvoted_id})['points']
        points -= 1
        # add point to tier list date_checker
        set_update_needed()
        collection.update_one({"_id":downvoted_id}, {"$set": {"points": points}})
        set_vote_time_and_user(downvoted_id, downvoter_id)
        return f"<@{downvoted_id}> was downvoted."

def calc_tier_list():

    cluster = MongoClient(CONNECTION_URL)
    db = cluster["cousins"]
    cousins_collection = db["cousins_users"]


    total_points = 0
    total_members = 0
    stdev_collector = [0]
    for member in list(cousins_collection.find({})):
        total_members += 1
        stdev_collector.append(member["points"])
        total_points += member["points"]

    average_points = total_points / total_members
    std_dev_points = stdev(stdev_collector)

    map_to_tier_list(total_points, average_points, std_dev_points)
    set_tier_up_to_date()
    # info_collection = db["update_info"]
    # info_collection.update_one({"_id":"update_info"}, {"$set": {"update_needed": 0}})


def print_tier_list():
    # Loop through tier list
    cluster = MongoClient(CONNECTION_URL)
    db = cluster["cousins"]
    collection_tier_list = db["tier_list"]

    for tier in collection_tier_list.find():
        yield f"**{tier['_id']} Tier:**"
        for member in tier['members']:
            yield f" \t<@{member}> "
    pass

def print_help_message():
    lines = open(help_doc, encoding='utf-8').read().splitlines()
    for line in lines:
        yield line

def print_intro_message():
    lines = open(intro_doc, encoding='utf-8').read().splitlines()
    for line in lines:
        yield line

def set_tier_up_to_date():
    reader = csv.reader(open(INFORMATION_FILE_NAME))
    lines = list(reader)
    lines[1][0] = 0

    writer = csv.writer(open(INFORMATION_FILE_NAME, "w"))
    writer.writerows(lines)

def tier_list_is_up_to_date():
    with open (INFORMATION_FILE_NAME, 'r') as csv_file:
        line_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_file:
            if line_count == 0:
                line_count += 1
            else:
                return int(row[0]) == 0
    #             print(row[0])
    # cluster = MongoClient(CONNECTION_URL)
    # db = cluster["cousins"]
    # update_needed_collection = db["update_info"]

    # query = {"_id": "update_info"}
    # info = update_needed_collection.find_one(query)
    # return info["update_needed"] == 0


def set_update_needed():
    reader = csv.reader(open(INFORMATION_FILE_NAME))
    lines = list(reader)
    lines[1][0] = 1

    writer = csv.writer(open(INFORMATION_FILE_NAME, "w"))
    writer.writerows(lines)


def map_to_tier_list(total_points, average_points, std_dev_points):
    tier_mapping =    { 
        'S' : round(average_points + (std_dev_points)), # ge
        'A': round(average_points + (std_dev_points*0.5)), # ge
        'B': round(average_points), # ge
        'C': round(average_points - (std_dev_points*0.75)), # le 
        'D': round(average_points - (std_dev_points*.95)), # le
        'Piss Dungeon': round(average_points - (std_dev_points)) # le
    }

    cluster = MongoClient(CONNECTION_URL)
    db = cluster["cousins"]
    collection_members = db["cousins_users"]
    collection_tier_list = db["tier_list"]
    # collection_update_info = db["update_info"]
    for tier in tier_mapping:
        collection_tier_list.update_one({"_id":tier}, {"$set":{"members": []}})

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
        else:
            tier = "Piss Dungeon"
        collection_tier_list.update_one({"_id":tier}, {"$push":{"members": member["_id"]}})
        # collection_update_info.update_one({"_id": "update_info"}, {"$set": {"update_needed": 0}})
        collection_members.update_one({"_id":member["_id"]}, {"$set": {"tier": tier}})


# Check who is the most horny
def horny_check(members):
    member_ids = [member.id for member in members]
    return random.choice(member_ids)

def horny_quote_generator(chosen_horndog):
    choice = "<@" + str(chosen_horndog) + ">"
    return "Mirror, mirror on the wall — " + choice + " is the horniest of them all.\nMinus one point for execessive horniness."

def dog_source():
    return f"{DOG_SOURCE}"

def dogs_killed():
    current_year = datetime(datetime.today().year, 1, 1)
    # current_year = date(datetime.today().year, 1, 1)
    current_date = datetime.today()
    
    #.strftime("%Y-%m-%d %I")
    
    # prev_date = datetime.strptime("2021-07-08 4","%Y-%m-%d %H")
    # delta_last_inquiry = current_date - prev_date
    # seconds_since_last_incquiry = delta_last_inquiry.seconds
    # dogs_killed_since_last_inquiry = round(seconds_since_last_incquiry/3600)

    seconds_since_year_start = (current_date - current_year).total_seconds() 
    dogs_killed_since_year_start = round(seconds_since_year_start/3600)

    dog_quotes = ["Ruff world!", "Talk about puppy love!", "Man's best friend! Pig\'s worst enemy!"]

    return f"There have been approximately {dogs_killed_since_year_start} dogs killed by cops this year. " + random.choice(dog_quotes) + "\n\nType \'!dogs_source\' for source."


def current_time_in_seconds():
    current_time = datetime.today()
    time =  (current_time - epoch).total_seconds()
    return time

def get_time_since_last_vote(current_time, last_vote):
    time = current_time - last_vote
    return int(time)

    
def can_user_vote(last_user_voted_on, current_user_voted_on, time_since_last_vote):
    if last_user_voted_on != current_user_voted_on:
        return True
    if (last_user_voted_on == current_user_voted_on) and  (time_since_last_vote <= vote_refresh_time):
        return False
    else:
        return True 

def set_vote_time_and_user(voted_id, voter_id):
    current_time = int(current_time_in_seconds())
    # time.sleep(10)
    second_time = int(current_time_in_seconds())
    cluster = MongoClient(CONNECTION_URL)
    db = cluster["cousins"]
    collection = db["cousins_users"]
    # print("current time: " + str(current_time))
    # time.sleep(10)
    if voter_id != None:
        collection.update_one({"_id":voter_id}, {"$set": {"last_user_voted_on":voted_id}})
        collection.update_one({"_id":voter_id}, {"$set": {"most_recent_vote_time": current_time}})
        vote_time = collection.find_one({'_id':voted_id})['most_recent_vote_time']
        # print(f"Set_vote_time_and_user: {vote_time}")
        # print(f"difference: {vote_time - current_time}")


def toggle_mark_mode():
    reader = csv.reader(open(ANNOY_MARK_FILE_NAME))
    lines = list(reader)
    if int(lines[1][0]) == 1:
        lines[1][0] = 0
    else:
        lines[1][0] = 1
    writer = csv.writer(open(ANNOY_MARK_FILE_NAME, "w"))
    writer.writerows(lines)

def check_mark_mode():
    with open (ANNOY_MARK_FILE_NAME, 'r') as csv_file:
        line_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_file:
            if line_count == 0:
                line_count += 1
            else:
                return int(row[0]) == 1