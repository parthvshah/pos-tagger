#!/usr/bin/env python3

from lib2to3.pgen2.tokenize import TokenError
import sys
import itertools

# Initialize
transition_matrix = dict()
emission_matrix = dict()

emission_tag_count = dict()
transition_tag_count = dict()

word_tags = dict()

tags = set()

# Function to split a token into a word and tag
def split_token(token):
    slashes_count = token.count("/")
    if slashes_count > 1:
        token = token.replace("/", "\\", slashes_count - 1)
    word = token.split("/")[0]
    tag = token.split("/")[1]

    if len(word) == 0 or len(tag) == 0:
        raise TokenError

    return word, tag


# Function to update a dict based on key - increment by 1
def atomic_update(dictionary, key):
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1


# Function to write the params of the model into a text file
def write_state():
    with open("hmmmodel.txt", "w+") as f:
        # Emmisions
        f.write("<Emission Probabilities>\n")
        for key in emission_matrix:
            value = float(
                (emission_matrix[key]) / (float(emission_tag_count[str(key[1])]))
            )
            f.write(str(key[0]) + " " + str(key[1]) + " " + str(value) + "\n")

        # Transitions
        f.write("<Transition Probabilites>\n")
        for i in itertools.combinations_with_replacement(tags, 2):
            if (i not in transition_matrix) and (i[1] != "<s>"):
                transition_matrix[i] = 0
            if (tuple([i[1], i[0]]) not in transition_matrix) and (i[0] != "<s>"):
                transition_matrix[tuple([i[1], i[0]])] = 0
        for key in transition_matrix:
            val = (transition_matrix[key] + 1) / (
                float(len(transition_tag_count) - 1) + transition_tag_count[str(key[0])]
            )
            f.write(str(key[0]) + " " + str(key[1]) + " " + str(val) + "\n")

        # Tags
        f.write("<Tags>\n")
        for key, value in word_tags.items():
            f.write(key + " " + ",".join([str(i) for i in value]) + "\n")

        # Tag counts
        f.write("<Tag Counts>\n")
        for key, value in emission_tag_count.items():
            f.write(key + " " + str(value) + "\n")


if __name__ == "__main__":
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        for line in f:
            start_tag = "<s>"
            atomic_update(emission_tag_count, start_tag)

            # Get all tokens
            tokens = line.strip().split(" ")
            for token in tokens:
                atomic_update(transition_tag_count, start_tag)

                word, tag = split_token(token)
                # word = token.split('/')[0]
                # tag = token.split('/')[1]

                atomic_update(emission_tag_count, tag)
                transmission_tuple = (start_tag, tag)
                atomic_update(transition_matrix, transmission_tuple)
                tags.add(start_tag)
                tags.add(tag)
                emission_tuple = (word, tag)
                atomic_update(emission_matrix, emission_tuple)
                if word not in word_tags:
                    word_tags[word] = set()
                else:
                    word_tags[word].add(tag)

                start_tag = tag
                # TODO: Implement end tag
    write_state()
