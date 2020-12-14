#!/usr/bin/python

# Import libraries needed
import os, discord, random, asyncio
import func, msgs
from datetime import datetime as dt

# Set token so bot can connect to Discord services
tokenFile = open('../dnd-token.txt', 'r')
TOKEN = tokenFile.read()
tokenFile.close()

# Set event loop
loop = asyncio.get_event_loop()

# Set bot's client
client = discord.Client()

# # # # # # # # # # # # # # # # # # # # # # # # #

### Event Call
@client.event
## Run when bot is fully loaded in
async def on_ready():
    print("-------------------------")
    print(client.user.name)
    print(client.user.id)
    print(dt.utcnow().strftime("%m/%d/%Y %H:%M:%S"))
    print("-------------------------")


### Event Call
@client.event
## Run when a message is sent that the bot can read
async def on_message(msg):
    # Only activates if the message is a command message and isn't from the bot
    if msg.author != client.user and str(msg.content[0]) == "!":
        await msgs.on_message(msg)

### Event Call
@client.event
## Run when a message is sent that the bot can read
async def on_disconnect():
    await client.close()

# # # # # # # # # # # # # # # # # # # # # # # # #

### Loop to run the bot
## Loop bot under normal conditions
try:
    # Start the bot
    loop.run_until_complete(client.start(TOKEN))

## Intercepts terminal keyboard interrupt so I can make things look neat
except KeyboardInterrupt:
    # Sets bot status to offline so people know it's inactive
    loop.run_until_complete(client.change_presence(status=discord.Status.offline))
    # Print message to terminal
    func.terminalOutput("Poweroff")
    # Disconnect bot from Discord services
    loop.run_until_complete(client.logout())

## Runs after above is finished
finally:
    # Closes loop thread on OS
    loop.close()
    # Reruns bot (press Ctrl+C during this to kill the bot)
    os.system("python3 bot.py")