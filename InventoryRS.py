import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
np.random.seed(42)  # For reproducibility
T = 100  # Number of periods to simulate
R = 19    # Review period (every R periods, we order)
S = 220  # Order-up-to level
lead_time = 2  # Fixed lead time
demand_lambda = 10  # Poisson distribution mean (λ)

# Initialize variables
inventory = 100  # Initial inventory
orders = [0] * (T + lead_time)  # Order arrivals
inventory_levels = []
demand_history = []
reorder_points = []
shortages = 0

# Simulation loop
for t in range(T):
    # Demand realization from Poisson distribution
    demand = np.random.poisson(demand_lambda)
    demand_history.append(demand)

    # Fulfill demand (if enough inventory)
    if inventory >= demand:
        inventory -= demand
    else:
        shortages += (demand - inventory)
        inventory = 0  # All stock is depleted

    # Order arrives if lead time has passed
    inventory += orders[t]

    # Periodic review: Place order every R periods
    if t % R == 0:
        order_quantity = max(0, S - inventory)  # Order to fill up to S
        orders[t + lead_time] = order_quantity  # Arrives after lead_time
        reorder_points.append((t, inventory))  # Store the reorder point

    # Record inventory level
    inventory_levels.append(inventory)

# Create subplots
fig, ax = plt.subplots(2, 1, figsize=(8, 5), sharex=True, gridspec_kw={'height_ratios': [1, 2]})

# Plot demand (line chart)
#ax[0].plot(range(T), demand_history, marker='', linestyle='-', color='gray', label="Demand")
ax[0].bar(range(T), demand_history, color='lightblue', alpha=0.7, label="Demand")
ax[0].set_ylabel("Demand")
ax[0].set_title("Demand over Time")
ax[0].set_ylim(0, max(demand_history) + 5)  # Start Y-axis from zero
ax[0].legend()
ax[0].grid()

# Plot inventory levels (step chart)
ax[1].step(range(T), inventory_levels, where='mid', linestyle='-', color='b', label="Inventory Level")
ax[1].axhline(S, color='r', linestyle='--', label='Order-up-to Level (S)')

# Add vertical dotted lines for review periods & keep a label only once
for t in range(0, T, R):
    ax[1].axvline(x=t, color='gray', linestyle='dotted', alpha=0.7, label="Review Period" if t == 0 else "")

# Mark reorder points with red crosses
if reorder_points:
    reorder_x, reorder_y = zip(*reorder_points)  # Extract coordinates
    ax[1].scatter(reorder_x, reorder_y, color='red', marker='x', s=100, label="Reorder Point")

ax[1].set_xlabel("Time Period")
ax[1].set_ylabel("Inventory Level")
ax[1].set_title("(R,S) Inventory Policy Simulation with LeadTime=2")
ax[1].set_facecolor('lightgrey')
ax[1].set_ylim(0, S + 10)  # Start Y-axis from zero
ax[1].legend()
ax[1].grid()

# Show plot
plt.tight_layout()
plt.show()

# Output summary
print(f"Total shortages over {T} periods: {shortages}")
