from collections import Counter
from random import randint
from .item_text_prettification import inventory_update_text, items_to_user_string
from .genes import *

def vesper_roller_factory(generator, rolls):
    if generator == 'Default':
        return DefaultVesper(rolls)
    elif generator == "Max Rarity Based":
        return MaxRarityVesper(rolls)

class VesperRoller:
    def __init__(self, rolls):
        self.rolls = rolls
        self.results = []

    def get_results(self):
        pass

    def pick_items_from_list(self, num, possible_items):
        items = []
        for i in range(0,num):
            rng = randint(1,len(possible_items)) - 1
            item_name = possible_items[rng]
            items.append(item_name)
        return Counter(items)

    def pick_item_from_list(self, possible_items):
        rng = randint(1,len(possible_items)) - 1
        item_name = possible_items[rng]
        return item_name

    def get_sex(self):
        if randint(1, 2) == 1:
            return "Female"
        else:
            return "Male"


class DefaultVesper(VesperRoller):

    def get_results(self):
        for i in range(0, self.rolls):
            result = {"name": "Roll {}".format(i + 1)}

            result["coat"] = "Unknown coat"
            result["sex"] = self.get_sex()
            result["appearance"] = "Unknown appearance"
            result["abnormalities"] = "Unknown abnormalities"
            self.results.append(result)
        return self.results


class MaxRarityVesper(VesperRoller):

    def get_explanation(self):
        return "This randomly selects "

    def get_results(self):
        for i in range(0, self.rolls):
            result = {"name": "Roll {}".format(i + 1)}

            genes = {"rare": 0, "mythic": 0, "common": 0, "uncommon": 0}

            colour = None
            coat = None
            horns = None
            tail = None
            colour_mod = None
            gene_mod = None
            coat_genes = []

            self.get_rare_and_mythic_genes(genes)

            if genes["mythic"] == 1:
                mythic_gene = self.pick_item_from_list(all_mythic_options)
                if mythic_gene in all_tails:
                    tail = mythic_gene + " Tail"
                elif mythic_gene in all_colour_mods:
                    colour_mod = mythic_gene
                elif mythic_gene in all_gene_modifiers:
                    gene_mod = mythic_gene

            get_rare_gene = False
            get_rare_abnormality = False
            if genes["rare"] == 2:
                get_rare_gene = True
                get_rare_abnormality = True

            if get_rare_gene:
                coat_genes.append(self.pick_item_from_list(rare_genes))

            if get_rare_abnormality:
                rare_abnormailty = self.pick_item_from_list(["tail", "colour", "horns"])
                # If you have a mythic tail don't pick a rare one
                if tail:
                    rare_abnormailty = self.pick_item_from_list([ "colour", "horns"])
                # If you have a mythic colour
                if colour_mod:
                    rare_abnormailty = self.pick_item_from_list(["tail", "horns"])

                if rare_abnormailty == "tail":
                    tail = self.pick_item_from_list(rare_tails) + " Tail"
                elif rare_abnormailty == "horns":
                    horns = self.pick_item_from_list(rare_horns)
                elif rare_abnormailty == "colour":
                    colour = self.pick_item_from_list(rare_colours)

            # Fill the rest of the genes in if they're missing

            coat_rng = randint(1,100)
            if coat_rng <= 15:
                coat = self.pick_item_from_list(rare_bases)
            elif coat_rng <= 40:
                coat = self.pick_item_from_list(uncommon_bases)
            else:
                coat = self.pick_item_from_list(common_bases)

            if not tail:
                tail_rng = randint(1,100)
                if tail_rng <= 25:
                    tail = self.pick_item_from_list(uncommon_tails) + " Tail"
                else:
                    tail_type = self.pick_item_from_list(common_tails)
                    if tail_type != "Domestic":
                        tail = tail_type + " Tail"

            if not horns:
                horns_rng = randint(1,100)
                if horns_rng <= 25:
                    horns = self.pick_item_from_list(uncommon_horns)

            if not colour:
                colour_rng = randint(1, 100)
                if colour_rng <= 25:
                    colour = self.pick_item_from_list(uncommon_colours)
                else:
                    colour = self.pick_item_from_list(common_colours)

            abnormailities = None
            if colour_mod or tail or horns:
                if colour_mod and tail and horns:
                    abnormailities = "{} with {} and {}.".format(colour_mod, horns, tail)
                elif colour_mod and tail:
                    abnormailities = "{} with {}.".format(colour_mod, tail)
                elif colour_mod and horns:
                    abnormailities = "{} with {}.".format(colour_mod, horns)
                elif horns and tail:
                    abnormailities = "{} with {}.".format(horns, tail)
                elif colour_mod:
                    abnormailities = "{}.".format(colour_mod)
                elif tail:
                    abnormailities = "{}.".format(tail)
                elif horns:
                    abnormailities = "{}.".format(horns)
            if not abnormailities:
                abnormailities = "None"

            # Now sort out the genes
            gene_count = randint(2,4)
            while len(coat_genes) < gene_count:
                gene_rng = randint(1, 100)
                if gene_rng <= 25:
                    gene = self.pick_item_from_list(uncommon_genes)
                else:
                    gene = self.pick_item_from_list(common_genes)
                if gene not in coat_genes:
                    coat_genes.append(gene)

            if gene_mod:
                mod_gene_num = randint(0,len(coat_genes)-1)
                coat_genes[mod_gene_num] = "{} ({})".format(coat_genes[mod_gene_num], gene_mod)

            last_genes = coat_genes.pop()
            early_genes = ", ".join(coat_genes)
            appearance = "{} and {} on {}".format(early_genes, last_genes, colour)

            result["coat"] = coat
            result["sex"] = self.get_sex()
            result["appearance"] = appearance
            result["abnormalities"] = abnormailities
            self.results.append(result)
        return self.results

    def get_rare_and_mythic_genes(self, genes):
        rng = randint(1,100)
        if rng <= 5:
            genes["mythic"] += 1
            genes["rare"] += 1
        elif rng <= 10:
            genes["mythic"] += 1
        elif rng <= 20:
            genes["rare"] += 2
        elif rng <= 35:
            genes["rare"] += 1
