from enum import Enum
from collections import defaultdict

class Rarity(Enum):
    DEFAULT = 0
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    MYTHIC = 4


common_genes = ["Banded", "Barring", "Blanket", "Blaze", "Cloak", "Collared", "Comet",
               "Dawn", "Flurry", "Freckling", "Mask", "Pangare", "Points", "Powder",
                "Sable", "Saddle", "Skunk", "Soot", "Stocking", "Socks", "Underbelly",
                "Washed"]
uncommon_genes = ["Acid", "Brindle", "Dapple", "Dun", "Etched", "Jacket", "Merle",
                 "Quagga", "Ribbed", "Spotting", "Stained", "Stripes", "Vitiligo"]
rare_genes = ["Crawler", "Fawn", "Firefly", "Glass", "Leopard", "Marble",
              "Overo", "Piebald", "Skink", "Stratus", "Void", "Scaled"]

freecolour_genes = ["Comet", "Crawler", "Firefly", "Skink", "Stratus", "Void", "Scaled"]

common_discovery_genes = ["Ruffle"]
uncommon_discovery_genes = ["Gooey", "Melted"]
rare_discovery_genes = ["Fog"]

mythic_vesper_modifiers = ["Albinism", "Axanthic", "Melanism"]
mythic_gene_modifiers = ["Gleam"]
mythic_genes = ["Stardust"]

all_common_genes = common_genes + common_discovery_genes
all_uncommon_genes = uncommon_genes + uncommon_discovery_genes
all_rare_genes = rare_genes + rare_discovery_genes
all_mythic_genes = mythic_gene_modifiers + mythic_genes

common_bases = ["Smooth"]
uncommon_bases = ["Woolen"]
rare_bases = ["Maned"]

common_tails = ["Domestic", "Docked", "Pointed", "Strand", "Tufted"]
uncommon_tails = ["Bobbed", "Curled", "Reptile", "Silk"]
rare_tails = ["Cloud", "Feline", "Gator", "Saluki", "Tailless"]
mythic_tails = ["Hook", "Skeletal", "Starchaser", "Scorpivias"]

# common_colours = ["Sand", "Earth", "Rust", "Geode", "Coal"]
# uncommon_colours = ["Harvest Vanilla", "Harvest Cocoa", "Harvest Russet", "Harvest Roast", "Harvest Petal", "Harvest Peach",
#                     "Gem Ink", "Gem Clay", "Gem Desert", "Gem Plum", "Gem Oil",
#                     "Natural Bracco", "Natural Adobe", "Natural Poodle", "Natural Aussie", "Natural Husky", "Natural Boer",
#                     "Dusk Brown", "Dusk Green", "Dusk Blue", "Dusk Red", "Dusk Bronze"]
# rare_colours = ["Quartz Wheat", "Quartz Lunar", "Quartz Slush", "Quartz Ice", "Quartz Amaranth",
#                 "Derecho Squall", "Derecho Wine", "Derecho Clatter", "Derecho Abyss", "Derecho Summer", "Derecho Royal",
#                 "Lush Taffy", "Lush Gummy", "Lush Mint", "Lush Sprinkle", "Lush Razzle"]

