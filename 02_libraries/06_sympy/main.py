import sympy as sp

x = sp.Symbol('x')
f = x**2 + sp.sin(x)

df = sp.diff(f, x)  # Symbolic derivative
print(df)           # Output: 2*x + cos(x)
