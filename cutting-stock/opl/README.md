# Cutting Stock in OPL

Files:

- `cutting_stock.mod` — integer programming model.
- `cutting_stock.dat` — sample stock/item/pattern data.

Run both files with CPLEX. The execute block reports selected patterns and total material waste.

This is a compact pattern-based formulation; it does not implement column generation.
