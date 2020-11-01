import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP
NP -> N | Det N |  AdjP N | Det AdjP N | N PP | N Adv
VP -> V | VP NP | V NP PP | VP PP | Adv V | VP Adv
PP -> P | P NP | PP PP
AdjP -> Adj | Adj AdjP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    print(sentence)
    # Extract words
    contents = [
        word.lower() for word in
        nltk.word_tokenize(sentence)
        if word.isalpha()
    ]
    print(contents)
    return contents
    # raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    contents = []
    for subtree in tree.subtrees():
        if (subtree.label() == "NP"):
            foundNP = False
            for subsubtrees in subtree.subtrees():
                if(subtree != subsubtrees):
                    # print(subtree.label())
                    # subtree.pretty_print()  
                    # print(subsubtrees.label())
                    # subsubtrees.pretty_print()
                    # print("~~~~~~~~~~~~~~~~~~~")
                    # input()
                    if (subsubtrees.label() == "NP"):
                        foundNP = True
                        break
            if(not foundNP):
                # print("Added A tree :")
                # subtree.pretty_print()
                # print("~~~~~~~~~~~~~~~~~~~")
                contents.append(subtree)
    # for tree in contents:
    #     tree.pretty_print()
    #     print("~~~~~~~~~~~~~~~~~~~")
    # input()     
    
    return contents
    # raise NotImplementedError


if __name__ == "__main__":
    main()
