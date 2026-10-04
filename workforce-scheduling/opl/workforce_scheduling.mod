/******************************************************************************
 * Weekly Workforce Scheduling
 * IBM ILOG CPLEX Optimization Studio / OPL
 ******************************************************************************/

int numEmployees = ...;
int numDays = ...;
int numShifts = ...;

range Employees = 1..numEmployees;
range Days = 1..numDays;
range Shifts = 1..numShifts;

string employeeName[Employees] = ...;
string dayName[Days] = ...;
string shiftName[Shifts] = ...;

int demand[Days][Shifts] = ...;
int availability[Employees][Days][Shifts] = ...;
float assignmentCost[Employees][Shifts] = ...;
int minShifts[Employees] = ...;
int maxShifts[Employees] = ...;
int maxConsecutiveDays = ...;

dvar boolean work[Employees][Days][Shifts];

minimize
    sum(e in Employees, d in Days, s in Shifts)
        assignmentCost[e][s] * work[e][d][s];

subject to {
    // Required staffing level for every day and shift.
    forall(d in Days, s in Shifts)
        sum(e in Employees) work[e][d][s] >= demand[d][s];

    // Respect employee availability.
    forall(e in Employees, d in Days, s in Shifts)
        work[e][d][s] <= availability[e][d][s];

    // At most one shift per employee per day.
    forall(e in Employees, d in Days)
        sum(s in Shifts) work[e][d][s] <= 1;

    // Weekly workload limits.
    forall(e in Employees) {
        sum(d in Days, s in Shifts) work[e][d][s] >= minShifts[e];
        sum(d in Days, s in Shifts) work[e][d][s] <= maxShifts[e];
    }

    // Any window of maxConsecutiveDays + 1 days must contain a day off.
    forall(e in Employees, firstDay in 1..numDays-maxConsecutiveDays)
        sum(d in firstDay..firstDay+maxConsecutiveDays, s in Shifts)
            work[e][d][s] <= maxConsecutiveDays;
}

execute DISPLAY_SCHEDULE {
    writeln("Objective value: ", cplex.getObjValue());
    writeln();

    for (var d in Days) {
        writeln(dayName[d], ":");
        for (var s in Shifts) {
            write("  ", shiftName[s], " -> ");
            for (var e in Employees) {
                if (work[e][d][s] > 0.5) {
                    write(employeeName[e], " ");
                }
            }
            writeln();
        }
    }
}
