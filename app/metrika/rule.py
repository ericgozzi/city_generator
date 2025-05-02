

class Rule:

    def __init__(self, rules: list[tuple[any, any]]):
        self.rules: list[tuple] = rules


    def __str__(self):
        string = '<|'
        for i, rule in enumerate(self.rules):
            string += f'{rule[0]} -> {rule[1]}'
            if i < len(self.rules)-1:
                string += ', '
        string += '|>'
        return string
    


    def merge(self, new_rules: 'Rule') -> None:
        merged = self.rules + new_rules.rules
        self.rules = merged

    
