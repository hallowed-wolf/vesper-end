from random import randint, choice, shuffle
from .genes import *
from dataclasses import dataclass
from typing import List, Dict, Set
from collections import Counter

from enum import Enum

@dataclass
class BreedingVesper:
    """Class for keeping track of a vesper which is being bred."""
    name: str
    colour: str
    horns: str
    tail: str
    base: str
    modifier: str
    subspecies: str
    mutation: str
    chimera_status: str
    chimera_colour: str
    genes: List[str]

    @staticmethod
    def factory(data: Dict[str, str], name: str) -> 'BreedingVesper':
        vesper_genes: List[str] = []
        for gene_num in range(1, 11):
            potential_gene = data[f"{name}gene{gene_num}"]
            if potential_gene != "None":
                vesper_genes.append(potential_gene)

        vesper = BreedingVesper(name = name,
                                colour = data[f"{name}coatcolour"],
                                horns = data[f"{name}horns"],
                                tail = data[f"{name}tail"],
                                base = data[f"{name}base"],
                                modifier = data[f"{name}mod"],
                                subspecies = data[f"{name}species"],
                                mutation = data[f"{name}mut"],
                                chimera_status = data[f"{name}chimera"],
                                chimera_colour=data[f"{name}chimeracolour"],
                                genes = vesper_genes
                                )
        return vesper

    def populate_data(self, data: Dict):
        for num, gene in enumerate(self.genes):
            data[f"{self.name}gene{num+1}_value"] = gene

        data[f"{self.name}coatcolour_value"] = self.colour
        data[f"{self.name}horns_value"] = self.horns
        data[f"{self.name}tail_value"] = self.tail
        data[f"{self.name}base_value"] = self.base
        data[f"{self.name}mod_value"] = self.modifier
        data[f"{self.name}species_value"] = self.subspecies
        data[f"{self.name}mut_value"] = self.mutation
        data[f"{self.name}chimera_value"] = self.chimera_status
        data[f"{self.name}chimeracolour_value"] = self.chimera_colour

@dataclass
class Puppy:
    name: str
    health: str
    sex: str
    colour: str
    horns: str
    tail: str
    base: str
    modifier: str
    subspecies: str
    major_mutations: List[str]
    minor_mutation: str
    chimera_status: str
    chimera_colour: str
    genes: List[str]
    chimera_genes: List[str]

    def __init__(self, name):
        self.name = name

    def format_genes(self, genes: List[str]) -> str:
        if len(genes) == 0:
            genes = ["None"]
        elif len(genes) > 1:
            genes = sorted(genes)
            last_gene = genes.pop(-1)
            genes[-1] = "{} and {}".format(genes[-1], last_gene)
        gene_string = ", ".join(genes)
        return gene_string

    @property
    def all_genes(self) -> List[str]:
        return self.genes + self.chimera_genes

    @property
    def appearance(self) -> str:
        if self.chimera_status == "None":
            return f"{self.format_genes(self.genes)} on {self.colour}"
        elif self.chimera_status == BICOLOUR_CHIMERA:
            return f"{self.format_genes(self.genes)} on {self.colour} // {self.chimera_colour}"
        elif self.chimera_status == FULL_CHIMERA:
            return f"{self.format_genes(self.genes)} on {self.colour} // {self.format_genes(self.chimera_genes)} on {self.chimera_colour}"

    @property
    def abnormalities(self) -> str:
        abnormalities_list = []
        if self.modifier and self.modifier != "None":
            abnormalities_list.append(self.modifier)

        if self.horns and self.horns != "None":
            abnormalities_list.append(self.horns)

        if self.tail and self.tail != "Domestic Tail":
            abnormalities_list.append(self.tail)

        if self.chimera_status and self.chimera_status != "None":
            abnormalities_list.append(self.chimera_status)

        # Get the list of mutations - probably just one, but there's the chance for spontaneous occurrence

        abnormalities_list.extend(self.major_mutations)

        # Decide how to present them - if no abnormalities put none.
        if len(abnormalities_list) > 3:
            # Do stuff to make it 3
            start = abnormalities_list[0]
            end = abnormalities_list[-1]
            middle = ", ".join(abnormalities_list[1:-1])
            abnormalities_list = [start, middle, end]

        if len(abnormalities_list) == 3:
            abnormalities = "{} with {} and {}".format(*abnormalities_list)
        elif len(abnormalities_list) == 2:
            abnormalities = "{} with {}".format(*abnormalities_list)
        elif len(abnormalities_list) == 1:
            abnormalities = "{}".format(*abnormalities_list)
        else:
            abnormalities = "None"
        return abnormalities

    @property
    def dictionary_form(self):
        dictionary_form = {
            "Name": self.name,
            "Health": self.health,
            "Subspecies": self.subspecies,
            "Base": self.base,
            "Sex": self.sex,
            "Appearance": self.appearance,
            "Abnormalities": self.abnormalities,
            "MinorMutation": self.minor_mutation,
        }
        return dictionary_form


