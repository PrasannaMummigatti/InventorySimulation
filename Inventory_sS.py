import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Simulation parameters
np.random.seed(42)  # For reproducibility
num_periods = 100  # Number of time periods
s = 50  # Reorder point
S = 250  # Order-up-to level
initial_inventory = 0  # Starting inventory
lambda_demand = 20   # Mean demand per period (Poisson)
OrderCount = 0  # Count of orders placed

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
        OrderCount += 1
        order_quantity = S - current_inventory  # Order to replenish stock
        orders[t] = order_quantity
        current_inventory = S  # Restock inventory

# Create figure and axes
fig, axes = plt.subplots(2, 1, figsize=(8, 5), sharex=True)

# Demand Plot (Animated Bar Chart)
bars = axes[0].bar(range(num_periods), np.zeros(num_periods), color='lightblue', alpha=0.7, label='Demand')
axes[0].set_xlim(0, num_periods)
axes[0].set_ylim(0, max(demand) + 5)
axes[0].set_ylabel('Demand')
axes[0].set_title('Demand Over Time')
axes[0].legend()
axes[0].grid(axis='y')

# Inventory Level Plot (Stepwise)
line_inventory, = axes[1].step([], [], where='post', linestyle='-', color='g', label='Inventory Level')
axes[1].set_xlim(0, num_periods)
axes[1].set_ylim(-10, max(inventory) + 10)
axes[1].axhline(y=s, color='r', linestyle='--', label='s (Reorder Point)')
axes[1].axhline(y=S, color='b', linestyle='--', label='S (Order-up-to Level)')
axes[1].set_ylabel('Inventory')
axes[1].set_title('Inventory Level Over Time')
axes[1].legend()
axes[1].grid(axis='y')

plt.xlabel('Time Periods')
plt.tight_layout()

# Animation function
def update(frame):
    # Update demand bars dynamically
    for i, bar in enumerate(bars):
        if i <= frame:
            bar.set_height(demand[i])  # Update bar height
        else:
            bar.set_height(0)  # Hide future bars
    
    # Update inventory step plot
    line_inventory.set_data(range(frame + 1), inventory[:frame + 1])
    
    return bars, line_inventory

# Create animation
ani = animation.FuncAnimation(fig, update, frames=num_periods, interval=100, blit=False, repeat=False)

plt.show()
