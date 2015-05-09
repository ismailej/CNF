import sys


#Global variables
symbols = {}
results = {}
li = []


""" Implies elimnation :- P => Q is equivalent to ~P or Q, 
    Bidirectional elimnation :- P <=> Q is equivalent to P => Q and Q => P, 
"""
def implication_elimination(o):

    if isinstance(o, list):
        if o[0] == "implies":
            o[0] = "or"
            new = ["not"]
            new.append(o[1])
            o[1] = new
        elif o[0] == "iff":
            o[0] = "and" 
            new = ["implies"]
            new.append(o[1])
            new.append(o[2])
            new1 = ["implies"]
            new1.append(o[2])
            new1.append(o[1])
            o[1] = new
            o[2] = new1
                     
        for value in o:
            implication_elimination(value)
                 
    return o
    
""" demorgan_and :- all clauses in the form [not, [and, P, Q]] will be converted to 
	[or, [not, p], [not, q]] in below function
"""

def demorgan_and(sentence):
    global change
    if isinstance(sentence, list):
        if sentence[0] == "not":
            if isinstance(sentence[1], list):
                    if sentence[1][0] == "and":
                        new = sentence[1]
                        sentence.pop()
                        sentence[0] = "or"
                        change = 1
                        for item in new[1:]:
                            if isinstance(item, list) and item[0] == "not":
                                sentence.append(item[1])
                            else:
                                sentence.append(["not", item])
        
        
        for elem in sentence:
            demorgan_and(elem)
    
    return sentence

""" demorgan_or :- all clauses in the form [not, [or, P, Q]] will be converted to 
	[and, [not, p], [not, q]] in below function
"""
def demorgan_or(sentence):
    global change
    if isinstance(sentence, list):
        if sentence[0] == "not":
            if isinstance(sentence[1], list):
                    if sentence[1][0] == "or":
                        new = sentence[1]
                        sentence.pop()
                        sentence[0] = "and"
                        change = 1
                        for item in new[1:]:
                            if isinstance(item, list) and item[0] == "not":
                                sentence.append(item[1])
                            else:
                                sentence.append(["not", item])
        
        
        for elem in sentence:
            demorgan_or(elem)
    return sentence
          

""" double_negation :- removes clauses of the form [not, [not, p]] to p
"""
def double_negation(sentence):
    global change
    if isinstance(sentence, list):
        if isinstance(sentence[1], list):
            #print "sentence 1 0", sentence[1][0]
            if sentence[1][0] == "not":
                if isinstance(sentence[1][1], list):
                    if sentence[1][1][0] == "not":
                       # new = sentence[1][1]
                       change = 1
                       # sentence.pop()
                       # sentence.pop()
                       # sentence.extend(new)
                       sentence[1] = sentence[1][1][1]
                       #print sentence[1]
                        
        for index, elem in enumerate(sentence):
            double_negation(elem)
    
    return sentence


  
#print sentence  

#sentence = ["or", ["and", ["and", "s", ["or", "p", "q"], ["and", "s", "t", "r"]], "p"], "s"]
#sentence = ["and", ["and", ["and", "p", "q"], ["and", "r", "q"], "p"], "s", ["or", "s", "t"], ["and", "s", "t"], "p"]
#sentence = ["and", ["and",["and",["and", "p", "s"], "i"], "p"],"m"]
#sentence = ["or", "a", "b", ["or", "p", "q"]]

""" associativity_or :- clauses of the form [or, [or, a, b], c, d] will be converted to 
	[or, a, b, c, d]
"""
def associativity_or(sentence):
    change = 0
    if isinstance(sentence, list):
        if sentence[0] == "or":
            i = 1
            length = len(sentence)
            print sentence
            while(i < length):
                if (isinstance(sentence[i], list)):
                    if (sentence[i][0] == "or"): #associativity for or
                        
                        temp = sentence[i]
                        sentence.pop(i)
                        print "sentence", sentence
                        change = 1
                        for item in temp[1:]:
                           # print "item is ",item
                            #associativity(item)
                        #sentence.pop(i)
                            sentence.append(item)
                            print item
                    else:
                        i = i + 1
                else:
                    i = i + 1
            if (change):
                associativity_or(sentence)
        for value in sentence:
            associativity_or(value)
    
    return sentence

""" associativity_and :- clauses of the form [and, [and, a, b], c, d] will be converted to 
	[and, a, b, c, d]
"""
def associativity_and(sentence):
    change = 0
    if isinstance(sentence, list):
        if sentence[0] == "and":
            i = 1
            length = len(sentence)
            print sentence
            while(i < length):
                if (isinstance(sentence[i], list)):
                    if (sentence[i][0] == "and"): #associativity for and
                        
                        temp = sentence[i]
                        sentence.pop(i)
                        change = 1
                        print "sentence", sentence
                        for item in temp[1:]:
                           # print "item is ",item
                            #associativity(item)
                        #sentence.pop(i)
                            sentence.append(item)
                            print item
                    else:
                        i = i + 1
                else:
                    i = i + 1
            if (change):
                associativity_and(sentence)
        for value in sentence:
            associativity_and(value)
    
    return sentence


