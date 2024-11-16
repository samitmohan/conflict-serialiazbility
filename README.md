# Implementation of conflict serialiazbility.

serializibility is the effect of a concurrent schedule having the same effect as
SOME serial schedule for ALL initial values of data (transactions)

conflict serialiazbility is easier to compute(O(x^2) to check schedule, O(V+E) for topSort, hence O(N^2)), serializibility / view serialiazbility is np complete (exponential time) : harder to implement

# Steps for Conflict Serialiazbility

- Transaction input : input(transactions, data, schedule)
  transaction : T1,T2,T3
  data : A,B,C
  schedule : T1:R(A); T2:W(A) etc...

# Example of Input

TRANS:T1,T2,T3
DATA:A,B
SCHEDULE:
T1:R(A);
T2:W(B);
T3:W(A);
T1:R(A);

- Check for conflicting pairs (RW,WR,WW) on same data in different transactions
  (can be consecutive / non consecutive)
- Make precedence graph based on conflicting pairs
  - If graph acyclic : CS, if it contains Cycle : print the cycle and let it know its not CS
- Topological sort algo for computing order of transaction schedule for it to be CS.
- If no order : it is non CS and print that it's not conflict seriazable (note : Not CS != Not Serialiazble) : some schedules are serializable but not cs