colours_with_details = {
    "Sand": (None, "Sand", Rarity.COMMON),
    "Coal": (None, "Coal", Rarity.COMMON),
    "Geode": (None, "Geode", Rarity.COMMON),
    "Rust": (None, "Rust", Rarity.COMMON),
    "Earth": (None, "Earth", Rarity.COMMON),
    "Birch": (None, "Birch", Rarity.COMMON),
    "Lichen": (None, "Lichen", Rarity.COMMON),
    "Pebble": (None, "Pebble", Rarity.COMMON),
    "Hollow": (None, "Hollow", Rarity.COMMON),
    "Brook": (None, "Brook", Rarity.COMMON),
    "Harvest Vanilla": ("Harvest", "Birch", Rarity.UNCOMMON),
    "Harvest Cocoa": ("Harvest", "Sand", Rarity.UNCOMMON),
    "Harvest Russet": ("Harvest", "Rust", Rarity.UNCOMMON),
    "Harvest Roast": ("Harvest", "Rust", Rarity.UNCOMMON),
    "Harvest Petal": ("Harvest", "Pebble", Rarity.UNCOMMON),
    "Harvest Peach": ("Harvest", "Earth", Rarity.UNCOMMON),
    "Gem Ink": ("Gem", "Coal", Rarity.UNCOMMON),
    "Gem Clay": ("Gem", "Earth", Rarity.UNCOMMON),
    "Gem Desert": ("Gem", "Hollow", Rarity.UNCOMMON),
    "Gem Plum": ("Gem", "Geode", Rarity.UNCOMMON),
    "Gem Oil": ("Gem", "Rust", Rarity.UNCOMMON),
    "Natural Bracco": ("Natural", "Rust", Rarity.UNCOMMON),
    "Natural Adobe": ("Natural", "Earth", Rarity.UNCOMMON),
    "Natural Poodle": ("Natural", "Lichen", Rarity.UNCOMMON),
    "Natural Aussie": ("Natural", "Brook", Rarity.UNCOMMON),
    "Natural Husky": ("Natural", "Coal", Rarity.UNCOMMON),
    "Natural Boer": ("Natural", "Coal", Rarity.UNCOMMON),
    "Dusk Brown": ("Dusk", "Rust", Rarity.UNCOMMON),
    "Dusk Green": ("Dusk", "Birch", Rarity.UNCOMMON),
    "Dusk Blue": ("Dusk", "Geode", Rarity.UNCOMMON),
    "Dusk Red": ("Dusk", "Earth", Rarity.UNCOMMON),
    "Dusk Bronze": ("Dusk", "Coal", Rarity.UNCOMMON),
    "Derecho Squall": ("Derecho", "Coal", Rarity.RARE),
    "Derecho Wine": ("Derecho", "Lichen", Rarity.RARE),
    "Derecho Clatter": ("Derecho", "Geode", Rarity.RARE),
    "Derecho Abyss": ("Derecho", "Hollow", Rarity.RARE),
    "Derecho Summer": ("Derecho", "Earth", Rarity.RARE),
    "Derecho Royal": ("Derecho", "Geode", Rarity.RARE),
    "Lush Taffy": ("Lush", "Brook", Rarity.RARE),
    "Lush Gummy": ("Lush", "Hollow", Rarity.RARE),
    "Lush Mint": ("Lush", "Sand", Rarity.RARE),
    "Lush Sprinkle": ("Lush", "Rust", Rarity.RARE),
    "Lush Razzle": ("Lush", "Pebble", Rarity.RARE),
    "Pure Caribbean": ("Pure", "Sand", Rarity.RARE),
    "Pure Cinnamon": ("Pure", "Rust", Rarity.RARE),
    "Pure Drab": ("Pure", "Coal", Rarity.RARE),
    "Pure Moss": ("Pure", "Birch", Rarity.RARE),
    "Pure Sky": ("Pure", "Sand", Rarity.RARE),
    "Pure Slate": ("Pure", "Pebble", Rarity.RARE),
    "Pure Soil": ("Pure", "Earth", Rarity.RARE),
    "Pure Sterling": ("Pure", "Coal", Rarity.RARE),
    "Quartz Wheat": ("Quartz", "Sand", Rarity.RARE),
    "Quartz Lunar": ("Quartz", "Brook", Rarity.RARE),
    "Quartz Slush": ("Quartz", "Lichen", Rarity.RARE),
    "Quartz Ice": ("Quartz", "Coal", Rarity.RARE),
    "Quartz Amaranth": ("Quartz", "Earth", Rarity.RARE),
    "Electric Squash": ("Electric", "Hollow", Rarity.RARE),
    "Electric Persimmon": ("Electric", "Sand", Rarity.RARE),
    "Electric Thistle": ("Electric", "Rust", Rarity.RARE),
    "Electric Morpho": ("Electric", "Pebble", Rarity.RARE),
    "Electric Orchid": ("Electric", "Geode", Rarity.RARE),
    "Electric Ivy": ("Electric", "Coal", Rarity.RARE),

}

