from cycle_detect import Graph
from cycle_print import *

graph = {} # printing cycles if present
try:
    def isConflicting(instr1, instr2):
        if instr1 == "VACANT" or instr2 == "VACANT": return False
        op1, op2 = instr1[0], instr2[0]
        data1, data2 = instr1[2], instr2[2]
        if op1 == "W" or op2 == "W":
            if data1 == data2: return True #conflict
        return False

    fn = input("Enter file name path : ")
    with open(fn) as f:
        first_line = f.readline().split(":")
        trans = len(first_line[1].split(',')) # number of transactions

    #2d arr for diff transactions
    ls = [[] for _ in range(trans)]
    with open(fn) as f:
        for _ in range(3): # skip first 3 lines (only care about schedule)
            temp = f.readline()
        line = f.readline() # real transaction schedule
        while line:
            level1 = line.split(":")
            trans_number = int(level1[0][1]) # extract 1 from T1, 2 from T2,,,
            count = 0
            for _ in range(len(ls)):
                if _ == trans_number - 1:
                    ls[_].append(level1[1][:-2])
                else:
                    ls[_].append("VACANT")
            line = f.readline()
    print("Schedule : ")
    for lst in ls:
        print(lst)

    # making precendence graph
    # Conflict graph creation
    g = Graph(trans)
    graph = defaultdict(list)  # Use defaultdict for simpler edge additions
    L = len(ls[0]) # length of trans
    for t_id in range(trans):
        for i in range(L):
            instr = ls[t_id][i]
            for j in range(trans):
                if j == t_id: 
                    continue  # Skip self-dependencies
                for k in range(i + 1, L):
                    if isConflicting(instr, ls[j][k]):
                        g.addEdge(t_id, j)
                        graph[t_id].append(j)  # Add edge to the cycle printing graph
    print("Result:")
    if g.iC():
        print("Not CS")
        print("Cycles:")
        if graph:
            cycle_printing_fn(graph)
        else:
            print("No cycles detected.")
    else:
        print("CS")
        print("Order of execution:")
        order = g.topSort()
        print(" -> ".join(f"T{item + 1}" for item in order))
except FileNotFoundError:
    print("Error: File not found. Please provide a valid file path.")
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")