from lib2to3.pgen2.parse import ParseError
import sys
import os
import math
from collections import defaultdict

from itertools import islice


def default_value():
    return 1


transition_matrix = defaultdict(default_value)
emission_matrix = defaultdict(default_value)
transition_tag_count = defaultdict(default_value)

word_tags = dict()
tags_list = list()


def is_english(s):
    try:
        s.encode(encoding="utf-8").decode("ascii")
    except UnicodeDecodeError:
        return False
    else:
        return True


def take(n, iterable):
    return list(islice(iterable, n))


def fix_tag(word, tag, tag_prob):
    word = str(word)
    tag = str(tag)

    most_prob = take(2, tag_prob)[1:]
    if len(tag) == 0:
        if is_english(word[0]):
            if word[0].isupper():
                tag = "SP"
            else:
                tag = "S"
        else:
            tag = most_prob[0]

    return word, tag


def load(line, read_flag):
    tokens = line.strip("\n").split(" ")
    if read_flag == 1:
        t = (tokens[0], tokens[1])
        emission_matrix[t] = float(tokens[2])
    elif read_flag == 2:
        t = (tokens[0], tokens[1])
        transition_matrix[t] = float(tokens[2])
    elif read_flag == 3:
        word_tags[tokens[0]] = set()
        for i in tokens[1].split(","):
            word_tags[tokens[0]].add(i)
    elif read_flag == 4:
        transition_tag_count[tokens[0]] = float(tokens[1])
    else:
        raise ParseError


def output(previous_state, previous_tag, index, line):
    f = open("hmmoutput.txt", "a")
    k = index

    for i in range(k):
        if index == 0:
            break
        tags_list.append(previous_state[index][previous_tag])
        index -= 1
        previous_tag = previous_state[index + 1][previous_tag]

    if index == 0:
        tags_list.reverse()
        lines = list(line.split(" "))
        x = len(lines)
        tempans = ""
        for i in range(x):
            fixed_word, fixed_tag = fix_tag(
                lines[i], tags_list[i], transition_tag_count
            )
            tempans = tempans + " " + fixed_word.rstrip() + "/" + fixed_tag
        f.write(tempans.lstrip().rstrip().strip())
        f.write("\n")
        f.close()


def last_tag(previous_state, previous_word, line):
    max_last_tag = max(previous_word, key=lambda k: previous_word[k])
    tags_list.append(max_last_tag[1])

    output(previous_state, max_last_tag[1], max_last_tag[2], line)


def viterbi_algorithm():
    with open(sys.argv[1]) as f:
        for line in f:
            previous_word = dict()
            previous_state = dict()
            index = 0

            tokens = line.strip().split(" ")
            start = "<s>"
            counter = 0

            first_avg = [0, 0]
            second_avg = [0, 0]

            for observation in tokens:
                temp_dict = dict()
                if counter == 0:
                    if observation in word_tags:
                        for current_tag in word_tags[observation]:
                            transition_tuple = (start, current_tag)
                            transmission_probability = float(
                                transition_matrix[transition_tuple]
                            )
                            observation_tuple = (observation, current_tag)
                            observation_probability = float(
                                emission_matrix[observation_tuple]
                            )

                            probability_value = math.log(
                                transmission_probability, 10
                            ) + math.log(observation_probability, 10)
                            first_avg[0] += probability_value
                            first_avg[1] += 1

                            previous_word[
                                tuple([observation, current_tag, index])
                            ] = probability_value

                    # observation not in word_tags
                    else:
                        for key in transition_matrix:
                            if key[0] == "<s>" and key[1] != "<s>":
                                previous_word[
                                    tuple([observation, key[1], index])
                                ] = math.log(transition_matrix[key], 10)
                                second_avg[0] += math.log(transition_matrix[key], 10)
                                second_avg[1] += 1
                # counter not 0
                else:
                    if observation in word_tags:
                        counter_dict = dict()
                        temp_1 = ""
                        temp_2 = ""
                        for current_tag in word_tags[observation]:
                            max_probability = -float(1e9)

                            for k in previous_word:
                                transition_tuple = (k[1], current_tag)
                                transmission_probability = float(
                                    transition_matrix[transition_tuple]
                                )
                                observation_tuple = (observation, current_tag)
                                emission_probability = float(
                                    emission_matrix[observation_tuple]
                                )

                                if (
                                    transmission_probability == 0.0
                                    or emission_probability == 0.0
                                ):
                                    probability_value = float(previous_word[k])
                                else:
                                    probability_value = (
                                        (math.log(transmission_probability, 10))
                                        + math.log(emission_probability, 10)
                                        + float(previous_word[k])
                                    )
                                if probability_value > max_probability:
                                    max_probability = probability_value
                                    temp_1 = current_tag
                                    temp_2 = k

                            counter_dict[
                                tuple([observation, temp_1, index])
                            ] = max_probability
                            temp_dict[temp_1] = temp_2[1]
                    else:
                        tempdict = dict()
                        counter_dict = dict()

                        for word in previous_word:
                            for keys in transition_matrix:
                                if word[1] == keys[0]:
                                    if transition_matrix[keys] == 0.0:
                                        probability_value = float(previous_word[word])
                                    else:
                                        probability_value = math.log(
                                            transition_matrix[keys], 10
                                        ) + float(previous_word[word])
                                    tempdict[
                                        tuple([keys[0], keys[1], index])
                                    ] = probability_value

                        sorted_dict = dict(
                            sorted(tempdict.items(), key=lambda x: x[1], reverse=True)
                        )
                        temp_dict_2 = dict()
                        tags_dict = dict()
                        for key in sorted_dict:
                            if key[1] not in tags_dict:
                                temp_dict_2[key] = sorted_dict[key]
                            tags_dict[key[1]] = 1

                        for temp_key in temp_dict_2:
                            counter_dict[
                                tuple([observation, temp_key[1], index])
                            ] = temp_dict_2[temp_key]
                            temp_dict[temp_key[1]] = temp_key[0]

                counter += 1
                previous_state[index] = temp_dict
                if counter > 1:
                    previous_word = counter_dict
                index += 1
            last_tag(previous_state, previous_word, line)


if __name__ == "__main__":
    read_flag = 0
    if os.path.exists("hmmoutput.txt"):
        os.remove("hmmoutput.txt")

    with open("hmmmodel.txt") as f:
        for line in f:
            if line.startswith("*Emission Probabilities"):
                read_flag = 1
            elif line.startswith("*Transition Probabilites"):
                read_flag = 2
            elif line.startswith("*Tags"):
                read_flag = 3
            elif line.startswith("*Tag Counts"):
                read_flag = 4
            else:
                load(line, read_flag)

        viterbi_algorithm()
