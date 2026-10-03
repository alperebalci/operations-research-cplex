/******************************************************************************
 * Capacitated Facility Location Problem
 * IBM ILOG CPLEX Optimization Studio / OPL
 *
 * Decisions:
 *   - which facilities to open
 *   - which facility serves each customer
 *
 * Objective:
 *   minimize fixed opening costs + assignment/transportation costs
 ******************************************************************************/

int numFacilities = ...;
int numCustomers = ...;

range Facilities = 1..numFacilities;
range Customers = 1..numCustomers;

string facilityName[Facilities] = ...;
string customerName[Customers] = ...;

float fixedCost[Facilities] = ...;
float capacity[Facilities] = ...;
float demand[Customers] = ...;
float assignmentCost[Facilities][Customers] = ...;

dvar boolean open[Facilities];
dvar boolean assign[Facilities][Customers];

minimize
    sum(f in Facilities) fixedCost[f] * open[f]
  + sum(f in Facilities, c in Customers)
        assignmentCost[f][c] * assign[f][c];

subject to {
    // Every customer must be assigned to exactly one facility.
    forall(c in Customers)
        sum(f in Facilities) assign[f][c] == 1;

    // Customers can only be assigned to open facilities.
    forall(f in Facilities, c in Customers)
        assign[f][c] <= open[f];

    // Facility capacity cannot be exceeded.
    forall(f in Facilities)
        sum(c in Customers) demand[c] * assign[f][c]
            <= capacity[f] * open[f];
}

execute DISPLAY_SOLUTION {
    writeln("Objective value: ", cplex.getObjValue());
    writeln();

    for (var f in Facilities) {
        if (open[f] > 0.5) {
            var usedCapacity = 0.0;
            writeln("Open facility: ", facilityName[f]);

            for (var c in Customers) {
                if (assign[f][c] > 0.5) {
                    usedCapacity += demand[c];
                    writeln("  -> ", customerName[c],
                            " | demand=", demand[c],
                            " | assignment cost=", assignmentCost[f][c]);
                }
            }

            writeln("  Used capacity: ", usedCapacity,
                    " / ", capacity[f]);
            writeln();
        }
    }
}
