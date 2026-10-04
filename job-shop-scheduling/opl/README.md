# Job-Shop Scheduling in OPL / CP Optimizer

Files:

- `job_shop.mod` — CP Optimizer scheduling model.
- `job_shop.dat` — three-job, three-machine sample instance.

Create an OPL run configuration containing both files. Because the model starts with `using CP;`, OPL runs it with CP Optimizer rather than the CPLEX MIP engine.
