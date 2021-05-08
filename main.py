# <--- IMPORTS --->
from typing import Pattern              # IMPORTS PATTERN FROM TYPING
import discord                          # IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
from discord.ext import commands        # IMPORT COMMANDS FROM THE DISCORD.EXT MODULE.
from discord.ext.commands import Bot    # IMPORT BOT FROM DISCORD.EXT.COMMANDS
import utils                            # IMPORT UTILS.PY
from enc_calc import Party              # IMPORT THE PARTY CLASS FROM ENC_CALC.PY
import os                               # IMPORT THE OS MODULE.
import asyncio                          # IMPORT THE ASYNC INPUT/OUTPUT
from dotenv import load_dotenv          # IMPORT THE LOAD_DOTENV METHOD FROM DOTENV
load_dotenv()                           # LOADS ENVIRONMENT VARIABLES FROM THE LOCAL .ENV FILE


# <--- BOILERPLATE CODE --->
bot_prefix = "."
bot = commands.Bot(command_prefix=bot_prefix)
TOKEN = os.environ['DISCORD_OPENLEGEND_BOT_TOKEN']
GitHub_Repo = os.environ['GITHUB_REPO_LINK']

# <---- Removes Built-In Help Command --->
bot.remove_command('help')

# <--- Console Ready --->
@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following guilds:\n')
    for guild in bot.guilds:
        print(f'{guild.name} (id: {guild.id})')


# <--- Commands --->
#? Help Command
@bot.command(name="help",aliases=["h", "Help", "H"],description="Returns The Custom Help Message From ./usage_help_msg.")
async def help(ctx):
    file = open("./usage_help_msg", "r")
    msg = file.read()
    file.close()
    await ctx.send(msg)

#? Source Code Command
@bot.command(name="source code",aliases=["src"],description="Returns The GitHub Repository For The Running Version Of The Bot.")
async def source_code(ctx):
        msg = f"**Source Code:** {GitHub_Repo}"
        await ctx.send(msg)


