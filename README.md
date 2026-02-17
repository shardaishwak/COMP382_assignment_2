# COMP382_assignment_2

Step 1: Add new start variable with S0 -> S
-> we can simply takt the start_symbol and add it to the non-terminals, productions and the start symbol

Step 2: remove epsilon
-> We will go through all productions in search of epsilon. we will consider epsilon to be a nullable character. This way for each non-terminal we check if it contains eplison. If it does not, we do not need to check any production at all and exit early.
-> For each production, we will need to create a new version that does not have nullable. We can use combination of all nullable cpositions and compare them with the positions.

Step 3: We will remove all unit rules A -> B
-> This one is easy: we will go through each prodiction and verify whether a A -> B case exists and eliminate it directly

Step 4: Convert to binary form
-> we will first need to detect any termins in rules of lendgth >= 2. We can create the new production under U_* such as U_i -> ui
-> Then we consider the chain of 3+ elements as it becomes long. We will cut that one as X_j