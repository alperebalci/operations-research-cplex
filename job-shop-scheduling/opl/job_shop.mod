/******************************************************************************
 * Job-Shop Scheduling
 * IBM ILOG CP Optimizer / OPL
 ******************************************************************************/

using CP;

int numJobs = ...;
int numMachines = ...;
int numOperationsPerJob = ...;

range Jobs = 1..numJobs;
range Machines = 1..numMachines;
range Operations = 1..numOperationsPerJob;

string jobName[Jobs] = ...;
string machineName[Machines] = ...;

int machine[Jobs][Operations] = ...;
int duration[Jobs][Operations] = ...;

dvar interval task[j in Jobs][o in Operations] size duration[j][o];

minimize
    max(j in Jobs) endOf(task[j][numOperationsPerJob]);

subject to {
    // Preserve the operation order within each job.
    forall(j in Jobs, o in 1..numOperationsPerJob-1)
        endBeforeStart(task[j][o], task[j][o+1]);

    // A machine can process at most one operation at a time.
    forall(m in Machines)
        noOverlap(all(j in Jobs, o in Operations : machine[j][o] == m)
            task[j][o]);
}

execute DISPLAY_SCHEDULE {
    writeln("Makespan: ", cp.getObjValue());
    writeln();

    for (var j in Jobs) {
        writeln(jobName[j], ":");
        for (var o in Operations) {
            writeln("  op ", o,
                    " | machine=", machineName[machine[j][o]],
                    " | start=", task[j][o].start,
                    " | end=", task[j][o].end);
        }
    }
}
