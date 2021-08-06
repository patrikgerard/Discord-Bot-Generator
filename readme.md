This is a generic bot that you can customize!

Some cool things it can do:

1. Calculate a tier list in real-time based on the point distribution of the users in the discord
2. Do naughty checks on discord members and send members to naughty jail
3. Join the vc and play .mp3 files and then dc
4. Ridicule a random user for their tweets
5. Others!

Install:
 - Use pip to install the necessary packages ("necessary_packages.txt")
 - Set up a mongodb account and collection -- documentation here: https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
    - Connect the mongodb account to the bot by inputting the necessary info in secret_info.py:
        1.  MONGO_CONNECTION_URL
        2.  MONGO_DB
        3.  MONGO_COLLECTION_USERS
        4.  MONGO_COLLECTION_TIER_LIST
 - Set up the discord bot's settings:
    - https://discord.com/developers/applications/
    - Instructions for setup: https://discordpy.readthedocs.io/en/stable/discord.html
    - Connect the discord bot to the actual code in secret_info.py:
        1. TOKEN
        2. CHANNEL_ID
        3. GUILD_ID
 - Set up tweepy api (to read user's tweets)
    - https://realpython.com/twitter-bot-python-tweepy/
 - Add mp3 files and other miscellaneous info (ensure that all of secret_info.py is filled)

 - More information here: 
    https://patrickgerard.co/projects/discord-bot

