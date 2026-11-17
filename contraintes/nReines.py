from ortools.sat.python import cp_model

###resolution du probleme des n reines 
## approche classique : une variable par ligne, valeur = colonne de la reine
## complexite de 3n(n-1)/2 contraintes
def reines_classiques(n=8):
    model = cp_model.CpModel()

    # q[i] = colonne de la reine de la ligne i, appellee Q_i
    q = [model.new_int_var(0, n - 1, f"Q_{i}") for i in range(n)]

    for i in range(n - 1):
        for j in range(i + 1, n):
            model.add(q[i] != q[j])              # colonnes differentes
            model.add(q[i] != q[j] + (j - i))    # diagonale
            model.add(q[i] != q[j] - (j - i))    # autre diagonale

    print(model.model_stats())
    print(len(model.proto.variables), "variables,", len(model.proto.constraints), "contraintes")
    print("-"*50)

    solver = cp_model.CpSolver()

    if solver.solve(model) == cp_model.OPTIMAL:
        print(solver.response_stats())
        print([solver.value(v) for v in q])


###resolution du probleme des n reines 
## approche par allDifferents
## complexite de 3 contraintes !
def reines_allDiff(n=8):
    model = cp_model.CpModel()
    q = [model.new_int_var(0, n - 1, f"Q_{i}") for i in range(n)]

    model.add_all_different(q)
    model.add_all_different(q[i] + i for i in range(n))
    model.add_all_different(q[i] - i for i in range(n))

    print(model.model_stats())
    print(len(model.proto.variables), "variables,", len(model.proto.constraints), "contraintes")
    print("-"*50)

    solver = cp_model.CpSolver()

    if solver.solve(model) == cp_model.OPTIMAL:
        print(solver.response_stats())
        print([solver.value(v) for v in q])


n=100
reines_classiques(n)
print("/\\"*100)
reines_allDiff(n)
