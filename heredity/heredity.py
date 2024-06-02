import csv
import itertools
import random
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    # people = load_data("data/family0.csv")

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }


    # Loop over all sets of people who might have the trait
    names = set(people)

    for have_trait in powerset(names):
        # Check if current set of people violates known information
        # Only combinations of people where
        #   "True" people are in the set
        #   "False" people are not in the set
        #   In other words, all 'True' people + any combination of 'None" people
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue
        # print("\n~~passed", have_trait)

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)


    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Init probs to 100%, modified by calculated chances
    probability = 1

    # print("\n~~~~~~dataset~~~~~~~~~~~~")
    # print("~~one_gene~~", one_gene)
    # print("~~two_gene~~", two_genes)
    # print("~~have_tra~~", have_trait)

    for person in people:
        # For adhering to PROBS datastructure
        gene_count = 1 if person in one_gene else (2 if person in two_genes else 0)
        trait = True if person in have_trait else False
        
        ###
        # print("\n~before~", person, probability)

        # If no parents, use general probability
        # Note: if a person doesn't have a mother, they don't have a father either
        #   As per distribution code explaination
        if people[person]['mother'] == None:
            general_prob = PROBS['gene'][gene_count]
            probability = probability * general_prob

        # If they have parents
        else:
            mother = people[person]["mother"]
            father = people[person]["father"]
            mom_pass = parent_pass(mother, one_gene, two_genes)
            dad_pass = parent_pass(father, one_gene, two_genes)

            ## Posiibilities for child gene count
            # No parent passed the gene
            if gene_count == 0:
                probability = probability * (1 - mom_pass) * (1 - dad_pass)
            # Either parent passed the gene, but not both
            elif gene_count == 1:
                probability = probability * ((1 - mom_pass) * dad_pass) + (mom_pass * (1 - dad_pass))
            # Both parent passed the gene
            elif gene_count == 2:
                probability = probability * mom_pass * dad_pass

        # Probs that the person is both (gene_count and trait)
        geneXtrait_prob = PROBS["trait"][gene_count][trait]
        probability *= geneXtrait_prob

        ###
        # print("~after~~", person, probability)

    ####
    #print("~final", probability)
    return probability

# Helper function for joint_probability()
def parent_pass(parent, one_gene, two_genes):
    '''calulate probs that parent passed the gene'''
    # 50/50 of passing either gene, both have same chance to mutate into the other
    if parent in one_gene:
        pass_prob = 0.5
    
    # 100% chance to pass the gene, minus chance to mutate into normal
    elif parent in two_genes:
        pass_prob = (1 - PROBS["mutation"])
    
    # 0% chance to pass the gene, plus change to mutate into it
    else: # parent in no_gene
        pass_prob = PROBS["mutation"]
    
    return pass_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    # probabilities = {
    # 'Harry': {'gene': {2: 0, 1: 0, 0: 0}, 'trait': {True: 0, False: 0}}, 
    # 'James': {'gene': {2: 0, 1: 0, 0: 0}, 'trait': {True: 0, False: 0}}, 
    # 'Lily': {'gene': {2: 0, 1: 0, 0: 0}, 'trait': {True: 0, False: 0}}}

    for person in probabilities:
        # Datastructure used in probability{}
        gene_count = 1 if person in one_gene else (2 if person in two_genes else 0)
        trait = True if person in have_trait else False

        probabilities[person]["gene"][gene_count] += p
        probabilities[person]["trait"][trait] += p
    

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    # Per statistics magic, the sum of any person's datatype's values are the same
    val = sum(probabilities[random.choice(list(probabilities.keys()))]['trait'].values())

    for person in probabilities:
        for data in probabilities[person]:
            for possibility in probabilities[person][data]:
                probabilities[person][data][possibility] /= val

    # Not technically needed, since dicts are passed by reference
    # But adding this makes the function's purpose clearer
    return probabilities

if __name__ == "__main__":
    main()
