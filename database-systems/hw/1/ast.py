class AST:
    def __init__(self, statement):
        self.statement = statement
        cleaned = self.clean(statement.tokens)

    def clean(self, tokens):
        f = lambda x: not(x.is_whitespace)
        return list(filter(f, tokens))
