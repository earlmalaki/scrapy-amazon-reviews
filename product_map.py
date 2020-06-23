########################################
# Author : Earl Timothy D. Malaki
# User Experience Designer
# Plaza 2 6th Floor C'10 6
# Lexmark Research and Development Cebu
########################################

# Product Map Matrix
# Map which models belong to which codenames, and which codename belongs to program.
# [
#   [Program, Codename, [Models]],
#   [Program, Codename, [Models]],
#   [Program, Codename, [Models]]
# ]
PRODUCT_MAP = [
    ["Baja/Donzi (BD)", "Baja", ["B3442dw", "B3340dw"]],
    ["Baja/Donzi (BD)", "Donzi", ["MB3442adw"]],
    ["Big Blue/Needlefish (BBN)", "Big Blue", ["C3426dw"]],
    ["Big Blue/Needlefish (BBN)", "Needlefish", ["MC3426adw"]],
    ["Bluering/Lionfish (BRLF)", "Bluering", ["C3224dw", "C3326dw"]],
    ["Bluering/Lionfish (BRLF)", "Lionfish", ["MC3224adwe", "MC3224dwe", "MC3326adwe"]],
    ["Sidu/Goldengate (SGG)", "Sidu", ["B2236dw"]],
    ["Sidu/Goldengate (SGG)", "Goldengate", ["MB2236adwe", "MB2236adw"]],
    ["Zues/Jupiter (ZJ)", "Zues", ["C2325dw"]],
    ["Zues/Jupiter (ZJ)", "Jupiter", ["MC2425adw"]],
    ["Skyfall/Moonraker (SM)", "Skyfall", ["MB2338adw", "MB2442adwe"]]
    # ['Skyfall/Moonraker (SM)', 'Moonraker', ],
]

# Program | Codename | Model
# [program, [codename1,codename2], model]
# Given a model name, return the printer program and codename
def get_program_codename(string):
    for product in PRODUCT_MAP:
        for model in product[2]:
            if model == string:
                # Input model matched with model
                # Return Program Name, Codename
                return [product[0], product[1]]
    return ["TBD", "TBD"]


# PROGRAM
# Baja/Donzi (BD)
# Big Blue/Needlefish (BBN)
# Bluering/Lionfish (BRLF)
# Sidu/Goldengate (SGG)
# Zues/Jupiter (ZJ)
# Skyfall/Moonraker (SM)

# Mackinac/Macau (MM)
# Eagle/Hudson/Rhine (EHR)
# Saipai/Maui (SM)
# Scout/Nile (SN)

# CODENAME - MODEL
# Baja=[B3442dw,B3340dw]
# Donzi=[MB3442adw]
# BigBlue=[C3426dw]
# Needlefish=[MC3426adw]
# BlueRing=[C3224dw,C3326dw]
# Lionfish=[MC3224adwe,MC3224dwe,MC3326adwe]
# Sidu=[B2236dw]
# Goldengate=[MB2236adwe,MB2236adw]
# Zeus=[C2325dw]
# Jupiter=[MC2425adw]
# Skyfall=[MB2338adw,MB2442adwe]
