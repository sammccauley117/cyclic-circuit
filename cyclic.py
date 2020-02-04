# Description: program that can accept 2n logic functions and generate the
#   cyclic circuit implementing these functions, if possible.
# Author: Samuel McCauley
# Date: February 3rd, 2020

LENGTH = 6 # Desired length of Rivest circuit

# Potential functions to connect, where the uppercase letters are inverted
functions = [
    'b&(A|C)',
    'A&b&c',
    'A|B|c',
    'a|(b&c)',
    'c&(a|B)',
    'c&(a|b)',
    'A|(b&C)',
    '(A&C)|B'
]

# Potential symbols, where the uppercase letters are inverted
symbols = 'abcABC'
unique_symbols = '' # Just the lowercase, not the inverted uppercase
for c in  set(symbols.lower()):
    unique_symbols += c

# Initialize the graph that maps valid connections
graph = {}
for i in range(len(functions)):
    graph['f'+str(i+1)] = []

# Takes a function, cycles through all possibilities, and returns truth table
def all_solutions(function):
    solutions = []

    for binary in range(2**len(unique_symbols)):
        d = {}
        for i in range(len(unique_symbols)):
            d[unique_symbols[i]] = int((binary & (1 << i)) > 0)
            d[unique_symbols[i].upper()] = 1 - d[unique_symbols[i]]
        solutions.append(eval(function, d))

    return solutions

# Check whether or not a cyclic function can be applied between two functions
def check_connections(i1, i2):
    function_1 = functions[i1]
    function_2 = functions[i2]

    solutions = all_solutions(function_1)

    for symbol in symbols:
        # AND
        if solutions == all_solutions('{}&({})'.format(symbol,function_2)):
            print('f{0} = {2} & f{1}'.format(i1+1,i2+1,symbol))
            graph['f'+str(i2+1)].append('f'+str(i1+1))
        # OR
        if solutions == all_solutions('{}|({})'.format(symbol,function_2)):
            print('f{0} = {2} | f{1}'.format(i1+1,i2+1,symbol))
            graph['f'+str(i2+1)].append('f'+str(i1+1))
        # NAND
        if solutions == all_solutions('1-({}&({}))'.format(symbol,function_2)):
            print('f{0} = ~({2} & f{1})'.format(i1+1,i2+1,symbol))
            graph['f'+str(i2+1)].append('f'+str(i1+1))
        # NOR
        if solutions == all_solutions('1-({}|({}))'.format(symbol,function_2)):
            print('f{0} = ~({2} | f{1})'.format(i1+1,i2+1,symbol))
            graph['f'+str(i2+1)].append('f'+str(i1+1))

# Find all valid Rivest Circuit cycles of the predetermined length
def possible_paths(root, visited=[]):
    current_path = visited + [root]
    if len(current_path) == LENGTH and current_path[0] in graph[current_path[-1]]:
        print(current_path)
    else:
        for next in graph[root]:
            if next not in current_path:
                possible_paths(next, current_path)

# Print all of our valid cyclic connections between functions
print('\nConnections:')
for i in range(len(functions)):
    for j in range(len(functions)):
        if i != j:
            check_connections(i,j)

# Print valid cycles of LENGTH
print('\nValid Cycles')
for start in graph.keys():
    possible_paths(start)

# Show connection graph
print('\nGraph')
for key in graph.keys():
    print(key+': '+str(graph[key]))
print()
