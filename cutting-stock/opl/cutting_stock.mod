/******************************************************************************
 * Pattern-Based One-Dimensional Cutting Stock
 * IBM ILOG CPLEX Optimization Studio / OPL
 ******************************************************************************/

int stockLength = ...;
int numItemTypes = ...;
int numPatterns = ...;

range Items = 1..numItemTypes;
range Patterns = 1..numPatterns;

int itemLength[Items] = ...;
int demand[Items] = ...;
int pieces[Patterns][Items] = ...;

dvar int+ usePattern[Patterns];

minimize
    sum(p in Patterns) usePattern[p];

subject to {
    // Meet or exceed demand for each item type.
    forall(i in Items)
        sum(p in Patterns) pieces[p][i] * usePattern[p] >= demand[i];

    // Input patterns must fit inside one stock roll.
    forall(p in Patterns)
        sum(i in Items) itemLength[i] * pieces[p][i] <= stockLength;
}

execute DISPLAY_SOLUTION {
    var totalRolls = 0;
    var totalWaste = 0;

    writeln("Objective / stock rolls: ", cplex.getObjValue());
    writeln();

    for (var p in Patterns) {
        if (usePattern[p] > 0.5) {
            var usedLength = 0;
            for (var i in Items) {
                usedLength += itemLength[i] * pieces[p][i];
            }

            var patternWaste = stockLength - usedLength;
            totalRolls += usePattern[p];
            totalWaste += usePattern[p] * patternWaste;

            writeln("Pattern ", p,
                    " | rolls=", usePattern[p],
                    " | used length=", usedLength,
                    " | waste/roll=", patternWaste);
        }
    }

    writeln();
    writeln("Total rolls: ", totalRolls);
    writeln("Total waste: ", totalWaste);
}
