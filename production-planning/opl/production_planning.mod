/******************************************************************************
 * Multi-Period Capacitated Production Planning
 * IBM ILOG CPLEX Optimization Studio / OPL
 *
 * Features:
 *   - multiple products and periods
 *   - binary setup decisions
 *   - inventory balance
 *   - shared production capacity
 *   - optional overtime capacity
 *   - terminal inventory targets
 ******************************************************************************/

int numProducts = ...;
int numPeriods = ...;

range Products = 1..numProducts;
range Periods = 1..numPeriods;
range InventoryPeriods = 0..numPeriods;

string productName[Products] = ...;

float demand[Products][Periods] = ...;
float productionCost[Products] = ...;
float setupCost[Products] = ...;
float holdingCost[Products] = ...;
float processingTime[Products] = ...;

float regularCapacity[Periods] = ...;
float maxOvertime[Periods] = ...;
float overtimeCost[Periods] = ...;

float initialInventory[Products] = ...;
float targetEndingInventory[Products] = ...;
float maxProduction[Products][Periods] = ...;

dvar float+ production[Products][Periods];
dvar float+ inventory[Products][InventoryPeriods];
dvar boolean setup[Products][Periods];
dvar float+ overtime[Periods];

minimize
    sum(p in Products, t in Periods)
        productionCost[p] * production[p][t]
    + sum(p in Products, t in Periods)
        setupCost[p] * setup[p][t]
    + sum(p in Products, t in Periods)
        holdingCost[p] * inventory[p][t]
    + sum(t in Periods)
        overtimeCost[t] * overtime[t];

subject to {

    // Initial inventory is fixed by the input data.
    forall(p in Products)
        inventory[p][0] == initialInventory[p];

    // Inventory flow conservation.
    forall(p in Products, t in Periods)
        inventory[p][t - 1] + production[p][t]
            == demand[p][t] + inventory[p][t];

    // Production is possible only if the setup is activated.
    forall(p in Products, t in Periods)
        production[p][t]
            <= maxProduction[p][t] * setup[p][t];

    // Shared production-resource capacity.
    forall(t in Periods)
        sum(p in Products)
            processingTime[p] * production[p][t]
        <= regularCapacity[t] + overtime[t];

    // Overtime is bounded by period.
    forall(t in Periods)
        overtime[t] <= maxOvertime[t];

    // Preserve strategic stock at the end of the horizon.
    forall(p in Products)
        inventory[p][numPeriods] >= targetEndingInventory[p];
}

execute DISPLAY_SOLUTION {
    writeln("Objective value: ", cplex.getObjValue());
    writeln();

    for (var t in Periods) {
        var usedCapacity = 0.0;

        for (var p in Products) {
            usedCapacity += processingTime[p] * production[p][t];
        }

        writeln("Period ", t,
                " | regular capacity=", regularCapacity[t],
                " | used capacity=", usedCapacity,
                " | overtime=", overtime[t]);

        for (var p in Products) {
            writeln("  ", productName[p],
                    " | setup=", setup[p][t],
                    " | production=", production[p][t],
                    " | ending inventory=", inventory[p][t]);
        }
        writeln();
    }
}
