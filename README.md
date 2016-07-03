# randominions4
A map / independent randomizer for Dominions 4
Reads a map file and a independent definition file and outputs a mod file and a map file that can be used to play.

# Usage
Run the script to open a GUI which allows you to set the parameters for the script. It is possible to load multiple indy definitions at the same time, they all will be used.

Coastal, forest, swamp and cave starts are not in addition to land start positions, but define necessary start positions for known nations (for example Pangaea _must_ start in a forest or the game will refuse to start).

Rare chance means chance for extra defenders in a province, they do not affect the recruitment options and PD you get.

It is also possible to run the script on command line, to do so run the randominions4.py script, with parameters: input_map_file output_map_file indy_definitions number_of_land_nations number_of_water_nations number_of_coastal_starts number_of_forest_starts number_of_swamp_starts number_of_cave_starts lvl_1_thrones lvl_2_thrones lvl_3_thrones chance_for_rare_indies strength_of_indies

# License
MIT