""" distributivity :- clauses of the form [or, [and, a, b] c] will be coverted to 
	[and, [or, a, c], [or, b, c]]
"""
def distributivity(sentence):  
    change = 0
    if isinstance(sentence, list):
        if sentence[0] == "or":
            for item in sentence[1:]:
                distributivity(item)
            i = 1
            k = 1
            count = 0
            length = len(sentence)
            while(i < length):
                if (sentence[i][0] == "and"): 
                    count += 1
                    if k != i:
                        temp = sentence[k]
                        sentence[k] = sentence[i]
                        sentence[i] = temp
                        k += 1
                i += 1
            
            if count:
                sentence[0] = "and"
                new = ["and"]
                and_clause = sentence[1]
                rest_clause = sentence[2:]
                for item in and_clause[1:]:
                    temp = []
                    temp.append("or")
                    temp.append(item)
                    change = 1
                    for elem in rest_clause:
                        temp.append(elem)
                    new.append(temp)
                
                while(sentence):
                    sentence.pop()
                sentence.extend(new)
                print new
                if (change):
                    distributivity(sentence)       
        
        for item in sentence:
            distributivity(item)           
                            

""" extract_symbols :- helper function for removing duplicates
"""

def extract_symbols(sentence): 
    st = ""
    if sentence[0] == "not" and len(sentence) == 2:
        not_item = "~" + sentence[1]
        st = st + not_item
        if not_item in symbols:
            pass
        else:
            symbols[not_item] = 1
            results[not_item] = -1
    
        return st,symbols 
        
    for item in sentence:
        print"Item is", item
        if isinstance(item, list):
            if item[0] == "not":
                not_item = "~" + item[1]
                st = st + not_item
                if not_item in symbols:
                    pass
                else:
                    symbols[not_item] = 1
                    results[not_item] = -1
        else:
            if item != "or":
                st = st + item
                elem = item
                if elem in symbols:
                    pass
                else:
                    symbols[elem] = 1
                    results[elem] = -1
    
    return st, symbols

"""remove_duplicates :- Removal of duplicates and formating of output is done here
"""
def remove_dulplicates(sentence):
    print "sentence in remove", sentence
    global symbols
    dic = {}
    symbols = {}
    
    if isinstance(sentence, list):
        if sentence[0] == "not":
            return sentence
        elif sentence[0] == "or":
            #only one clause is present
            st,sym = extract_symbols(sentence)
            print st, symbols
            final = ["or"]
            for keys in symbols:
                if len(keys) == 1:
                    print "final", final
                    final.append(keys)
                else:
                    final.append(["not", keys[1]])
                
            if len(final) == 2:
                    final = final[1]
            return final        
        else:
            final = ["and"]
            for item in sentence[1:]:
                symbols = {}
                present = 0
                st,sym = extract_symbols(item)
                print "Symbol and st", st, sym
                for keys in dic:
                    if dic[keys] == sym:
                        present = 1
                        break
                if not present:
                    dic[st] = sym
                    total = ["or"]
                    for keys in symbols:
                        if len(keys) == 1:
                            total.append(keys)
                        else:
                            total.append(["not", keys[1]])
                    
                    if len(total) == 2:
                        total = total[1]
                    
                    final.append(total)
            
            if len(final) == 2:
                final = final[1]
            return final
                        
              
def cnf(sentence):
        global change
        sentence = implication_elimination(sentence)
        print "the elements are",sentence
        
        change = 1
        while(change):
            change = 0
            sentence = demorgan_and(sentence)
            sentence = demorgan_or(sentence)
            #double_negation(sentence)
            print "After 3", sentence
            
        
        change = 1
        while(change):
            change = 0
            sentence = double_negation(sentence)
        
        #Hack fix for removing extra not 
        if sentence[0] == "not" and isinstance(sentence[1], list):
            sentence = sentence[1][1]
        
        sentence = associativity_or(sentence)
        print "After calling or", sentence
        
        
        sentence = associativity_and(sentence)
        print "after calling and ", sentence,"\n"
        
        print sentence   
        distributivity(sentence)
        print sentence 
        
        
        sentence = associativity_or(sentence)
        print "After calling or", sentence
        
        sentence = associativity_and(sentence)
        print "After calling and", sentence
        
        result = remove_dulplicates(sentence)
        
        return result



input = open(sys.argv[2]).readlines()
output = open("sentences_CNF.txt", 'w')
input.pop(0)

for line in input:
  	print "input is ",line
	sentence = eval(line)
	sentence = cnf(sentence)
	if not isinstance(sentence, list):
		sentence = "'" + sentence + "'"
    #if not isinstance(sentence, list):
      #sentence = "'" + sentence + "'"
      
	output.write(str(sentence) + '\n')

output.close()
        
        

                
                   
                    
    
     
                          