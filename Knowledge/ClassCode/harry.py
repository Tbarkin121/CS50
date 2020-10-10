from logic import *

rain = Symbol("rain")
hagrid = Symbol("hagrid")
dumbledore = Symbol("dumbledore")

hermione = Symbol("hermione")
harry = Symbol("harry")
ron = Symbol("ron")
library = Symbol('library')


knowledge = And(
    Implication(Not(rain), hagrid),
    Or(hagrid, dumbledore),
    Not(And(hagrid, dumbledore)),
    dumbledore
)

# print(model_check(knowledge, rain))
print(knowledge.formula())