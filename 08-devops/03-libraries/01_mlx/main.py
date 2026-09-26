import mlx.core as mx
import inspect

# 1. Create arrays
a = mx.array([1.0, 2.0, 3.0])
b = mx.array([4.0, 5.0, 6.0])

# 2. Basic operations
c = a + b
print("c:", c)  # Output: array([5, 7, 9], dtype=float32)

# 3. Define a simple function: f(x) = x^2 + 3x + 5
def f(x):
    return x**2 + 3 * x + 5

# 4. Compute the derivative of f(x) using Automatic Differentiation
df = mx.grad(f)



x = mx.array(2.0)
df_dx = df(x)  # f'(x) = 2x + 3 -> f'(2) = 7

print("f(2):", f(x))       # Output: array(15, dtype=float32)
print("f'(2):", df_dx)     # Output: array(7, dtype=float32)
