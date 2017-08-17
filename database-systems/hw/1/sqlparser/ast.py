from pprint import pprint

def Integer(t):
    return ("Int", int(t[0]))

def Real(t):
    return ("Float", float(t[0]))

def String(t):
    return ("String", t[0])

def Identifier(t):
    return t[0]
    #return ("Id", t[0])

def BinaryOp(t):
    return ("BinaryOp", t[0])

def OpReorder(t):
    x, op, y = t
    return (op, (x, y))

def Projection(t):
    return ("Projection", t)

def From(t):
    f, r = t
    return ("From", r)

def Select(t):
    #print("Select:", len(t))
    #for i in t:
    #    pprint(i)
    #pprint(t)
    s, p, f, w = t
    return ("Select", (f, w, p))

def removeParanthesis(t):
    opening, e, closing = t
    return e

def Where(t):
    return ("Where", t[1])

def Function(t):
    return ("Function", t)


def Nest(t):
    return t

def Column(t):
    return ("Column", t)

def Columns(t):
    return ("Columns", t)

def Tables(ts):
    tagged_ts = list(map(Table, ts))
    return ("Tables", tagged_ts)

def Table(t):
    return ("Table", t)

def Functions(t):
    return ("Functions", t)

def All(t):
    return ("All", t)

def Selects(t):
    return ("Selects", t)

