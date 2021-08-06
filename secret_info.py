# Twitter configuration
TWEEPY_CONSUMER_KEY = "INSERT HERE"
TWEEPY_CONSUMER_SECRET_KEY = "INSERT HERE"
TWEEPY_ACCESS_TOKEN = "INSERT HERE"
TWEEPY_ACCESS_TOKEN_SECRET = "INSERT HERE"
TARGET_TWITTER_USERNAME = "INSERT HERE"
TARGET_ID = 000000000000000
TARGET_DISCORD_USER_ID = "<@INSERT HERE>"

# MongoDB Configuration
MONGO_CONNECTION_URL = "INSERT HERE"
MONGO_DB = "INSERT_HERE"
MONGO_COLLECTION_USERS = "INSERT_HERE"
MONGO_COLLECTION_TIER_LIST = "INSERT_HERE"

# Discord Configuration
TOKEN = "INSERT HERE"
CHANNEL_ID = 000000000000
GUILD_ID = 0000000000000

# IDS
ADMIN_ID = 00000000000000000000


# Naughty choices
naughty_choices = {"is naughty.\n": 1, "is not naughty.\n": 0, "is aggressively naughty.\n": 1, "is in heat.\n": 1, "is threateningly naughty.\n":1}

# Times:
allowed_naughty_permit_time = 1800 # 30 minutes
naughty_jail_sentence_time = 2700 # 45 minutes
naughty_check_cooldown = 300 # 5 minutes
permit_request_cooldown = 1200 # 20 minutes
naughty_strike_cooldown = 3600 # 1 hour

# Naughty jail images
naughty_jail_images = [f"https://i.redd.it/dxzh1w27sog41.jpg", f"https://pbs.twimg.com/media/EnhcMHsUwAw0PFy?format=jpg&name=small", f"https://pbs.twimg.com/media/EUkTxaQU4AEA2p-?format=jpg&name=medium"]
# Naughty jail messages
naughty_jail_messages = [f"NO TALKING IN NAUGHTY JAIL", f"DO NOT TALK TO THE NON-SINNERS"]

# Bonk image
bonk_image = f"https://pbs.twimg.com/media/Eqzk4gKXAAU_Y0c?format=jpg&name=large"

# Hoeny jail role
naughty_jail_role = "In Naughty Jail"

# Chances
permit_request_chance = 25

# Mom status
mom_statuses = [f"be SQUIRTING", f"is doing very well", f"is a bit tired", f"is feeling wonderful"]

# Forbidden IDS
forbidden_ids = [000000000000000, 00000000000000, 0000000000000]

# Voice Channels
test_voice_channel = 00000000000000
cousin_dbd_voice_channel = 0000000000

# MP3 Clips
mp3_files = ["mp3_files/INSERT_HERE.mp3", "mp3_files/INSERT_HERE.mp3", "mp3_files/INSERT_HERE.mp3"]


# Join Chance
join_chance = 40
# Join cooldown
join_cooldown = 1200 # 20 minutes
# Random join file
r_join_file = "info/random_join.txt"

