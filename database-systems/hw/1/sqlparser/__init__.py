from pyparsing import *
from collections import namedtuple
from .ast import *

selectStmt = Forward()

keywords = [
        "select", "from", "where",
        "and", "or", "not", "in"
]

ls = list(map(lambda x: Keyword(x, caseless=True), keywords))
reserved = namedtuple('reserved', map(lambda k: k+"_", keywords))
g = reserved(*ls)


identifier = Word(alphas, alphanums + "_$").setParseAction(Identifier)
aggregate = oneOf("min max avg sum", caseless=True).setParseAction(upcaseTokens)\


# Column Definitions
#column = (delimitedList(identifier, ".", combine=False)).\
                        #setName("column").setParseAction(Nest)
column = (identifier + Optional('.' + identifier)).setParseAction(Column)
columns = (delimitedList(column)).setParseAction(Columns)

# Table Defs
table = (identifier)
tables = (delimitedList(table)).setParseAction(Tables)

whereExpression = Forward()
E = CaselessLiteral("E")

compare = oneOf("= != < > >= <= eq ne lt le gt ge", caseless=True).setParseAction(BinaryOp)
sign = Word('+-', exact=1)


mantissa = Optional(E + Optional("+") + Word(nums))

withLeft = Optional(sign) + Word(nums) + "." + Optional(Word(nums))
withoutLeft = ("." + Word(nums))
real = Combine((withLeft | withoutLeft) + mantissa).setParseAction(Real)
integer = Combine(Optional(sign) + Word(nums) + mantissa).setParseAction(Integer)
columnRval = real | integer | quotedString | column

aggrExpr = (aggregate + ("(" + column + ")").setParseAction(removeParanthesis)).\
        setParseAction(Function)
aggGroup = delimitedList(aggrExpr).setParseAction(Functions)
tuples = ( aggGroup | columns | '*' ).setParseAction(Projection)

compareExpr = (column + compare + columnRval).setParseAction(OpReorder)
existCheck = (column + g.in_ + "(" + delimitedList(columnRval) + ")")
whereExpr = Forward()

whereCondition = (compareExpr | existCheck | ("(" + whereExpr + ")").setParseAction(removeParanthesis))
whereExpr << whereCondition + ZeroOrMore((g.or_ | g.and_) + whereExpr)
whereStruct = (g.where_ + whereExpr).setParseAction(Where)

select = Forward()
selects = delimitedList(("(" + select + ")").setParseAction(removeParanthesis))

followFrom = (tables | selects).setParseAction(removeParanthesis))
fromEtc = (g.from_ + followFrom).setParseAction(From)

select <<= (
        g.select_ + 
        tuples + 
        fromEtc +
        Optional(whereStruct, None)).setParseAction(Select)

SQL = select

def parse(query):
    r = SQL.parseString(query)
    return r

if __name__ == '__main__':
    import sys
    from pprint import pprint
    #table.runTests(sys.argv[1])
    #integer.runTests(sys.argv[1])
    #SQL.runTests(sys.argv[1])
    try:
        p = SQL.parseString(sys.argv[1])
        pprint(p.asList())
    except e:
        print(e)
