import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, d):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    N = len(corpus)
    distribution = {}

    # If page has no outgoing links, return uniform distribution over all pages
    if len(corpus[page]) == 0:
        for p in corpus:
            distribution[p] = 1 / N
        return distribution

    # Otherwise, start by giving each page (1 - d)/N
    for p in corpus:
        distribution[p] = (1 - d) / N

    # Then distribute the damping factor among the linked pages
    links = corpus[page]
    for linked_page in links:
        distribution[linked_page] += d / len(links)

    return distribution

def sample_pagerank(corpus, d, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    # Start by choosing a page at random
    page = random.choice(pages)

    counts = {p: 0 for p in pages}
    counts[page] += 1  # The first sample

    # Generate the remaining n - 1 samples
    for _ in range(n - 1):
        # Get transition probabilities from the current page
        probs = transition_model(corpus, page, d)

        # random.choices wants list for population, list for weights
        population = list(probs.keys())
        weights = list(probs.values())

        page = random.choices(population, weights=weights, k=1)[0]
        counts[page] += 1

    # Convert counts to probabilities
    pagerank = {p: counts[p] / n for p in pages}
    return pagerank

def iterate_pagerank(corpus, d):
    N = len(corpus)

    # 1) Preprocess: if a page has no links, treat it as linking to *every* page
    #    Create a new dict that has the "effective" set of links for each page.
    links = {}
    for p in corpus:
        if len(corpus[p]) == 0:
            # No links => pretend it links to *all* pages (including itself)
            links[p] = set(corpus.keys())
        else:
            links[p] = corpus[p]

    # 2) Initialize PR to 1/N
    pagerank = {p: 1 / N for p in corpus}
    

    # 3) Iteratively update
    epsilon = 0.001
    while True:
        newrank = {}
        for p in corpus:
            # (1 - d)/N
            rank = (1 - d) / N

            # Add d * [ sum of PR(i)/NumLinks(i) for i that link to p ]
            # i.e., for every page i that links to p
            s = 0
            for i in corpus:
                if p in links[i]:
                    s += pagerank[i] / len(links[i])

            rank += d * s
            newrank[p] = rank

        # Check convergence across all pages
        diffs = [abs(newrank[p] - pagerank[p]) for p in corpus]
        if max(diffs) < epsilon:
            # If the biggest difference is < epsilon, we can stop
            break

        pagerank = newrank

    # 4) Return the final distribution
    return newrank


if __name__ == "__main__":
    main()
