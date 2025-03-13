import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
s = 5               # Reorder threshold
S = 30              # Target inventory level
num_days = 30       # Simulation duration
lambda_demand = 5   # Average daily demand (Poisson parameter)
initial_inventory = S  # Starting inventory
np.random.seed(42)  # Seed for reproducibility

# Initialize simulation
current_inventory = initial_inventory
inventory_levels = []
daily_demands = []
orders_placed = []

# Run simulation
for _ in range(num_days):
    # Check if we need to place an order
    if current_inventory <= s:
        order_qty = S - current_inventory
        current_inventory = S  # Instant replenishment
    else:
        order_qty = 0
    
    # Generate daily demand
    demand = np.random.poisson(lambda_demand)
    actual_demand = min(demand, current_inventory)
    
    # Update inventory after meeting demand
    current_inventory = max(current_inventory - demand, 0)
    
    # Record daily values
    daily_demands.append(actual_demand)
    orders_placed.append(order_qty)
    inventory_levels.append(current_inventory)

# Create time axis for plotting
days = list(range(1, num_days + 1))

# Create figure with subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Plot demand
ax1.bar(days, daily_demands, color='tab:blue')
ax1.set_title('Daily Demand Pattern')
ax1.set_ylabel('Units Demanded')
ax1.grid(True, linestyle='--', alpha=0.7)

# Plot inventory levels
ax2.plot(days, inventory_levels, marker='o', color='tab:red', linewidth=2)
ax2.axhline(s, color='k', linestyle='--', label=f'Reorder threshold (s={s})')
ax2.axhline(S, color='g', linestyle='--', label=f'Target level (S={S})')
ax2.set_title('Inventory Level Tracking')
ax2.set_xlabel('Day')
ax2.set_ylabel('Inventory Level')
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend()

plt.tight_layout()
plt.show()