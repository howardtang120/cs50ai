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
    # corpus = crawl("corpus2")

    # Sampling data
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    # Iterative pagerank data
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

# Uses Markov chain model
def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Number of pages total, and number of outgoing links in the current page
    total_pages = len(corpus)
    out_links = len(corpus[page])

    # If current page has no outgoing links, choose random from ALL pages
    if out_links == 0:
        page_probability = {key: (1 / total_pages) for key in corpus.keys()}
        return page_probability
    
    # Each outgoing link in current page has the same weight
    page_probability = {key: ((1 - damping_factor) / total_pages) for key in corpus.keys()}
    for link in corpus[page]:
        page_probability[link] += 0.85 / out_links

    return (page_probability)


# Surfer hopping around randomly
def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Choose random page to start, and init dict with '0' values
    location = random.choice(list(corpus.keys()))
    sampled_data = {key: 0 for key in corpus.keys()}

    # Collect 'n' sample data
    for _ in range(n):
        sampled_data[location] += 1

        # Pick the next page based in the weights from transition_model()
        page_probability = transition_model(corpus, location, damping_factor)
        page, probability = list(page_probability.keys()), list(page_probability.values())
        location = random.choices(page, weights=probability)[0]

    # Normalize total sum to 1 
    for key, value in sampled_data.items():
        sampled_data[key] = value / n

    return sampled_data


# Infinite numbers of surfers hopping simultaneously 
# Visual model: https://www.youtube.com/watch?v=JGQe4kiPnrU/reducible
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Init all pages to have the same pagerank, with total sum of 1
    ### Init distribution doesn't matter, as long as sum is 1?
    total_pages = len(corpus)
    temp_data = {key: (1 / total_pages) for key in corpus.keys()}
    count = 0

    while True:
        count += 1
        iterated_data = temp_data.copy()
        # Check inbound links to current page
        for current_page in corpus:
            temp = 0

            # Users in check_page "migrates" to other pages per cycle
            for check_page in corpus:
                if current_page in corpus[check_page]:
                    temp += iterated_data[check_page] / len(corpus[check_page])
                elif len(corpus[check_page]) == 0:
                    temp += iterated_data[check_page] / total_pages
                    
            # 85% migrate through links, 15% jump randomly
            temp *= damping_factor
            temp += (1 - damping_factor) / total_pages
            temp_data[current_page] = temp
        # print(f"\n~~~compare data~~\n{iterated_data}\n{temp_data}")

        # Check for pagerank values convergence
        converge = True
        for keys in iterated_data:
            num = iterated_data[keys] - temp_data[keys]
            if abs(num) > 0.001:
                converge = False
            
        # Convergence is True
        if converge == True:
            print(f"\nIterations until convergence: {count}")
            return iterated_data


if __name__ == "__main__":
    main()
