import numpy as np
import os
import random

current_dir = os.path.dirname(__file__)
path = os.path.join(current_dir, "bunny_names.txt")
names = open(path).read().split(",")
names = [n.strip() for n in names]

def get_random_name():
    """
    Returns a random bunny name.
    """
    index = random.randint(0, len(names))
    return names[index]


