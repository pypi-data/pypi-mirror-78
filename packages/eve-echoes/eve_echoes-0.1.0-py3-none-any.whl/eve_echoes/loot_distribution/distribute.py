import copy
import json
import typing
from collections import Counter

import numpy as np


class LootDistribution:
    def __init__(self, members: typing.List[str], modules: typing.Dict[str, int]):
        self.members = {member: {"size": 0} for member in members}
        self.modules = modules

    def distribute(self):
        maxsize = 0
        remaining_member_list = list(self.members.keys())

        for module, quantity in self.modules.items():
            for item in range(quantity):
                # Everyone gets another item
                if len(remaining_member_list) == 0:
                    remaining_member_list = list(self.members.keys())

                # Select random member
                give_to = np.random.choice(remaining_member_list)
                remaining_member_list.remove(give_to)

                # Give module to member
                if module in self.members[give_to]:
                    self.members[give_to][module] += 1
                else:
                    self.members[give_to][module] = 1

                self.members[give_to]["size"] += 1
        return self.members
