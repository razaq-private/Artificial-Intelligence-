import numpy as np
import nltk
############################################################
# CIS 521: Homework 1
############################################################

student_name = "Abudurazaq Aribidesi"

# This is where your grade report will be sent.
student_email = "raribide@seas.upenn.edu"

############################################################
# Section 1: Python Concepts
############################################################

python_concepts_question_1 = "Strongly typed means that every \
    object's type is fixed.\
    This means that you cannot combine a string\
     and an int and expect a result because they are different types.\
Dynamic type means that you can change\
     the types of the variables and keep updating it."

python_concepts_question_2 = "This throws an error becuase lists \
    cannot be keys for a dictionary\
    . If this were a tuple it would have worked."

python_concepts_question_3 = "I believe that the second option with the \
    .join is more effiecient for larger inputs\
    it is better than just looping through all of the words."

############################################################
# Section 2: Working with Lists
############################################################


def extract_and_apply(lst, p, f):
    return [f(x) for x in lst if p(x)]


def concatenate(seqs):
    return [x for y in seqs for x in y]


def transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    empty = [[0 for x in range(rows)] for x in range(cols)]
    for i in range(rows):
        for j in range(cols):
            empty[j][i] = matrix[i][j]
    return empty

############################################################
# Section 3: Sequence Slicing
############################################################


def copy(seq):
    return seq[:]


def all_but_last(seq):
    return seq[:-1]


def every_other(seq):
    return seq[::2]

############################################################
# Section 4: Combinatorial Algorithms
############################################################


def prefixes(seq):
    for i in range(len(seq)+1):
        yield seq[:i]


def suffixes(seq):
    for i in range(len(seq)+1):
        yield seq[i:]


def slices(seq):
    for i in range(len(seq)):
        for j in range(i+1, len(seq)+1):
            yield seq[i:j]

############################################################
# Section 5: Text Processing
############################################################


def normalize(text):
    norm = ' '.join(text.split())
    return norm.lower()


def no_vowels(text):
    vowels = ['A', 'E', 'I', 'O', 'U', 'a', 'e', 'i', 'o', 'u']
    for v in vowels:
        text = text.replace(v, '')
    return text


def digits_to_words(text):
    dict_digit = {"0": "zero",
                  "1": "one",
                  "2": "two",
                  "3": "three",
                  "4": "four",
                  "5": "five",
                  "6": "six",
                  "7": "seven",
                  "8": "eight",
                  "9": "nine"}
    return ' '.join(dict_digit[x] for x in text if x in dict_digit)


def to_mixed_case(name):
    text = name.split('_')
    text = ' '.join(text)
    text = text.title()
    final = text[0].lower() + text[1:]
    return final.replace(" ", "")

############################################################
# Section 6: Polynomials
############################################################


class Polynomial(object):

    def __init__(self, polynomial):
        self.polynomial = tuple(polynomial)

    def get_polynomial(self):
        return self.polynomial

    def __neg__(self):
        neg = [(-coeff, expo) for coeff, expo in self.polynomial]
        return Polynomial(neg)

    def __add__(self, other):
        return Polynomial(self.polynomial + other.polynomial)

    def __sub__(self, other):
        other = -other
        return Polynomial(self.polynomial + other.polynomial)

    def __mul__(self, other):
        final = []
        for i in self.polynomial:
            for j in other.polynomial:
                coeff_i, expo_i = i
                coeff_j, expo_j = j
                new_coeff = coeff_i * coeff_j
                new_expo = expo_i + expo_j
                final.append((new_coeff, new_expo))
        return Polynomial(final)

    def __call__(self, x):
        return sum([poly[0] * (x ** poly[1]) for poly in self.polynomial])

    def simplify(self):
        poly = {}
        for coeff, expo in self.polynomial:
            if expo in poly:
                poly[expo] += coeff
            else:
                poly[expo] = coeff

        final = []
        for expo, coeff in poly.items():
            if coeff != 0:
                final.append((coeff, expo))

        final.sort(key=lambda x: x[1], reverse=True)

        if not final:
            final = [(0, 0)]

        self.polynomial = tuple(final)

    def __str__(self):
        text = ""
        for coeff, expo in self.polynomial:
            if coeff < 0:
                text += " - "
            else:
                text += " + "

            if text[1] == "+":
                text = text[0] + text[2:]

            if expo == 0 or abs(coeff) != 1:
                text += str(abs(coeff))

            if expo > 0:
                text += "x"
                if expo > 1:
                    text += "^" + str(expo)

        if text[0] == "-":
            print('works')
            text = "-" + text[3:]
        print("tex1:" + text)
        text = ' '.join(text.split())
        print("tex2:" + text)
        return text


############################################################
# Section 7: Python Packages
############################################################

def sort_array(list_of_matrices):
    nums = np.array([], dtype=int)

    for matrix in list_of_matrices:
        flat_matrix = matrix.flatten()
        nums = np.concatenate((nums, flat_matrix))

    final_array = np.sort(nums)[::-1]

    return final_array


def POS_tag(sentence):
    punctuation = ['!', '?', '.', '-', '_', ';',
                   ':', '(', ')', '[', ']', '~', ',']
    sentence = sentence.lower()
    tokens = nltk.word_tokenize(sentence)
    stops = set(nltk.corpus.stopwords.words('english'))
    words = [word for word in tokens if word
             not in stops and word not in punctuation]
    return nltk.pos_tag(words)


############################################################
# Section 8: Feedback
############################################################

feedback_question_1 = """
Around 10-11 hours
"""

feedback_question_2 = """
I mainly found the last part more confusing because\
     I was not sure on what we were supposed to do.\
     I also do not have as much experience with \
    coding so it was interesting learning different topics.
"""

feedback_question_3 = """
I liked how broad the assignment was beacsue I was able \
    to work on othe rparts if I were to get \
        stuck instead of just focusing on one portion.
"""
