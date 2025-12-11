from ortools.linear_solver import pywraplp


def solve_min_items_unbounded(items, target, time_limit_s=30, debug=False):
    """
    ILP model:
      - x[i] = how many times item i is used (integer >=0)
      - each item i increments certain dimensions by +1
      - final state must match exactly the target vector
      - minimize total picks = sum(x[i])

    Parameters:
        items: list of tuples/lists of indices incremented by 1 when item is used
        target: list/tuple of target integers
        time_limit_s: solver time limit
        debug: enable solver internal logs

    Returns:
        (min_total, counts_per_item) if optimal
        None, info            if not optimal or infeasible
    """

    solver = pywraplp.Solver.CreateSolver("CBC")
    if solver is None:
        raise RuntimeError("CBC solver unavailable")

    n_items = len(items)
    n_dims = len(target)

    # --------------------------------------------------------------
    # 1) Upper bounds (critical for speed)
    # --------------------------------------------------------------
    # An item cannot be used more times than the smallest target
    # dimension it affects.
    upper_bounds = []
    for inc in items:
        if not inc:
            upper_bounds.append(0)
            continue
        ub = min(target[j] for j in inc)
        upper_bounds.append(ub)

    # --------------------------------------------------------------
    # 2) Decision variables: integer >=0
    # --------------------------------------------------------------
    x = [
        solver.IntVar(0, upper_bounds[i], f"x_{i}")
        for i in range(n_items)
    ]

    # --------------------------------------------------------------
    # 3) Objective: minimize total picks
    # --------------------------------------------------------------
    solver.Minimize(solver.Sum(x))

    # --------------------------------------------------------------
    # 4) EXACT constraints: final state == target
    # --------------------------------------------------------------
    for j in range(n_dims):
        solver.Add(
            solver.Sum(
                x[i] * (1 if j in items[i] else 0)
                for i in range(n_items)
            ) == target[j]
        )

    # --------------------------------------------------------------
    # 5) Debug logging
    # --------------------------------------------------------------
    if debug:
        solver.EnableOutput()   # no args in new OR-Tools

    # --------------------------------------------------------------
    # 6) Time limit
    # --------------------------------------------------------------
    solver.SetTimeLimit(int(time_limit_s * 1000))

    # --------------------------------------------------------------
    # 7) Solve
    # --------------------------------------------------------------
    status = solver.Solve()

    # OR-Tools 10-compatible status names
    status_map = {
        solver.OPTIMAL: "OPTIMAL",
        solver.FEASIBLE: "FEASIBLE",
        solver.INFEASIBLE: "INFEASIBLE",
        solver.UNBOUNDED: "UNBOUNDED",
        solver.ABNORMAL: "ABNORMAL",
        solver.NOT_SOLVED: "NOT_SOLVED",
    }
    status_name = status_map.get(status, f"UNKNOWN({status})")

    if debug:
        print("Status:", status_name)
        print("Objective value:", solver.Objective().Value())

    # --------------------------------------------------------------
    # 8) Accept only TRUE optimal
    # --------------------------------------------------------------
    if status != solver.OPTIMAL:
        return None, {
            "status": status_name,
            "note": "Solution NOT guaranteed optimal"
        }

    # --------------------------------------------------------------
    # 9) Extract optimal solution
    # --------------------------------------------------------------
    sol = [int(x[i].solution_value()) for i in range(n_items)]
    total = sum(sol)

    return total, sol
