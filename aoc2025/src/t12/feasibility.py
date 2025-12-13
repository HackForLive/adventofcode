import pulp

# -----------------------------
# Grid
# -----------------------------
# W, L = 15, 15

# -----------------------------
# Tile shapes (example)
# -----------------------------
# base_shape = [
#     (0,0),(1,0),(2,0),
#     (0,1),(1,1),
#            (1,2),(2,2)
# ]

# shapes = [base_shape] * 6   # replace with 6 different shapes
# tile_count = [4, 1, 20, 30, 25, 14]

# -----------------------------
# Rotation handling
# -----------------------------
def rotate(shape):
    return [(y, 2 - x) for x, y in shape]

def normalize(shape):
    minx = min(x for x, y in shape)
    miny = min(y for x, y in shape)
    return sorted((x - minx, y - miny) for x, y in shape)

def unique_rotations(shape):
    rots = set()
    cur = shape
    for _ in range(4):
        cur = rotate(cur)
        rots.add(tuple(normalize(cur)))
    return [list(r) for r in rots]

# rotations = [unique_rotations(s) for s in shapes]

def feasibility(W: int, L: int, shapes: list[tuple[int, int]], rotations: list[list[int]], 
                tile_count: list[int]):
    # -----------------------------
    # Model
    # -----------------------------
    model = pulp.LpProblem("Polyomino_Packing", pulp.LpStatusOptimal)

    x = {}

    for t in range(len(shapes)):
        for i in range(tile_count[t]):
            for r, shape in enumerate(rotations[t]):
                for px in range(W):
                    for py in range(L):
                        if all(px + dx < W and py + dy < L for dx, dy in shape):
                            x[t,i,r,px,py] = pulp.LpVariable(
                                f"x_{t}_{i}_{r}_{px}_{py}", cat="Binary"
                            )

    # -----------------------------
    # Each tile used once
    # -----------------------------
    for t in range(len(shapes)):
        for i in range(tile_count[t]):
            model += pulp.lpSum(
                var for (tt,ii, *_), var in x.items()
                if tt == t and ii == i
            ) == 1

    # -----------------------------
    # No overlap
    # -----------------------------
    for cx in range(W):
        for cy in range(L):
            covering = []
            for (t,i,r,px,py), var in x.items():
                for dx, dy in rotations[t][r]:
                    if px + dx == cx and py + dy == cy:
                        covering.append(var)
            if covering:
                model += pulp.lpSum(covering) <= 1

    # -----------------------------
    # Solve
    # -----------------------------
    model.solve(pulp.PULP_CBC_CMD(msg=0))
    print("Status:", pulp.LpStatus[model.status])
