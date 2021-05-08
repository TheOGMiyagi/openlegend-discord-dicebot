# enc_calc.py
import utils

# Party Class
class Party:
    #*  Constructor
    def __init__(self, *Levels):
        self.levels = []
        # Handles Different Data Types
        for item in Levels:       # Iterates Through Self.Levels
            if type(item) == int:      # If The Item Is An Integer, Add It To Total
                self.levels.append(item)
            elif type(item) == list or type(item) == tuple:     # If The Item Is A Tuple Or List, Iterate Through it, Adding Its Items To Total
                for x in item:
                    self.levels.append(x)
        print(f"New Instance Of The {self.__class__.__name__} Class:\n", self.__dict__)
    
    #*   NUMBER OF MEMBERS
    @property
    def members(self):
        return len(self.levels)
    @members.setter         # Allows The Attribute To Be Set
    def members(self, Members: int):
        self.members = Members
    
    #*   TOTAL PLAYER LEVELS IN THE PARTY
    @property
    def total_levels(self):
        return sum(self.levels)
    @total_levels.setter    # Allows The Attribute To Be Set
    def total_levels(self, TotalLevels: int):
        if type(TotalLevels) != int:
            raise TypeError(f"TypeError: TotalLevels' data type is {type(TotalLevels)}, not int.")
        else:
            self.total_levels = TotalLevels
    
    #?   AVERAGE PLAYER LEVEL
    @property
    def average_level(self):
        return round(self.total_levels / self.members)
    
    #?   NORMAL ENCOUNTER CALCULATIONS
    @property
    def easy_encounter(self):
        return utils.floor(self.total_levels / 2)
    @property
    def moderate_encounter(self):
        return self.total_levels
    @property
    def hard_encounter(self):
        return self.total_levels * 2
    
    #?   MINION HORDE CALCULATIONS
    @property
    def easy_horde(self):
        return utils.floor(self.easy_encounter / self.average_level) * 3
    @property
    def moderate_horde(self):
        return utils.floor(self.moderate_encounter / self.average_level)* 3
    @property
    def hard_horde(self):
        return utils.floor(self.hard_encounter / self.average_level) * 3
    
    #?   BOSS ENCOUNTER CALCULATIONS
        #! The Easy Boss Encounter Formula Is Unbalanced & Returns Invalid Values
    #@property
    #def easy_boss(self):
        #bosses = round((self.easy_encounter / (self.average_level)) / 2)
        #if bosses > 0:
        #    return bosses
        #else:
        #    return 0
    @property
    def moderate_boss(self):
        bosses = utils.floor(self.moderate_encounter / (self.average_level * 4))
        if bosses > 0:
            return bosses
        else:
            return 0
    @property
    def hard_boss(self):
        bosses = utils.floor(self.hard_encounter / (self.average_level * 4))
        if bosses > 0:
            return bosses
        else:
            return 0







# Only Used In Main()
def get_user_input(same_levels_flag=False):
    try:
        if same_levels_flag == True:
            party_size = input("Enter Your Party's Size.\n")
            party_level = input("Enter Your Party's Level.\n")
            levels_ints = []
            for x in range(int(party_size)):
                levels_ints.append(party_level)
            return levels_ints, same_levels_flag
        else:
            usr_input = input("Please Enter The Levels Of Your Party Members.\n(Separated By Commas)\n")
            with usr_input.split(", ") as levels_list:
                levels_ints = [int(value) for value in levels_list]
            return levels_ints, same_levels_flag
    except Exception as e:
        print(f"Oh no! {e.__class__} has occured.", e)

# Main Method
def main():
    #usr_input = get_user_input()
    #test = Party(usr_input[0])
    test = Party([1, 2, 3, 4])
    print("\n", f"Members In The Party: {test.members}",
        "\n", f"Total Party Levels: {test.total_levels}",
        "\n", f"Average Party Member Level: {test.average_level}",
        "\n", f"Total Party Easy: {test.easy_encounter}",
        "\n", f"Total Party Medium: {test.moderate_encounter}",
        "\n", f"Total Party Hard: {test.hard_encounter}")

# Driver Code
if __name__ == "__main__":
    print ("\n\n")
    main()
    print ("\n\n")
else:
    print(f"The {__name__} module was successfully imported.\n\n")
