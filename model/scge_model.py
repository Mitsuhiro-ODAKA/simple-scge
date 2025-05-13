from gamspy import Container, Set, Parameter, Variable, Equation, Model, Sum, VariableType

def build_model():
    # Create a container
    m = Container()

    # Define a set (region)
    reg = Set(m, name="region", records=["A", "B"])

    # Define parameters
    alpha = Parameter(m, name="alpha", records=[0.3])  # scalar
    rho = Parameter(m, name="rho", records=[0.5])
    L = Parameter(m, name="L", domain=[reg], records=[["A", 20], ["B", 80]])
    K_total = Parameter(m, name="K_total", records=[200])  # scalar

    # Define variables
    Y = Variable(m, name="Y", domain=[reg], type=VariableType.POSITIVE)
    K = Variable(m, name="K", domain=[reg], type=VariableType.POSITIVE)
    C = Variable(m, name="C", domain=[reg], type=VariableType.POSITIVE)
    C.lo = 1e-3
    U = Variable(m, name="U", type=VariableType.FREE)
    Z = Variable(m, name="Z", type=VariableType.FREE)

    # Define equation
    obj = Equation(m, name="obj")
    obj[:] = Z == U

    eq_prod = Equation(m, name="eq_prod", domain=[reg])
    eq_prod[:] = Y[reg] == L[reg] ** alpha * K[reg] ** (1 - alpha)

    kap_constraint = Equation(m, name="kap_constraint")
    kap_constraint[:] = Sum(reg, K[reg]) == K_total
    
    # Consumption = Yield
    eq_cons = Equation(m, name="eq_cons", domain=[reg])
    eq_cons[:] = C[reg] == Y[reg]

    # Utility function：U = (C_A^rho + C_B^rho)^(1/rho)
    eq_utility = Equation(m, name="eq_utility")
    eq_utility[:] = U == (Sum(reg, C[reg] ** rho)) ** (1 / rho)

    # Define model
    model = Model(name="SCGE", equations=[obj, eq_prod, kap_constraint, eq_cons, eq_utility], container=m,
                  problem="nlp", sense="MAX", objective=Z)

    return m, model
