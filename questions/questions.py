import nltk
import string

import math

import sys
import os


FILE_MATCHES = 1
SENTENCE_MATCHES = 1

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])

    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}

    for file_name in os.listdir(directory):
        print(f"Loading text from: {file_name}")
        file_path = os.path.join(directory, file_name)

        if file_name.endswith(".txt"):
            with open(file_path, "r", encoding='utf-8') as file:
                files[file_name] = file.read()

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Set uses a hash table, which has faster lookup
    stopwords = set(nltk.corpus.stopwords.words("english"))

    tokens = nltk.tokenize.word_tokenize(document.lower())
    words = []

    for token in tokens:
        if token not in stopwords and token not in string.punctuation:
            words.append(token)

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    frequencies = {}

    for word_list in documents:
        uniques = set(documents[word_list])
        for word in uniques:
            if word in frequencies:
                frequencies[word] += 1
            else:
                frequencies[word] = 1
    
    for word in frequencies:
        idf = math.log(len(documents) / frequencies[word])
        frequencies[word] = idf

    return frequencies


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    doc_scores = dict()

    for document, word_list in files.items():

        score = 0
        for token in query:
            count = word_list.count(token)

            # default 0 in case query word does not exist
            tf_idf = count * idfs.get(token, 0)
            score += tf_idf

        doc_scores[document] = score

    sorted_dict = dict(sorted(doc_scores.items(), key=lambda k: k[1], reverse=True))
    rankings = list(key for key in sorted_dict)

    return rankings[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_score = {}

    for id, sentence in sentences.items():

        score = 0
        density = 0
        for word in query:
            if word in sentence:
                score += idfs[word]
                density = sentence.count(word)
        
        density /= len(sentence)
        sentence_score[id] = (score, density)

    sorted_dict = dict(sorted(sentence_score.items(), key=lambda k: k[1], reverse=True))
    rankings = list(key for key in sorted_dict)

    return rankings[:n]



if __name__ == "__main__":
    main()
