import sys

from itertools import islice


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


test_f = open(sys.argv[1], "r")
truth_f = open(sys.argv[2], "r")

total = 0
correct = 0

from collections import OrderedDict

misclass_dict = dict()

for test_l, truth_l in zip(test_f, truth_f):
    test_a = test_l.split(" ")
    truth_a = truth_l.split(" ")

    for test_w, truth_w in zip(test_a, truth_a):
        if test_w.strip() == truth_w.strip():
            correct += 1
        else:
            # print(test_w, " --> ", truth_w)
            key = tuple([test_w.split("/")[1], truth_w.split("/")[1]])
            if key not in misclass_dict:
                misclass_dict[key] = 1
            else:
                misclass_dict[key] += 1

        total += 1

misclassifications = OrderedDict(
    sorted(misclass_dict.items(), key=lambda x: x[1], reverse=True)
)

print(take(10, misclassifications.items()))
print("Accuracy: ", correct / total)