class BreedingRoller:
    def __init__(self, vespers: List[BreedingVesper], modifiers, password_valid=False, is_test=False):
        #Vespers were [{'Colour': 'Sand', 'Horns': 'None', 'Tail': 'Hook', 'Base': 'Maned', 'Genes': []}, {'Colour': 'Sand', 'Horns': 'None', 'Tail': 'Hook', 'Base': 'Maned', 'Genes': []}]
        #                                "Subspecies": data["{}species".format(id)],
        #                        "Mutation": data["{}mut".format(id)],
        #Boosts were {'MaleBoost': False, 'FemaleBoost': False, 'Alpha': False, 'SpringBlessing': False, 'Bonded': False, 'VirusReduction': 0, 'Inbred': 0}
        self.sire = vespers[0]
        self.dam = vespers[1]
        self.modifiers = modifiers
        self.comments = []
        self.puppies = []
        self.puppies_class_format = []
        self.all_male = False
        self.all_female = False
        self.gene_boost = 0
        self.genetic_discovery = password_valid
        self.is_test = is_test

    def roll_breeding(self):
        # Check there aren't any duplicate genes - this is the only
        if len(set(self.sire.genes)) < len(self.sire.genes):
            self.comments.append("THIS BREEDING IS NOT VALID! The same gene has been entered more than once for the sire.")
            return
        if len(set(self.dam.genes)) < len(self.dam.genes):
            self.comments.append("THIS BREEDING IS NOT VALID! The same gene has been entered more than once for the dam.")
            return
        if self.modifiers["VirusReduction"] < 0:
            self.comments.append("THIS BREEDING IS NOT VALID! Negative virus reduction is not possible")
            return
        if self.modifiers["Inbred"] < 0:
            self.comments.append("THIS BREEDING IS NOT VALID! Negative shared ancestors are not possible")
            return

        num_cubs = self.get_number_cubs()

        if self.modifiers['MaleBoost'] and self.modifiers['FemaleBoost']:
            self.comments.append("You applied two different gender boosters to this litter, neither can activate")
        elif (randint(1,100) < 81) and self.modifiers['MaleBoost']:
            self.comments.append("Your oak twig activated, the litter will be all male")
            self.all_male = True
        elif (randint(1,100) < 81) and self.modifiers['FemaleBoost']:
            self.comments.append("Your willow sprig activated, the litter will be all female")
            self.all_female = True

        if self.modifiers["Bonded"]:
            self.gene_boost += 5

        for cub in range(num_cubs):
            #Pup 1
            #Stillborn
            #Coat Type: Smooth
            #Sex: Male
            #Appearance: Points and Mask on Coal.
            #Abnormalities: Docked Tail.
            pup = self.get_puppy(cub+1)

            self.puppies.append(pup.dictionary_form)
            self.puppies_class_format.append(pup)

        # This is a bit hacky, but the last, spring blessing cub, should always be alive, so set that retroactively.
        if self.modifiers["SpringBlessing"]:
            blessed_cub = self.puppies[-1]
            if self.modifiers["Inbred"]:
                blessed_cub["Health"] += "MANUALLY ADJUST - Inbred but should be alive"
            else:
                blessed_cub["Health"] = "Healthy"

        if self.is_test:
            self.perform_test()

    def perform_test(self):
        iterations = 10000
        pups_counter = Counter()
        for iter in range(iterations):
            pups_counter[self.get_number_cubs()] += 1

        pup_distribution = []
        for num, count in pups_counter.items():
            pup_distribution.append((num, f"{100*count/iterations:.2f}%",count))
        pup_distribution.sort(key=lambda x: x[2], reverse=True)

        pup_dist_str = ""
        for num, percentage, count in pup_distribution:
            pup_dist_str += f"{num} pups: {percentage} "

        self.comments.append(f"Number of pups per litter averaged over {iterations} litters is")
        self.comments.append(f"{pup_dist_str}")

        health_counter = Counter()
        sex_counter = Counter()
        colours_counter = Counter()
        horns_counter = Counter()
        tail_counter = Counter()
        base_counter = Counter()
        modifier_counter = Counter()
        subspecies_counter = Counter()
        major_mutation_counter = Counter()
        minor_mutation_counter = Counter()
        chimera_counter = Counter()
        genes_counter = Counter()
        num_gene_counter = Counter()

        all_counters = {
            "Health": health_counter,
            "Sex": sex_counter,
            "Base colours": colours_counter,
            "Horns": horns_counter,
            "Tails": tail_counter,
            "Coat Type": base_counter,
            "Modifier": modifier_counter,
            "Subspecies": subspecies_counter,
            "Major Mutations": major_mutation_counter,
            "Minor Mutations": minor_mutation_counter,
            "Chimera": chimera_counter,
            "Genes": genes_counter,
            "Total number of genes": num_gene_counter
        }

        for iter in range(iterations):
            puppy = self.get_puppy(iter)
            health_counter[puppy.health] += 1
            sex_counter[puppy.sex] += 1
            colours_counter[puppy.colour] += 1
            horns_counter[puppy.horns] +=1
            tail_counter[puppy.tail] += 1
            base_counter[puppy.base] += 1
            modifier_counter[puppy.modifier] += 1
            subspecies_counter[puppy.subspecies] += 1
            if len(puppy.major_mutations) == 0:
                major_mutation_counter["None"] += 1
            for mut in puppy.major_mutations:
                major_mutation_counter[mut] += 1
            minor_mutation_counter[puppy.minor_mutation] +=1
            chimera_counter[puppy.chimera_status] += 1
            gene_count = 0
            for gene in puppy.genes:
                genes_counter[gene] += 1
                gene_count += 1
            if puppy.chimera_status == FULL_CHIMERA:
                for gene in puppy.chimera_genes:
                    genes_counter[gene] += 1
                    gene_count += 1
            num_gene_counter[gene_count] += 1

        self.comments.append(f"Test rolling {iterations} puppies we got the following results.")
        for counter_name, counter in all_counters.items():
            if counter_name in ["Genes", "Major Mutations"]:
                total = iterations
            else:
                total = sum(counter.values())
            distribution = []
            for num, count in counter.items():
                distribution.append((num, f"{100*count/total:.2f}%", count))
            distribution.sort(key=lambda x: x[2], reverse=True)
            distribution_string = ""
            for value, percentage, count in distribution:
                distribution_string += f"{value}: {percentage} "
            self.comments.append(f"{counter_name} occurrence is {distribution_string}")


    def get_puppy(self, number):
        pup = Puppy(f"Pup {number}")
        if self.all_male:
            pup.sex = "Male"
        elif self.all_female:
            pup.sex = "Female"
        elif (randint(1, 100) < 51):
            pup.sex = "Male"
        else:
            pup.sex = "Female"
        pup.health = self.get_health()

        # Sort out chimera first, as this affects a lot.
        pup.chimera_status = self.get_chimera()
        pup.colour = self.get_colour()
        if pup.chimera_status in [BICOLOUR_CHIMERA, FULL_CHIMERA]:
            pup.chimera_colour = self.get_colour()

        if pup.chimera_status == FULL_CHIMERA:
            pup.genes = self.get_genes(max=5)
            pup.chimera_genes = self.get_genes(max=5)
        else:
            pup.genes = self.get_genes()

        # Get horns
        pup.horns = self.get_horns()
        # Get tail
        tail = self.get_tail()
        pup.tail = "{} Tail".format(tail)
        pup.modifier = self.get_modifier()

        pup.base = self.get_base()
        pup.subspecies = self.get_species()

        # Fix base for pygmies - they can't be woolen or maned
        if pup.subspecies == "Bat Eared Pygmy Vesper" and pup.base == "Woolen":
            pup.base = "Smooth"
        pup.major_mutations = self.get_major_mutations()
        pup.minor_mutation = self.get_minor_mutation()
        return pup

    def get_colour(self):
        possible_colours = []
        possible_colours.append(self.sire.colour)
        if self.sire.chimera_status in all_chimeras:
            possible_colours.append(self.sire.chimera_colour)
        possible_colours.append(self.dam.colour)
        if self.dam.chimera_status in all_chimeras:
            possible_colours.append(self.dam.chimera_colour)

        # Which base colour do we have? Pick one at random.
        shuffle(possible_colours)
        base = colours_with_details[possible_colours[0]][1]

        # colour_modifier_base_lookup - for at the end
        # colours_with_details
        # "Quartz Amaranth": ("Quartz", "Earth", Rarity.RARE)
        # What modifier, if any, is inherited?
        possible_mods = []
        for colour in possible_colours:
            possible_mods.append((colours_with_details[colour][0], colours_with_details[colour][2]))
        passed_mods = []
        for mod in possible_mods:
            if self.get_does_mod_pass(mod[0], mod[1]):
                passed_mods.append(mod)

        if len(passed_mods) == 0:
            mod = None
        elif len(passed_mods) == 1:
            mod = passed_mods[0][0]
        else:
            # Find what is the rarity of the rarest mod passed
            max_rarity_value = max([mod[1].value for mod in passed_mods])
            # Get all the mods with that rarity
            rarest_mods = []
            for mod in passed_mods:
                if mod[1].value == max_rarity_value:
                    rarest_mods.append(mod[0])
            # Pick one at random
            shuffle(rarest_mods)
            mod = rarest_mods[0]

        # What does base + modifier give?
        key = (mod, base)
        if key not in colour_modifier_base_lookup:
            return base
        else:
            possible_colours = colour_modifier_base_lookup[key]
            return choice(possible_colours)

    def get_does_mod_pass(self, mod, rarity):
        if mod == None:
            return False

        pass_rate = 0
        if rarity == Rarity.RARE:
            pass_rate = RARE_PASS_RATE + self.gene_boost
        elif rarity == Rarity.UNCOMMON:
            pass_rate = UNCOMMON_PASS_RATE + self.gene_boost
        if randint(1, 100) <= pass_rate:
            return True
        else:
            return False

    def get_genes(self, max=10):
        siregenes = self.sire.genes
        damgenes = self.dam.genes
        allpossiblegenes = list(siregenes) + list(damgenes)
        output_genes = []
        for gene in allpossiblegenes:
            if self.get_does_gene_pass(gene, self.get_gene_rarity(gene)):
                output_genes.append(gene)

        # Add stardust if we have a chance for it
        if self.modifiers["Stardust"]:
            rng = randint(1,100)
            if rng <= self.modifiers["Stardust"]:
                output_genes.append("Stardust")

        # Also genetic discovery genes - but only if the password is valid
        if self.genetic_discovery:
            # Genetic discovery section. Hush.
            for parent_genes, child_gene in genetic_discovery_genes.items():
                one, two = parent_genes
                gene, rarity = child_gene
                if (((one in siregenes) and (two in damgenes)) or
                    ((two in siregenes) and (one in damgenes))):
                    # Discovery possible
                    if self.get_does_gene_pass(gene,rarity):
                        output_genes.append(gene)

        # Remove duplicates by transforming into set
        final_genes = list(set(output_genes))

        # Get rid of any genes above threshold
        if len(final_genes) > max:
            self.trim_genes(final_genes, max)

        # So theoretically we need to restrict colour modifiers, but I figure the user can deal with it if it ever happens
        # given they're mythic.
        if "Gleam" in final_genes:
            final_genes.remove("Gleam")
            gleam_genes = final_genes.copy()
            for gene in freecolour_genes:
                if gene in gleam_genes:
                    gleam_genes.remove(gene)
            if len(gleam_genes) > 0:
                random_gene_num = randint(0, len(gleam_genes)-1)
                random_gene_value = gleam_genes[random_gene_num]
                random_gene_index = final_genes.index(random_gene_value)
                final_genes[random_gene_index] = "{} (Gleam)".format(final_genes[random_gene_index])
            else:
                # Nothing we could sensibly attach to, add gleam unassigned.
                final_genes.append("Gleam")

        return final_genes

    def trim_genes(self, gene_list, max_genes):
        rarity_order = [Rarity.COMMON, Rarity.UNCOMMON, Rarity.RARE, Rarity.MYTHIC]
        for rarity in rarity_order:
            rarity_genes = []
            for gene in gene_list:
                if self.get_gene_rarity(gene) == rarity:
                    rarity_genes.append(gene)
            shuffle(rarity_genes)
            for gene in rarity_genes:
                if len(gene_list) <= max_genes:
                    return
                gene_list.remove(gene)

    def get_gene_rarity(self, gene):
            if gene in all_mythic_genes:
                return Rarity.MYTHIC
            elif gene in all_rare_genes:
                return Rarity.RARE
            elif gene in all_uncommon_genes:
                return Rarity.UNCOMMON
            elif gene in all_common_genes:
                return Rarity.COMMON


    def get_does_gene_pass(self, gene, rarity):
        pass_rate = 0
        if rarity == Rarity.MYTHIC:
            pass_rate = MYTHIC_PASS_RATE + self.gene_boost
        elif rarity == Rarity.RARE:
            pass_rate = RARE_PASS_RATE + self.gene_boost
        elif rarity == Rarity.UNCOMMON:
            pass_rate = UNCOMMON_PASS_RATE + self.gene_boost
        elif rarity == Rarity.COMMON:
            pass_rate = COMMON_PASS_RATE + self.gene_boost
        if randint(1, 100) <= pass_rate:
            return True
        else:
            return False

    def get_species(self):
        sirespecies = self.sire.subspecies
        damspecies = self.dam.subspecies
        if (sirespecies == "None") and (damspecies == "None"):
            return "None"
        elif sirespecies == "Bat Eared Pygmy Vesper" and damspecies == "Bat Eared Pygmy Vesper":
            return "Bat Eared Pygmy Vesper"
        else:
            # Two different species, randomise
            rng = randint(1,100)
            if rng <= 25:
                return "Bat Eared Pygmy Vesper"
            else:
                return "None"

    def get_major_mutations(self):
        siremut = self.sire.mutation
        dammut = self.dam.mutation
        mutations = set()
        if siremut != "None":
            if randint(1,100) <= 3:
                mutations.add(siremut + " Mutation")
        if dammut != "None":
            if randint(1,100) <= 3:
                mutations.add(dammut + " Mutation")
        # random major mutation
        if randint(1,100) <= 1:
            mutations.add(choice(all_mutations) + " Mutation")
        return list(mutations)

    def get_minor_mutation(self):
        if randint(1,100) <= 1:
            return choice(minor_mutations)
        return "None"

    def get_base(self):
        sirebase = self.sire.base
        dambase = self.dam.base
        sire_passed, sire_rarity = self.get_passed_base(sirebase)
        dam_passed, dam_rarity = self.get_passed_base(dambase)
        base = "Error"
        if sire_passed and dam_passed:
            if sire_rarity.value > dam_rarity.value:
                base = sirebase
            elif dam_rarity.value > sire_rarity.value:
                base = dambase
            else:
                base = sirebase if (randint(1,2) == 1) else dambase
        elif sire_passed:
            base = sirebase
        elif dam_passed:
            base = dambase
        else:
            base = "Smooth"
        return base

    def get_passed_base(self, base):
        pass_rate = 0
        rarity = Rarity.COMMON
        if base in rare_bases:
            # Rare coat = 15% pass rate
            pass_rate = MANED_PASS_RATE + self.gene_boost
            rarity = Rarity.RARE
        elif base in uncommon_bases:
            pass_rate = UNCOMMON_PASS_RATE + self.gene_boost
            rarity = Rarity.UNCOMMON
        elif base in common_bases:
            pass_rate = COMMON_PASS_RATE + self.gene_boost
            rarity = Rarity.COMMON
        if randint(1,100) <= pass_rate:
            return True, rarity
        else:
            return False, rarity

    def get_modifier(self):
        siremod = self.sire.modifier
        dammod = self.dam.modifier
        sire_passed, sire_rarity = self.get_passed_modifier(siremod)
        dam_passed, dam_rarity = self.get_passed_modifier(dammod)
        mod = "Error"
        if sire_passed and dam_passed:
            if sire_rarity.value > dam_rarity.value:
                mod = siremod
            elif dam_rarity.value > sire_rarity.value:
                mod = dammod
            else:
                mod = siremod if (randint(1, 2) == 1) else dammod
        elif sire_passed:
            mod = siremod
        elif dam_passed:
            mod = dammod
        else:
            mod = "None"
        return mod

    def get_passed_modifier(self, modifier):
        if modifier == "None":
            return False, Rarity.COMMON
        pass_rate = MYTHIC_PASS_RATE + self.gene_boost
        rarity = Rarity.MYTHIC

        if pass_rate and randint(1,100) <= pass_rate:
            return True, rarity
        else:
            return False, Rarity.COMMON


    def get_horns(self):
        sirehorns = self.sire.horns
        damhorns = self.dam.horns
        sire_passed, sire_rarity = self.get_passed_horns(sirehorns)
        dam_passed, dam_rarity = self.get_passed_horns(damhorns)
        horns = "Error"
        if sire_passed and dam_passed:
            if sire_rarity.value > dam_rarity.value:
                horns = sirehorns
            elif dam_rarity.value > sire_rarity.value:
                horns = damhorns
            else:
                horns = sirehorns if (randint(1,2) == 1) else damhorns
        elif sire_passed:
            horns = sirehorns
        elif dam_passed:
            horns = damhorns
        else:
            horns = "None"
        return horns

    def get_passed_horns(self, horns):
        pass_rate = 0
        rarity = Rarity.COMMON
        if horns in mythic_horns:
            pass_rate = MYTHIC_PASS_RATE + self.gene_boost
            rarity = Rarity.MYTHIC
        if horns in rare_horns:
            pass_rate = RARE_PASS_RATE + self.gene_boost
            rarity = Rarity.RARE
        elif horns in uncommon_horns:
            pass_rate = UNCOMMON_PASS_RATE + self.gene_boost
            rarity = Rarity.UNCOMMON

        if pass_rate and randint(1,100) <= pass_rate:
            return True, rarity
        else:
            return False, Rarity.COMMON

    def get_tail(self):
        siretail = self.sire.tail
        damtail = self.dam.tail
        sire_passed, sire_rarity = self.get_passed_tail(siretail)
        dam_passed, dam_rarity = self.get_passed_tail(damtail)

        if sire_rarity.value > dam_rarity.value:
            tail = sire_passed
        elif dam_rarity.value > sire_rarity.value:
            tail = dam_passed
        else:
            tail = sire_passed if (randint(1,2) == 1) else dam_passed

        return tail


    def get_passed_tail(self, tail):
        if tail == "Domestic":
            return "Domestic", Rarity.DEFAULT

        if tail in ["Skeletal", "Starchaser", "Scorpivias"]:
            roll = randint(1,100)
            if roll <= (MYTHIC_PASS_RATE + self.gene_boost):
                return tail, Rarity.MYTHIC
            elif roll <= (RARE_PASS_RATE + self.gene_boost):
                return choice(rare_tails), Rarity.RARE
            elif roll <= (UNCOMMON_PASS_RATE + self.gene_boost):
                return choice(uncommon_tails), Rarity.UNCOMMON
            elif roll <= (COMMON_PASS_RATE + self.gene_boost):
                return choice(common_tails), Rarity.COMMON
            else:
                return "Domestic", Rarity.DEFAULT

        # Tailless is a rare tail which can go to anything else if it would be uncommon or below.
        if tail in ["Tailless"]:
            roll = randint(1,100)
            if roll <= (MYTHIC_PASS_RATE + self.gene_boost):
                return tail, Rarity.MYTHIC
            elif roll <= (RARE_PASS_RATE + self.gene_boost):
                return choice(rare_tails), Rarity.RARE
            elif roll <= (UNCOMMON_PASS_RATE + self.gene_boost):
                return choice(uncommon_tails), Rarity.UNCOMMON
            elif roll <= (COMMON_PASS_RATE + self.gene_boost):
                return choice(common_tails), Rarity.COMMON
            else:
                return "Domestic", Rarity.DEFAULT

        # Dealt with skeletal, the rest of the tails now all follow the same pattern - we can inherit a tail which is
        # from the same family as the one we started with and the same or lower rarity.
        tail_rarity = tails_by_rarity[tail]

        # Get the tails of the appropriate family
        tail_family = None
        if tail in reptile_tails:
            tail_family = reptile_tails
        elif tail in silk_tails:
            tail_family = silk_tails
        elif tail in curled_tails:
            tail_family = curled_tails
        elif tail in bobbed_tails:
            tail_family = bobbed_tails

        roll = randint(1,100)

        if (tail_rarity.value >= Rarity.MYTHIC.value) and (roll <= (MYTHIC_PASS_RATE + self.gene_boost)):
            return tail_family[0], Rarity.MYTHIC
        if (tail_rarity.value >= Rarity.RARE.value) and (roll <= (RARE_PASS_RATE + self.gene_boost)):
            return tail_family[1], Rarity.RARE
        if (tail_rarity.value >= Rarity.UNCOMMON.value) and (roll <= (UNCOMMON_PASS_RATE + self.gene_boost)):
            return tail_family[2], Rarity.UNCOMMON
        if (tail_rarity.value >= Rarity.COMMON.value) and (roll <= (COMMON_PASS_RATE + self.gene_boost)):
            return tail_family[3], Rarity.COMMON
        return "Domestic", Rarity.DEFAULT

    def get_chimera(self):
        sirechimera = self.sire.chimera_status
        damchimera = self.dam.chimera_status
        sire_passed, sire_rarity = self.get_passed_chimera(sirechimera)
        dam_passed, dam_rarity = self.get_passed_chimera(damchimera)

        if sire_rarity.value > dam_rarity.value:
            chimera = sire_passed
        elif dam_rarity.value > sire_rarity.value:
            chimera = dam_passed
        else:
            chimera = sire_passed if (randint(1,2) == 1) else dam_passed

        return chimera

    def get_passed_chimera(self, chimera):
        roll = randint(1, 100)
        if chimera == "None":
            return "None", Rarity.DEFAULT
        elif chimera == BICOLOUR_CHIMERA:
            if roll <= (RARE_PASS_RATE + self.gene_boost):
                return BICOLOUR_CHIMERA, Rarity.RARE
        elif chimera == FULL_CHIMERA:
            if roll <= (MYTHIC_PASS_RATE + self.gene_boost):
                return FULL_CHIMERA, Rarity.MYTHIC
        return "None", Rarity.DEFAULT

    def get_health(self):
        health = []

        virus_chance = 50
        virus_reduction = self.modifiers["VirusReduction"]
        if self.modifiers["Bonded"]:
            virus_reduction += 20

        virus_chance = max(0, virus_chance - virus_reduction)

        inbred = self.modifiers["Inbred"]

        if inbred:
            stillborn_chance = 80 + 5*(inbred -1)
            sterile_chance = 80 + 5*(inbred -1)
            blind_chance = 80 + 5*(inbred -1)
            deaf_chance = 80 + 5*(inbred -1)
            dystonia_chance = 60 + 5*(inbred -1)
            hemophilia_chance = 60 + 5*(inbred -1)

            if randint(1,100) <= stillborn_chance or randint(1,100) <= virus_chance:
                health.append("Stillborn")
            if randint(1,100) <= sterile_chance:
                health.append("Sterile")
            if randint(1,100) <= blind_chance:
                health.append("Blind")
            if randint(1,100) <= deaf_chance:
                health.append("Deaf")
            if randint(1,100) <= dystonia_chance:
                health.append("Dystonia")
            if randint(1,100) <= hemophilia_chance:
                health.append("Hemophilia")
        else:
            if randint(1,100) <= virus_chance:
                health.append("Stillborn")

        if not health:
            health_string = "Healthy"
        else:
            health_string = ", ".join(health)
        return health_string

    def get_number_cubs(self):
        cub_rng = randint(1,100)
        if self.modifiers["SomnisBlessing"]:
            if cub_rng < 11:
                num_cubs = 6
            elif cub_rng < 21:
                num_cubs = 5
            elif cub_rng < 31:
                num_cubs = 4
            elif cub_rng < 71:
                num_cubs = 3
            else:
                num_cubs = 2
        else:
            if cub_rng < 11:
                num_cubs = 4
            elif cub_rng < 21:
                num_cubs = 3
            elif cub_rng < 61:
                num_cubs = 2
            else:
                num_cubs = 1
        if self.modifiers["SpringBlessing"]:
            num_cubs = randint(3,6)
        if self.modifiers["Alpha"]:
            if randint(1,100) < 11:
                num_cubs += 1
                self.comments.append("Alpha's Blessing activated. An extra pup has been born!")
        if self.modifiers["Bonded"]:
            if randint(1,100) < 11:
                num_cubs += 1
                self.comments.append("Due to your pair's bond an extra pup has been born!")
        return num_cubs