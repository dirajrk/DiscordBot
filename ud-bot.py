"""
ud-bot (Placeholder name) is a Discord chat bot powered by Discord.py by Diraj Ravikumar.
Things it can do:
* Notify when a user joins/leaves the server
* Notify when a user gets banned/unbanned from the server
* Retrieve UrbanDictionary links
* Retrieve LMGTFY links in case someone's lazy to Google it out
* Barebones Google Search
* Retrieve user avatar
* Retrieve weather status
* Retrieve last.fm now playing status
(Some might need admin/mod permissions)
"""

# To import discord functionalities
import discord
import asyncio
import pyowm
import pylast
from discord.ext import commands

client = discord.Client()

# OpenWeatherMap API key for weather related stuff
owm = pyowm.OWM('OpenWeatherMapAPI Key')
# last.fm API for scrobbling related stuff
lfmnetwork = pylast.LastFMNetwork(api_key="last.fm API KEY",
                                       api_secret="last.fm API SECRET", username="last.fm USERNAME",
                                       password_hash="last.fm PASSWORD HASH") # use pylast.md5("last.fm PASSWORD") and print it to retrieve password hash


# Timer for how long these messages should last, modify to your value and these are in seconds
SLEEP_TIME = 25

@client.event
async def on_ready():
    # When bot is up and running, these messages print out in the console
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='Radiohead I suppose'))

# Checks if message sent by the bot
def is_me(message):
    return message.author == client.user

# When a member joins the group
@client.event
async def on_member_join(member):
    await client.send_message(member.server, content="**HELLO THERE:** " + member.mention + " has joined " + member.server.name)

# When a member leaves the group	
@client.event
async def on_member_remove(member):
    await client.send_message(member.server, content=member.mention + " has left " + member.server.name + ". Hasta la vista!")

# When a member gets banned
@client.event
async def on_member_ban(member):
    await client.send_message(member.server, content=member.mention + " has been banned from " + member.server.name)

# When a member gets unbanned
@client.event
async def on_member_unban(server, user):
    await client.send_message(server.default_channel, content=user.name + " has been unbanned.")

# Set of functionalities, productive or not
@client.event
async def on_message(message):

    # UrbanDictionary functionality
    if message.content.startswith('!ud'):
        await client.send_message(message.channel, 'https://www.urbandictionary.com/define.php?term={}'.format(message.content).replace('!ud', '').replace(' ', '+'))
        await asyncio.sleep(SLEEP_TIME)
        await client.purge_from(message.channel, limit=1, check=is_me)

    # Let Me Google That For You functionality
    elif message.content.startswith('!lmgtfy'):
        await client.send_message(message.channel, 'http://lmgtfy.com/?q={}'.format(message.content).replace('!lmgtfy', '').replace(' ', '+'))
        await asyncio.sleep(SLEEP_TIME)
        await client.purge_from(message.channel, limit=1, check=is_me)

    # Barebones Google Search functionality
    elif message.content.startswith('!goog'):
        await client.send_message(message.channel, 'https://www.google.com/search?q={}'.format(message.content).replace('!goog', '').replace(' ', '+'))
        await asyncio.sleep(SLEEP_TIME)
        await client.purge_from(message.channel, limit=1, check=is_me)

    # User avatar
    elif message.content.startswith('!avatar'):
        result = ""
        if message.mentions:
            for mention in message.mentions:
                result += "{}: {}\n".format(mention.name, mention.avatar_url)
            await client.send_message(message.channel, result)
        else:
            result = "{}: {}".format(message.author.name, message.author.avatar_url)
            await client.send_message(message.channel, result)
        await client.delete_message(message)

    # Provides a city's weather status
    elif message.content.startswith('!weather'):
        await client.send_message(message.channel, 'Enter city name for weather? Type !city cityname')
        def check(msg):
            # Check message for command and replace it
            return msg.content.startswith('!city')

        message = await client.wait_for_message(author=message.author, check=check)
        city = message.content[len('!city'):].strip()

        # Detailed weather status
        observation = owm.weather_at_place('{}'.format(city))
        w = observation.get_weather()
        detailed_stat = w.get_detailed_status()
        await client.send_message(message.channel, '{} at {}'.format(detailed_stat.title(), city))

    # last.fm scrobbling
    elif message.content.startswith('!np'):
        lfmusername = message.content.replace('!np', '').strip()
        await client.send_message(message.channel, '{} is listening to {}'.format(lfmusername, network.get_user(lsusername).get_now_playing()))

# Replace string with your bot token
client.run('Discord Bot Token')
