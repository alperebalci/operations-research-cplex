# Job-Shop Scheduling

This project implements a classical job-shop scheduling problem in OPL using **IBM CP Optimizer**.

Each job consists of an ordered sequence of operations. Every operation requires a specific machine for a fixed duration. The model minimizes the makespan while enforcing:

- operation precedence inside each job,
- no-overlap constraints on machines.

The native OPL implementation is in `opl/`.
