import csv
import itertools
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
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

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

def get_gene_count(person, one_gene, two_genes):
    """
    Returns the number of gene copies for a person based on the sets one_gene and two_genes.
    """
    if person in two_genes:
        return 2
    elif person in one_gene:
        return 1
    else:
        return 0

def gene_pass_probability(gene_count):
    """
    Returns the probability that a person with a given gene_count passes on the mutated gene.
    """
    if gene_count == 2:
        return 1 - PROBS["mutation"]
    elif gene_count == 1:
        return 0.5
    else:  # gene_count == 0
        return PROBS["mutation"]

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_genes` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set `have_trait` does not have the trait.
    """
    
    probability = 1.0

    for person in people:
        # Determine the gene count and trait status for this person.
        gene_count = get_gene_count(person, one_gene, two_genes)
        has_trait = person in have_trait

        # Check if person has no parental information.
        if people[person]["mother"] is None or people[person]["father"] is None:
            gene_prob = PROBS["gene"][gene_count]
        else:
            # Get the names of the parents.
            mother = people[person]["mother"]
            father = people[person]["father"]

            # Get each parent's gene count.
            mother_genes = get_gene_count(mother, one_gene, two_genes)
            father_genes = get_gene_count(father, one_gene, two_genes)

            # Get the probability each parent passes on the mutated gene.
            mother_pass = gene_pass_probability(mother_genes)
            father_pass = gene_pass_probability(father_genes)

            # Calculate gene_prob based on the child's gene count.
            if gene_count == 2:
                gene_prob = mother_pass * father_pass
            elif gene_count == 1:
                gene_prob = mother_pass * (1 - father_pass) + (1 - mother_pass) * father_pass
            else:  # gene_count == 0
                gene_prob = (1 - mother_pass) * (1 - father_pass)

        # Get the probability of the trait given the gene count.
        trait_prob = PROBS["trait"][gene_count][has_trait]

        # Multiply the probability for this person into the overall joint probability.
        probability *= gene_prob * trait_prob

    return probability

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `one_gene` and `have_trait`, respectively.
    """
    for person in probabilities:

        gene = get_gene_count(person, one_gene, two_genes)

        # Update the gene probability distribution.
        probabilities[person]["gene"][gene] += p

        # Determine trait status: True if the person is in have_trait, otherwise False.
        trait = person in have_trait

        # Update the trait probability distribution.
        probabilities[person]["trait"][trait] += p



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        gene_map = probabilities[person]["gene"]
        trait_map = probabilities[person]["trait"]

        gene_prob_sum = sum(gene_map.values())
        trait_prob_sum = sum(trait_map.values())

        probabilities[person]["gene"] = {
            gene: prob / gene_prob_sum for gene, prob in gene_map.items()
        }
        probabilities[person]["trait"] = {
            trait: prob / trait_prob_sum for trait, prob in trait_map.items()
        }

if __name__ == "__main__":
    main()
