# Workforce Scheduling in OPL

Files:

- `workforce_scheduling.mod` — CPLEX MILP model.
- `workforce_scheduling.dat` — seven-day, two-shift sample instance.

Run both files in an OPL run configuration with CPLEX.

Decision variable `work[e][d][s]` equals 1 when employee `e` works shift `s` on day `d`.
