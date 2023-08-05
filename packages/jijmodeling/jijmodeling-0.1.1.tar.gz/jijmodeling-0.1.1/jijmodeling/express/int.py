from jijmodeling.express.express import Express


class Int(Express):
    def __init__(self, label: str) -> None:
        super().__init__([])
        self.label = label