from typing import List
import math
import pandas as pd
import os
from pandas import Series
from src.url_interpreter.token import Token


class StateMachineNew:
    def __init__(self):
        self.transition_table = pd.read_csv(os.path.join(os.path.dirname(__file__), "state-machine123.csv"))
        self.current_state = 0

    def set_next_state(self, token: Token, token_category):
        try:

            new_state = int(self.transition_table[token_category][self.current_state])
            self.current_state = new_state
        except (Exception, ValueError):
            print(f'Token: {token.word()}')
            print(f'Token category: {token_category} Current state: {self.current_state}')
            raise

    def is_final_state(self):
        return self.transition_table["is_final"][self.current_state]

    def possible_categories(self, category) -> List[str]:
        column = self.transition_table[category]
        states: List[int] = list(set([int(i[1]) for i in column.items() if not math.isnan(i[1])]))
        categories = []
        for s in states:
            line: Series = self.transition_table.iloc[s]
            line.pop('state')
            line.pop('is_final')
            categories += [i[0] for i in line.items() if not math.isnan(i[1])]
        return list(set(categories))


