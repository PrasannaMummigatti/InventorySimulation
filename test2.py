import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
np.random.seed(42)  # For reproducibility
num_periods = 100  # Number of time periods
s = 20  # Reorder point
S = 100  # Order-up-to level
initial_inventory = 50  # Starting inventory
lambda_demand = 5  # Mean demand per period (Poisson)

# Arrays to store results
demand = np.random.poisson(lambda_demand, num_periods)
inventory = np.zeros(num_periods)
orders = np.zeros(num_periods)

# Initialize inventory level
current_inventory = initial_inventory

for t in range(num_periods):
    # Record inventory level before demand is realized
    inventory[t] = current_inventory
    
    # Apply demand
    current_inventory = max(0, current_inventory - demand[t])
    
    # Check if an order is needed
    if current_inventory <= s:
        order_quantity = S - current_inventory
        orders[t] = order_quantity
        current_inventory = S  # Restock inventory

# Plot results
fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# Demand over time
axes[0].plot(range(num_periods), demand, marker='o', linestyle='-', label='Demand')
axes[0].set_ylabel('Demand')
axes[0].set_title('Demand Over Time')
axes[0].legend()
axes[0].grid()

# Inventory level over time (step format)
axes[1].step(range(num_periods), inventory, where='post', linestyle='-', color='g', label='Inventory Level')
axes[1].axhline(y=s, color='r', linestyle='--', label='s (Reorder Point)')
axes[1].axhline(y=S, color='b', linestyle='--', label='S (Order-up-to Level)')
axes[1].set_ylabel('Inventory')
axes[1].set_title('Inventory Level Over Time')
axes[1].legend()
axes[1].grid()

plt.xlabel('Time Periods')
plt.tight_layout()
plt.show()
