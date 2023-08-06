import os
os.environ["BUNNY_LAB_LOCAL"] = "1"
import bunny_lab.api as api
import traceback
import sys
from bunny_lab.levels import levels

class BunnyLabSession:
    """
    Client-side interface to the bunny-lab server.
    """
    def __init__(self, url):
        self.url = url
        self.name = api.register(url)
        self.levels_completed = set()
        print(f"Welcome, {self.name}, to the Bunny Lab.\n"
              "Good luck saving your furry comrades!")

    def __del__(self):
        api.unregister(self.url, self.name)

    def get_results(self):
        response = api.get_results(self.url)
        bold_name = "<b>" + self.name + " (you) </b>"
        return response.replace(self.name, bold_name)

    def bunnies_saved(self, bunnies, level=0, **kwargs):
        if not level in self.levels_completed:
            levels[level - 1].complete(bunnies)
            n_saved = len(bunnies)
            api.bunnies_saved(self.url, self.name, n_saved)
            self.levels_completed.add(level)


session = None

def initialize(url):
    global session
    session = BunnyLabSession(url)

def rescue(bunnies, level=0, **kwargs):
    session.bunnies_saved(bunnies, level, **kwargs)


class BunnyLabLevel:
    def __init__(self, level_number, function):
        self.level_number = level_number
        self.function = function
        self.tries = 0
        self.completed = False
        self.n_rescued = 0

    def __call__(self, *args, **kwargs):
        if self.completed:
            print(f"You already completed this level and rescued {self.n_rescued} bunnies.")
            return None

        if self.tries >= 3:
            print("You exhausted your number of tries.")
            return None

        try:
            global rescue
            def rescue_level(bunnies):
                self.n_rescued += len(bunnies)
                session.bunnies_saved(bunnies, self.level_number)
            rescue = rescue_level
            self.function(*args, **kwargs)
            self.completed = True
        except Exception as e:
            self.tries += 1
            print(f"Oh no, your function call failed! You have {3 - self.tries} tries left.\n")
            traceback.print_exc(file=sys.stdout, limit=-1)


#
# Level 1
#

def _transport_bunnies(velocity):
    """
    Bunnies need to be transported from the farm to the lab but the road
    is dangerous and the amount of oxygen in the truck is limited.
    """
    bunnies = ["Fifi", "Gunter", "Hazy"]
    distance = 100.0

    time_required = distance / velocity
    oxygen_required = time_required * 10.0

    if velocity > 100:
        return rescue([])
    if oxygen_required > 20.0:
        return rescue([])

    rescue(bunnies)

transport_bunnies = BunnyLabLevel(1, _transport_bunnies)

#
# Level 2
#

def _shave_bunnies(device_index):
    """
    Shaves bunnies to prepare them for experiments.
    """
    bunnies = ["Alfie", "Bugs", "Chip"]
    devices = ["harmless bunny shaver", "buzz saw", "rusty razor"]
    devices.reverse()
    device = devices[device_index]

    for bunny in bunnies:
        if device in ["buzz saw", "rusty razor"]:
            bunnies.remove(bunny)

    rescue(bunnies)

shave_bunnies = BunnyLabLevel(2, _shave_bunnies)

#
# Level 3
#

def _feed_bunnies(names):
    """
    Some of the bunnies are hungry and need food. This
    function feeds a list of bunnies.
    """
    hungry_bunnies = ["Hips", "Ivan", "Jo"]
    allergies = {"Hips":  ["Carrots"],
                 "Ivan": ["Hay, Carrots"],
                 "Jo": ["Cale"]}
    foods = ["Carrots", "Hay", "Cale"]

    bunnies_fed = []
    for bunny, food in zip(names, foods):
        if not food in allergies[bunny]:
            bunnies_fed.append(bunny)

    healthy_bunnies = [b for b in bunnies_fed if b in hungry_bunnies]
    rescue(healthy_bunnies)

feed_bunnies = BunnyLabLevel(3, _feed_bunnies)

#
# Level 4
#
from random import shuffle

def _test_drug(choose_drug):
    """
    You offer the scientist help with the experiments in order to save your
    bunny friends. The task they give you is to choose the drug to give
    to each patient.
    """
    bunnies = ["Turbo", "Uma", "Velvet", "Whoopie"]
    drugs = ["Placebo", "Bleach"]

    healthy_bunnies = []
    for bunny in bunnies:
        drugs_shuffled = shuffle(drugs)
        drug = choose_drug(drugs_shuffled)
        if drug == "Placebo":
            healthy_bunnies.append(bunny)

    rescue(healthy_bunnies)

test_drug = BunnyLabLevel(4, _test_drug)

#
# Level 5
#
from random import random

def _free_bunnies(spy_class):
    """
    Just as you and a group of other bunnies want to escape from the lab, you
    discover that the back door is locked with a secret code. To open it, you
    need to spy on a guard who's going out for a smoke.
    """
    bunnies = ["Turbo", "Uma", "Velvet", "Whoopie"]
    drugs = ["Placebo", "Bleach"]

    spy = spy_class()

    secret_code = []
    for i in range(10):
        x = random()
        spy.listen(x)
        secret_code.append(x)

    if secret_code == spy.guess_code():
        rescue(bunnies)

free_bunnies = BunnyLabLevel(5, _free_bunnies)
