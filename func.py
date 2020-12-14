#!/usr/bin/python
import os, discord, random

### Print output to terminal
def terminalOutput(output):
    from datetime import datetime as dt
    print('{} '.format(dt.utcnow().strftime('%m/%d/%Y %H:%M:%S')) + output)

### Roll die/dice
async def roll(msg, number):
    # String for roll results
    rolls = ""
    # Looks for roll multiplier
    if number.find('*') != -1:
        # Sets die number and roll multiplier
        dieNumber = int(number[:number.find('*')])
        multiplier = int(number[number.find('*') + 1:])

        # Caps die and multiplier at 100 so the bot doesn't die
        if dieNumber > 100 or multiplier > 100:
            terminalOutput('Roll:\n' + '    Error: roll die cap')
            # Send an embedded message telling user not to roll as much
            await msg.channel.send(embed=discord.Embed(
                title = "{0.author.name}".format(msg),
                description = "Die or multiplier too large, cap is 100",
                color = discord.Color.from_rgb(
                    255,
                    0,
                    0
                    )
                ))
            return # Do nothing

        # Calls RNG
        for i in range(0, multiplier):
            # Run RNG to find result
            rollValue = random.randrange(0, int(dieNumber)) + 1
            # Add the result of the RNG call to the result string
            if i == multiplier - 1:
                rolls = rolls + '{}'.format(rollValue)
            else:
                rolls = rolls + '{}, '.format(rollValue)

    # Calls RNG
    else:
        # Run RNG to find result
        rollValue = random.randrange(0, int(number)) + 1
        rolls = rolls + '{}'.format(rollValue) 
    terminalOutput(
        'Roll:\n    User:"{0.author.name}"'.format(msg) +
        '   Die: "{}"'.format(str(number)) +
        '   Result: "{}"'.format(str(rolls))
        )
    # Sends an embedded message containing the results of the roll
    await msg.channel.send(embed=discord.Embed(
        title = "{0.author.name}: Roll Result".format(msg),
        description = rolls,
        color = discord.Color.from_rgb(
            0,
            255,
            0
            )
        ))