common_colours = []
uncommon_colours = []
rare_colours = []
colour_modifier_base_lookup = defaultdict(list)

for colour, details in colours_with_details.items():
    if details[2] == Rarity.COMMON:
        common_colours.append(colour)
    elif details[2] == Rarity.UNCOMMON:
        uncommon_colours.append(colour)
    elif details[2] == Rarity.RARE:
        rare_colours.append(colour)

    mod_base = (details[0], details[1])
    colour_modifier_base_lookup[mod_base].append(colour)


common_horns = []
uncommon_horns = ["Cape Horns", "Hook Horns", "Nub Horns"]
rare_horns = ["Dwarf Horns", "Ram Horns", "Stag Horns", "Unicorn Horn", "Reindeer Horns"]
mythic_horns = ["Astral Horns"]

all_mythic_options = mythic_tails + mythic_gene_modifiers + mythic_vesper_modifiers

all_tails = mythic_tails + rare_tails + uncommon_tails + common_tails
all_colour_mods = mythic_vesper_modifiers
all_gene_modifiers = mythic_gene_modifiers

all_genes = all_mythic_genes + all_rare_genes + all_uncommon_genes + all_common_genes
all_horns = common_horns + uncommon_horns + rare_horns + mythic_horns
all_colours = common_colours + uncommon_colours + rare_colours
all_bases = common_bases + uncommon_bases + rare_bases
all_modifiers = mythic_vesper_modifiers
all_subspecies = ["Bat Eared Pygmy Vesper"]
all_mutations = ["Extra Eyes", "Feathers", "Fins", "Gills", "Quills", "Scales"]
minor_mutations = ["Cheek Pouches", "Heightened Hearing", "Infravision", "Large Whiskers", "Oddly Shaped Tongue", "Poison/Venom Glands", "Raptor Claw", "Secondary Row of Teeth", "Sonar/Echolocation"]


FULL_CHIMERA = "Chimera"
BICOLOUR_CHIMERA = "Bicolor"
all_chimeras = [BICOLOUR_CHIMERA, FULL_CHIMERA]


tails_by_rarity = {}
for tail in mythic_tails:
    tails_by_rarity[tail] = Rarity.MYTHIC
for tail in rare_tails:
    tails_by_rarity[tail] = Rarity.RARE
for tail in uncommon_tails:
    tails_by_rarity[tail] = Rarity.UNCOMMON
for tail in common_tails:
    tails_by_rarity[tail] = Rarity.COMMON
tails_by_rarity["Domestic"] = Rarity.DEFAULT

# Tail families
reptile_tails = ["Hook", "Gator", "Reptile", "Pointed"]
silk_tails = ["None","Saluki", "Silk", "Strand"]
curled_tails = ["None","Cloud", "Curled", "Tufted"]
bobbed_tails = ["None","Feline","Bobbed", "Docked"]

COMMON_PASS_RATE = 40
UNCOMMON_PASS_RATE = 25
MANED_PASS_RATE = 15
RARE_PASS_RATE = 10
MYTHIC_PASS_RATE = 5

# Genetic discovery section. Hush.
genetic_discovery_genes = {
    ("Collared","Flurry"): ("Ruffle", Rarity.COMMON),
    ("Cloak","Comet"): ("Gooey", Rarity.UNCOMMON),
    ("Sable","Underbelly"): ("Melted", Rarity.UNCOMMON),
    ("Barring","Dapple"): ("Snowstorm", Rarity.RARE),
    ("Washed","Merle"): ("Fog", Rarity.RARE),
}
