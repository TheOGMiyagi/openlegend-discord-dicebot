# openlegend-discord-dicebot
An [OpenLegend RPG][1] dice bot for [Discord][2] servers.

## Configuration

Set your [Discord Token][3] in env variable ```DISCORD_OPENLEGEND_BOT_TOKEN```

## Usage

```/roll [flags] [attribute] [advantage] [quantity]```

```/r [flags] [attribute] [advantage] [quantity]```
    
Flags:

 ```-R```: Repeat the roll 
 
 ```-V```: Vicious Strike: Exploding dice have advantage 
 
 ```-D```: Destructive Trance: Explode on max or one less

### Raw Dice Using xdice Patterns

```/!r [xdice pattern]``` 

```/!roll [xdice pattern]```

```xdice pattern```: Given pattern should be as described in [xdice documentation][4]. Use this to roll "raw", i.e. without any Open Legend RPG specific logic. 

## Used External Libraries 

- [Rapptz/discord.py][5]
- [cro-ki/xdice][6]

[1]: https://openlegendrpg.com/
[2]: https://discord.com/
[3]: https://discordpy.readthedocs.io/en/stable/discord.html
[4]: https://xdice.readthedocs.io/en/latest/dice_notation.html#patterns
[5]: https://github.com/Rapptz/discord.py
[6]: https://github.com/cro-ki/xdice
