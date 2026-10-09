import mlx.core as mx

# 1. Create MLX arrays (NumPy-like API)
a = mx.array([1.0, 2.0, 3.0])
b = mx.array([4.0, 5.0, 6.0])

# 2. Perform basic element-wise operations
c = a + b
d = mx.sin(a) * mx.cos(b)

# 3. Trigger evaluation (MLX uses lazy evaluation)
print("c:", c)
print("d:", d)

# 4. Automatic differentiation (gradient of sin(x) at pi)
def loss_fn(x):
    return mx.sum(mx.sin(x))

grad_fn = mx.grad(loss_fn)
x_val = mx.array(3.14159 / 2)
print("Gradient of sin(x) at pi/2:", grad_fn(x_val))