# Legacy Command Handler
@bot.event
async def on_message(message):
    #? Ignores Messages From Itself
    if message.author == bot.user:
        return
    
    #? Roll Command
    if message.content.startswith(f"{bot_prefix}r") or message.content.startswith(f"{bot_prefix}roll"):
        check_err = utils.parse_msg(
            message.content)
        if check_err == -1:
            await message.channel.send("Ooops...Wrong arguments!")
        else:
            vicious, destructive, attr_score, adv, repeat_factor = utils.parse_msg(
                message.content)
            results, info = utils.calculate_result(
                vicious, destructive, attr_score, adv, repeat_factor)
            #*  OUTPUT MESSAGE
            msg = f"__{message.author.display_name} rolled__: "
            
            for result in results:
                msg += f"\n\n**Roll {results.index(result)+1}**"

                total_base = sum(sum(result[0][0], []))
                total_attr = sum(sum(result[1][0], []))
                separator = " "
                table = str.maketrans('[]', '()')

                base_kept = separator.join(
                    map(str, result[0][0])).translate(table)

                base_dropped = separator.join(
                    map(str, result[0][1])).translate(table)
                if base_dropped == "":
                    base_dropped = "-"

                base_dropped_vs = separator.join(
                    map(str, result[0][2])).translate(table)
                if base_dropped_vs == "":
                    base_dropped_vs = "-"

                attr_kept = separator.join(
                    map(str, result[1][0])).translate(table)
                if attr_kept == "":
                    attr_kept = "-"

                attr_dropped = separator.join(
                    map(str, result[1][1])).translate(table)
                if attr_dropped == "":
                    attr_dropped = "-"

                
                    #? BASE ROLL INFO
                msg += f"\n----------\nTotal: {(total_base + total_attr)} \nBase (1d20 -> {total_base}): \t {base_kept}\n"
                # Hides Dropped rolls if there are none.
                if base_dropped != "-" and base_dropped != "0":
                    msg += f"> \t *Dropped: {base_dropped}*\n"
                # Hides Vicious Strike if there is no value associated with the dropped values.
                if base_dropped_vs != "-" and base_dropped_vs != "0":
                    msg += f"> \t _Dropped  **(Vicious Strike)**: {base_dropped_vs}_\n"
                    #?   ATTRIBUTE ROLL INFO
                msg += f"Attribute ({info} -> {total_attr}): \t {attr_kept}"
                # Hides Dropped rolls if there are none.
                if attr_dropped != "-" and attr_dropped != "0":
                    msg += f"\n> \t *Dropped: {attr_dropped}*"

            await message.channel.send(msg)

    #? Raw Roll Command
    elif message.content.startswith(f"{bot_prefix}!r") or message.content.startswith(f"{bot_prefix}!roll"):
        args = message.content.split(" ")[1:]
        result = utils.roll_raw(args[0])
        if result != -1:
            await message.channel.send(f"{message.author.display_name} rolled: {args[0]} -> {result}")
    
    #? Encounter Calculator Command
    elif message.content.startswith(f"{bot_prefix}encounter") or message.content.startswith(f"{bot_prefix}enc"):
        bot_say = message.channel.send
        try:
        #*  PARTY SIZE
            # Fetches The Party's Size & Asks If The 
            await bot_say("Please Enter Your Party Size.\n")
            party_size = await bot.wait_for("message", check=lambda msg: msg.author == message.author, timeout=30) # 30 seconds to reply
            await bot_say("Are All Of Your Party Members The Same Level?\n")
            same_levels_flag = await bot.wait_for("message", check=lambda msg: msg.author == message.author, timeout=30) # 30 seconds to reply

        #*  PARTY LEVELS
            levels = []
            #? If Party Member Levels Are The Same...
            if same_levels_flag.content.lower() == "y" or same_levels_flag.content.lower() == "yes":
                    #   Fetches The Party's Shared Level & Sets Each Member's Level To It
                    await bot_say("Please Enter The Level Of Your Party.\n")
                    shared_party_level = await bot.wait_for("message", check=lambda msg: msg.author == message.author, timeout=30) # 30 seconds to reply
                    for x in range(int(party_size.content)):
                        #!  Looping Through An Incremental Index Is Preferred To Appending, As It Ensures That The Length Of The List Stays The Same
                        levels[x+1] = int(shared_party_level.content)

            #? If Party Member Levels Are NOT The Same...
            elif same_levels_flag.content.lower() == "n" or same_levels_flag.content.lower() == "no":
                #*   Loops For Each Member Of The Party
                for x in range(int(party_size.content)):
                    # Fetches The Party Member's Level & Appends It To The "levels" List
                    await bot_say(f"Please Enter The Level Of Party Member #{x+1}.\n")
                    input_msg = await bot.wait_for("message", check=lambda msg: msg.author == message.author, timeout=30) # 30 seconds to reply
                    levels.append(int(input_msg.content))
        except asyncio.TimeoutError:
            await bot_say("Sorry, you didn't reply in time!")
        resulting_party = Party(levels)
        
        #*   OUTPUT MESSAGE
        output = ("**__Party Information__**\n"
                    f"> **Members In The Party:**\t`{resulting_party.members}`\n"
                    f"> **Total Party Levels:**\t`{resulting_party.total_levels}`\n"
                    f"> **Party Member Average Level:**\t{resulting_party.average_level}\n\n"
                    #? NORMAL ENCOUNTERS
                    "**__Normal Encounters__**\n"
                    f"> **Total NPC Levels _(__Easy__ Encounter)_ :**\t`{resulting_party.easy_encounter}`\n"
                    f"> **Total NPC Levels _(__Moderate__ Encounter)_ :**\t`{resulting_party.moderate_encounter}`\n"
                    f"> **Total NPC Levels _(__Hard__ Encounter)_ :**\t`{resulting_party.hard_encounter}`\n\n"
                    #? HORDE ENCOUNTERS
                    "**__Minion Horde Encounters__**\n"
                    f"> **Number Of _LVL {resulting_party.average_level}_ Minions _(__Easy__ Encounter)_ :**\t`{resulting_party.easy_horde}`\n"
                    f"> **Number Of _LVL {resulting_party.average_level}_ Minions _(__Moderate__ Encounter)_ :**\t`{resulting_party.moderate_horde}`\n"
                    f"> **Number Of _LVL {resulting_party.average_level}_ Minions _(__Hard__ Encounter)_ :**\t`{resulting_party.hard_horde}`\n\n"
                    
                    #? BOSS ENCOUNTERS
                    "**__Boss Battle Encounters__**\n"
                    #"> **Number Of Boss NPCs _(__Easy__ Encounter)_ :**\n"
                    #f"> `{resulting_party.easy_boss}` _LVL {utils.floor(resulting_party.members)}_ Boss\n"
                    "> **Number Of Boss NPCs _(__Moderate__ Encounter)_ :**\n"
                    f"> `{resulting_party.moderate_boss}` _LVL {resulting_party.average_level}_ Boss, or `{resulting_party.moderate_boss * 2}` _LVL {round(resulting_party.average_level * 0.75)}_ Bosses\n"
                    "> **Number Of Boss NPCs _(__Hard__ Encounter)_ :**\n"
                    f"> `{resulting_party.hard_boss}` _LVL {resulting_party.average_level}_ Boss, or `{round(resulting_party.hard_boss * 0.74) * 2}` _LVL {round(resulting_party.average_level * 0.70)}_ Bosses")
        
        await bot_say(output)

if __name__ == "__main__":
    if TOKEN == "[Your Bot Token Here]":
        raise ValueError("Please set up your Bot Token by either using the included setup.py or by manually editing the local .env file.")
    else:
        bot.run(TOKEN)
