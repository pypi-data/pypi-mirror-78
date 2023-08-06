def print_bunnies(bunnies):
    s = ""
    for b in bunnies[:-1]:
        s += b + ", "
    if len(bunnies) > 0:
        s += "and " + bunnies[-1]
    return s

class Level:
    def __init__(self,
                 msg_saved,
                 msg_dead):
        self.msg_saved = msg_saved
        self.msg_dead = msg_dead

    def complete(self, bunnies, **kwargs):
        kwargs["bunnies"] = print_bunnies(bunnies)
        if len(bunnies) > 0:
            print(self.msg_saved.format(**kwargs))
        else:
            print(self.msg_dead.format(**kwargs))

level_1 = Level("Well done, {bunnies} survived the transport to the lab.",
                "Oh no, none of the bunnies made it to the lab.")
level_2 = Level("Great job, you saved {bunnies}.",
                "Oh no, this was definitely not the right device to shave bunnies."
                "None of {bunnies} made it.")
level_3 = Level("Great job, you saved {bunnies}.",
                "Oh no, {bunnies} got the wrong food.")
level_4 = Level("Great job, you saved {bunnies}.",
                "Oh no, turns out injecting bleach isn't the best idea.")
level_5 = Level("Great job, you and {bunnies} escape into the night.",
                "Oh no, you entered the wrong code and got caught.")

levels = [level_1, level_2, level_3, level_4, level_5]
