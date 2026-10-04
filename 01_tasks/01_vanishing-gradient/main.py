import torch
import torch.nn as nn

# 1. Setup reproducibility
torch.manual_seed(42)

# 2. Define a deep network using Sigmoid activations
class DeepNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        # 5 fully connected layers
        self.layer1 = nn.Linear(10, 10)
        self.layer2 = nn.Linear(10, 10)
        self.layer3 = nn.Linear(10, 10)
        self.layer4 = nn.Linear(10, 10)
        self.layer5 = nn.Linear(10, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.sigmoid(self.layer1(x))
        x = self.sigmoid(self.layer2(x))
        x = self.sigmoid(self.layer3(x))
        x = self.sigmoid(self.layer4(x))
        x = self.layer5(x)  # Output layer (no activation)
        return x

# 3. Instantiate model, create dummy input and target
model = DeepNetwork()
dummy_input = torch.randn(1, 10)
target = torch.tensor([[1.0]])

# 4. Forward pass & compute a basic MSE loss
output = model(dummy_input)
criterion = nn.MSELoss()
loss = criterion(output, target)

# 5. Backward pass to calculate gradients
loss.backward()

# 6. Check the average gradient absolute value for each layer
print(f"Layer 5 (Output) gradient norm: {model.layer5.weight.grad.abs().mean().item():.8f}")
print(f"Layer 4          gradient norm: {model.layer4.weight.grad.abs().mean().item():.8f}")
print(f"Layer 3          gradient norm: {model.layer3.weight.grad.abs().mean().item():.8f}")
print(f"Layer 2          gradient norm: {model.layer2.weight.grad.abs().mean().item():.8f}")
print(f"Layer 1 (Input)  gradient norm: {model.layer1.weight.grad.abs().mean().item():.8f}")
