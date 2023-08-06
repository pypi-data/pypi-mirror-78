class File:
    def __init__(self, uses, node):
        super().__init__()
        self.uses = uses
        self.node = node

    def __repr__(self):
        uses = '\n'.join(str(u) for u in self.uses)
        return uses + f'\n{self.node}'
