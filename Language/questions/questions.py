import nltk
import sys
import os
import string 
import math
from collections import Counter

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
    contents = {}
    for filename in os.listdir(directory):
        # print(os.path.join(directory, filename))
        f = open(os.path.join(directory, filename), "r")
        contents[filename] = f.read().replace('\n', '')
        f.close
    return contents
#    raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Extract words
    contents = [
        word.lower() for word in
        nltk.word_tokenize(document)
        # if word.isalpha()
    ]
    checklist = nltk.corpus.stopwords.words("english") + list(string.punctuation) + ["==", "====", "=====", "======", "''", "``"]
    for bad_entry in checklist:
        try:
            while True:
                contents.remove(bad_entry)
        except ValueError:
            pass

    # print(contents)
    # input()
    return contents
#    raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = {}
    for document in documents.keys():
        for word in set(documents[document]):
            try:
                idfs[word] += 1
            except:
                idfs[word] = 1
    for word in idfs.keys():
        idfs[word] = math.log(len(documents)/idfs[word])
    # print(idfs)
    # input()
    return idfs
    # raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_scores = {}
    for source in files:
        file_scores[source] = 0
        wordcount = Counter(files[source])
        for word in query:
            if(word in files[source]):
                file_scores[source] += wordcount[word]*idfs[word]
                # print(word)
                # print(wordcount[word])
                # print(idfs[word])
                # print(file_scores)
                # input()
    sorted_score =  sorted(file_scores.items(), key=lambda x: x[1], reverse=True)
    final_list = []
    # print(sorted_score)
    # input()
    for i in range(n):
        final_list.append(sorted_score[i][0])
    # print(final_list)
    # input()
    return final_list
    # raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_scores = {}
    for sentence in sentences:
        sentence_scores[sentence] = (0, 0) #idfs, word_count -> word_density later
        for word in query:
            if(word in tokenize(sentence)):
                sentence_scores[sentence] = (sentence_scores[sentence][0] + idfs[word], sentence_scores[sentence][1] + 1)
            sentence_scores[sentence] = (sentence_scores[sentence][0], sentence_scores[sentence][1]/len(sentence))

    sorted_score =  sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    final_list = []
    # print(sorted_score)
    # input()
    for i in range(n):
        final_list.append(sorted_score[i][0])
    # print(final_list)
    # input()
    return final_list
    # raise NotImplementedError


if __name__ == "__main__":
    main()
