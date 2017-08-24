from pyparsing import *

E = CaselessLiteral("E")
sign = Word('+-', exact=1)                                              
                                                                        
                                                                        
mantissa = Optional(E + Optional("+") + Word(nums))                     
                                                                        
withLeft = Optional(sign) + Word(nums) + "." + Optional(Word(nums))         
withoutLeft = ("." + Word(nums))                                        
real = Combine((withLeft | withoutLeft) + mantissa)
integer = Combine(Optional(sign) + Word(nums) + mantissa)


operand = real | integer
expr = operatorPrecedence( operand,
    [(oneOf("+ -"), 1, opAssoc.RIGHT),
     ("!", 1, opAssoc.LEFT),
     (oneOf("* /"), 2, opAssoc.LEFT),
     (oneOf("+ -"), 2, opAssoc.LEFT),]
    )

print(expr.runTests(input()))
