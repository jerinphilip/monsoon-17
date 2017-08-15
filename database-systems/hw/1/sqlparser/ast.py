from pprint import pprint

def Integer(t):
    return ("Int", int(t[0]))

def Real(t):
    return ("Float", float(t[0]))

def String(t):
    return ("String", t[0])

def Identifier(t):
    return ("Id", t[0])

def BinaryOp(t):
    return ("BinaryOp", t[0])

def OpReorder(t):
    x, op, y = t
    return (op, (x, y))

def Projection(t):
    return ("Projection", t)

def From(t):
    #print("From:")
    #pprint(t)
    return ("From", t[1])

def Select(t):
    #print("Select:", len(t))
    #for i in t:
    #    pprint(i)
    #pprint(t)
    s, p, f, w = t
    return ("Select", (f, w, p))


def removeParanthesis(t):
    opening, e, closing = t
    return [e]

def Where(t):
    return ("Where", t[1])

def Function(t):
    return ("Function", t)

