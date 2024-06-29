import sympy

print(sympy.sympify("limit(sin(x)/x, x, 0)"))
equation1 = """
import sympy
x = sympy.symbols('x')
res = sympy.sympify("solveset(x**2 - x, x)")
print(res)
"""
equation2 = """
import sympy

A, B, C = sympy.symbols('A B C')
eq1 = sympy.Eq(A, 3*B)
eq2 = sympy.Eq(B, C + 12)
eq3 = sympy.Eq(C, A - 20)

res = sympy.solve((eq1, eq2, eq3), (A, B, C))
"""
vars = {}
exec(equation2, vars)
print(vars['res'])