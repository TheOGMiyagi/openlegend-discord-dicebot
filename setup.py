# setup.py

def main():
    token = input("Please Enter Your Discord Bot Token.\n")
    dice_channel = input("Please Enter The ID OF Your Dice Channel.")
    env_variables = f"DISCORD_TOKEN={token}\n" if dice_channel != None and dice_channel != None else f"DISCORD_TOKEN=[Your Bot Token Here]\n"
    env_variabels += f"DICE_CHANNEL={int(dice_channel)}"if dice_channel != None and dice_channel != None else f"DICE_CHANNEL=[Your Dice Channel ID Here]"
    with open(".\.env", w) as env_file:
        env_file.write(env_variables)
        env_file.close()

if __name__ == "__main__":
    main()