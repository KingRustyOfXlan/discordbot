#!/usr/bin/env python
# vim: set foldmethod=marker:

# Imports {{{

# Import libraries needed
import os, sys, discord, random, asyncio, signal
from datetime import datetime as dt

# }}}

# Variables and Definitions {{{

# Set token so bot can connect to Discord services
tokenFile = open(os.path.dirname(os.path.realpath(sys.argv[0])) + '/../.dnd-token.txt', 'r')

TOKEN = tokenFile.read()
tokenFile.close()

# Set event loop
loop = asyncio.get_event_loop()

# Set bot's client
client = discord.Client()

#reactMsgID = [
#        814893886124064768]

# SIGTERM exit signal handler, mainly here to work with systemd
def sigterm_handler(sig, frame):
    raise SystemExit

# }}}

# Startup {{{

# Run when bot is fully loaded in
@client.event
async def on_ready():
    print("-------------------------")
    print(client.user.name)
    print(client.user.id)
    print(dt.utcnow().strftime("%m/%d/%Y %H:%M:%S"))
    print("-------------------------")

# }}}

# Client Events {{{

@client.event
async def on_message(m):
    # Make sure the bot doesn't check for its own messages
    if m.author == client.user:
        return

# Roll Command {{{

    if m.content.startswith("!roll"):
        # Main part being taken from message
        mS = str(m.content)[6 :]

        # Values to be determined
        die = 0
        mul = 1

        # String for results
        rolls = ""
        
        # Look for multiplier
        if '*' in mS:
            # Set die number and roll multiplier
            die = int(mS[: mS.find('*')])
            mul = int(mS[mS.find('*') + 1 :])
        else:
            die = int(mS)

        # Cap to make sure there isn't an overflow
        if die > 100 or mul > 100:
            await m.channel.send( embed = discord.Embed(
                title = "{0.author.name}: Roll Error".format(m),
                description = "Die > 100 OR Multiplier > 100",
                color = discord.Color( 0xff0000 )
                )
            )
            print( "Roll:\n     Error: cap exceeded" )
            return
        # The good stuff, run RNG and append to "rolls" string
        else:
            for i in range(0, mul):
                if i == mul - 1:
                    rolls += str( random.randrange(0, die) + 1 )
                else:
                    rolls += str( random.randrange(0, die) + 1 ) + ", "
        # Send embedded message containing results
        await m.channel.send( embed = discord.Embed(
            title = "{0.author.name}: Roll Result".format(m),
            description = rolls,
            color = discord.Color(0x00ff00)
            )
        )
        print(
                "Roll:\n     User:{0.author.name}".format(m) +
                "     Die: {}".format(die) +
                "     Result: {}".format(rolls)
        )

# }}}

    # Reaction test
#    if m.content[1:] == "t":
#        msg = await m.channel.send("Press below to react")
#        reactMsgID = msg.id
#        await msg.add_reaction("\U0001F49C")
#        await msg.add_reaction("\U0001F499")
#        await msg.add_reaction("\U0001F49B")

#@client.event
#async def on_raw_reaction_add(p):
#    if p.message_id in reactMsgID:
#        channel = client.get_channel(p.channel_id)
#        print("added")

#@client.event
#async def on_raw_reaction_remove(p):
#    if p.message_id in reactMsgID:
#        channel = client.get_channel(p.channel_id)
#        print("removed")

# }}}

# Shutdown {{{

@client.event
# Run when bot disconnects from Discord
async def on_disconnect():
    await client.close()

# }}}

# Main Loop {{{

signal.signal(signal.SIGTERM, sigterm_handler)

# Loop bot under normal conditions
try:
    loop.run_until_complete(client.start(TOKEN))

# Intercepts terminal keyboard interrupt so I can make things look neat
except (KeyboardInterrupt , SystemExit):
    # Sets bot status to offline so people know it's inactive
    loop.run_until_complete(client.change_presence(status=discord.Status.offline))

    # Print message to terminal
    print("{} Shutdown".format(dt.utcnow().strftime('%d-%m_%H-%M-%S')))

    # Disconnect bot from Discord services
    loop.run_until_complete(client.logout())

# Runs after above is finished
finally:
    # Closes loop
    loop.close()

# }}}
