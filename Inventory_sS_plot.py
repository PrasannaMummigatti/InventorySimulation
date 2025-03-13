import numpy as np
import matplotlib.pyplot as plt

# Parameters
np.random.seed(42)
periods = 50  # Number of time periods
s = 3        # Reorder point
S = 10        # Order-up-to level
lambda_demand = 2  # Mean demand per period (Poisson)

# Initialize variables
inventory = S  # Start with full inventory
inventory_levels = [inventory]
demands = []

# Simulate demand and inventory over time
for t in range(periods):
    demand = np.random.poisson(lambda_demand)  # Random demand
    demands.append(demand)
    
    # Reduce inventory based on demand``
    inventory -= demand
    inventory = max(0, inventory)  # No negative inventory
    
    # Apply (s, S) policy
    if inventory < s:
        inventory = S  # Replenish to S
    
    inventory_levels.append(inventory)

# Create subplots
fig, axes = plt.subplots(2, 1, figsize=(7, 7), sharex=True)

# Demand subplot (on top)
axes[0].plot(range(periods), demands, linestyle='-', marker='o', color='r', label="Demand")
axes[0].set_ylabel("Demand")
axes[0].set_title("Demand Over Time")
axes[0].legend()
axes[0].grid(True)

# Inventory levels subplot (bottom)
axes[1].step(range(periods + 1), inventory_levels, where="post", linestyle='-', linewidth=2, label="Inventory Level")

# Add dotted lines for s and S levels
axes[1].axhline(y=s, color='gray', linestyle='dotted', linewidth=1.5, label=f"s = {s}")
axes[1].axhline(y=S, color='blue', linestyle='dotted', linewidth=1.5, label=f"S = {S}")

axes[1].set_xlabel("Time Periods")
axes[1].set_ylabel("Inventory Level")
axes[1].set_title("Inventory Over Time")
axes[1].legend()
axes[1].grid(True)

# Adjust layout
plt.tight_layout()
plt.show()
