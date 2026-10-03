/******************************************************************************
 * Capacitated Vehicle Routing Problem (CVRP)
 * IBM ILOG CPLEX Optimization Studio / OPL
 *
 * Formulation:
 *   - binary arc variables x[i][j]
 *   - MTZ-style cumulative load variables u[i]
 *   - depot degree constraints limit the fleet size
 ******************************************************************************/

int n = ...;
range Nodes = 0..n-1;
int depot = ...;
{int} Customers = { i | i in Nodes : i != depot };

int vehicleCapacity = ...;
int maxVehicles = ...;
int demand[Nodes] = ...;
float xCoord[Nodes] = ...;
float yCoord[Nodes] = ...;

float distance[i in Nodes][j in Nodes] =
    sqrt((xCoord[i] - xCoord[j])^2 + (yCoord[i] - yCoord[j])^2);

dvar boolean x[Nodes][Nodes];
dvar float+ u[Customers];

minimize
    sum(i in Nodes, j in Nodes : i != j) distance[i][j] * x[i][j];

subject to {
    // Self-loops are forbidden.
    forall(i in Nodes)
        x[i][i] == 0;

    // Every customer is entered and left exactly once.
    forall(i in Customers)
        sum(j in Nodes : j != i) x[i][j] == 1;

    forall(j in Customers)
        sum(i in Nodes : i != j) x[i][j] == 1;

    // Limit the number of depot-to-customer routes by the available fleet.
    sum(j in Customers) x[depot][j] <= maxVehicles;
    sum(i in Customers) x[i][depot] <= maxVehicles;

    // Departures and returns at the depot must balance.
    sum(j in Customers) x[depot][j]
        == sum(i in Customers) x[i][depot];

    // Load bounds and MTZ-style capacity/subtour elimination constraints.
    forall(i in Customers) {
        u[i] >= demand[i];
        u[i] <= vehicleCapacity;
    }

    forall(i in Customers, j in Customers : i != j)
        u[j] >= u[i] + demand[j]
            - vehicleCapacity * (1 - x[i][j]);
}

execute DISPLAY_SOLUTION {
    writeln("Objective value: ", cplex.getObjValue());
    writeln("Selected arcs:");
    for (var i in Nodes) {
        for (var j in Nodes) {
            if (i != j && x[i][j] > 0.5) {
                writeln("  ", i, " -> ", j,
                        "  distance=", distance[i][j]);
            }
        }
    }
}
