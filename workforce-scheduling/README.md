# Workforce Scheduling

This project implements a weekly multi-shift workforce scheduling problem as a MILP in IBM ILOG CPLEX Optimization Studio using OPL.

The model assigns employees to day/night shifts while minimizing assignment cost and respecting:

- shift coverage requirements,
- employee availability,
- at most one shift per employee per day,
- minimum and maximum weekly workload,
- maximum consecutive working days.

The native OPL implementation is in `opl/`.
