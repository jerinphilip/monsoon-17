from pyparsing import *
from collections import namedtuple
from .ast import *

selectStmt = Forward()

keywords = [
        "select", "from", "where",
        "and", "or", "not", "in"
]

ls = list(map(lambda x: Keyword(x, caseless=True).addParseAction(upcaseTokens), keywords))
reserved = namedtuple('reserved', map(lambda k: k+"_", keywords))
g = reserved(*ls)

identifier = Word(alphas, alphanums + "_$").setParseAction(Identifier)
aggregate = oneOf("min max avg sum abs distinct", caseless=True).setParseAction(upcaseTokens)\


column = (identifier + Optional('.' + identifier))
columns = (delimitedList(column)).setParseAction(Columns)

tables = (delimitedList(identifier)).setParseAction(Tables)

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

aggrExpr = (aggregate + ("(" + columns + ")").setParseAction(removeParanthesis)).\
        setParseAction(Function)
aggGroup = delimitedList(aggrExpr).setParseAction(Functions)
wildCard = Word('*', exact=1).setParseAction(All)
tuples = ( aggGroup | columns | wildCard ).setParseAction(Projection)

compareExpr = (column + compare + columnRval).setParseAction(OpReorder)
existCheck = (column + g.in_ + "(" + delimitedList(columnRval) + ")")
#whereExpr = Forward()
#whereCondition = (compareExpr | existCheck | ("(" + whereExpr + ")").setParseAction(removeParanthesis, Nest))
# whereExpr << (whereCondition + ZeroOrMore((g.or_ | g.and_) + whereExpr))
whereExpr = (compareExpr | existCheck)
whereExpr  = infixNotation(whereExpr, [
                        (g.or_, 2, opAssoc.RIGHT),
                        (g.and_, 2, opAssoc.RIGHT),
                    ]).setParseAction(UnNest, OpTree)
whereStruct = (g.where_ + whereExpr).setParseAction(Where)

select = Forward()
selects = delimitedList(("(" + select + ")").setParseAction(removeParanthesis)).setParseAction(Selects)

followFrom = (tables | selects) 
fromEtc = (g.from_ + followFrom).setParseAction(From)

select <<= (
        g.select_ + 
        tuples + 
        fromEtc +
        Optional(whereStruct, None)).setParseAction(Select)

SQL = select

def parse(query):
    try:
        r = SQL.parseString(query, True)
        #pprint(r.asList())
        return r
    except ParseException as e:
        print("ParseError:")
        print('\t' + query)
        print('\t' + ' '*(e.col-1) + '^')
        print(e)
        exit()

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
