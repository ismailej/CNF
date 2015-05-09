Representing Propositional Sentences:

The standard notation for propositional logic is not the easiest for computers
to process. Sure, we can find unicode characters for all of special symbols,
but we probably do not want to operate directly on unicode-encoded strings
for automated reasoning. Instead, we can represent sentences in propositional
logic using nested lists.

Traditional notation:
¬R ^ B ⇒ W

List representation (Python-style):
["implies", ["and", ["not", "R"], "B"], "W"]

This program convert any propositional logic sentence into its equivalent CNF sentence.

Sample Input 

["not", ["implies", ["implies", ["or", "P", ["not", "Q"]], "R"], ["and", "P", "R"]]]
["implies", ["implies", "a", "b"], "c"]
["not", ["not", ["or",["and", "p", "q"], ["not", "q"]]]]

Sample Output 

["and", "R", ["not", "B"], "W"]
["and", ["or", "P", ["not", "R"]], ["or", ["not", "Q"], ["not", "R"], "P"], ["not", "P"]]
["not", "p"]
["and", "p", ["not", "p"]]
["and", ["or", "p", "q"], ["or", ["not", "p"], "r"], ["or", ["not", "r"], ["not", "p"]], ["or", ["not", "q"], "s", ["not", "t"]], "t"]
["and", ["not", "p"], "p"]
["and", ["or", ["not", "p"], "q"], ["or", ["not", "q"], ["not", "p"]], ["or", "p", ["not", "q"]]]
["not", "p"]
