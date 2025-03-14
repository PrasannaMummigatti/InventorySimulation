import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from regex import F

# Simulation parameters
np.random.seed(42)  # For reproducibility
num_periods = 100  # Number of time periods
s = 10  # Reorder point
S = 150  # Order-up-to level
initial_inventory = 0  # Starting inventory
lambda_demand =20   # Mean demand per period (Poisson)
OrderCount = 0
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
    #current_inventory =  current_inventory - demand[t]
    # Check if an order is needed

    if current_inventory <= s:
        OrderCount = OrderCount + 1
        # Place order to reach order-up-to level
        order_quantity = S - current_inventory
        orders[t] = order_quantity
        current_inventory = S  # Restock inventory

# Create figure and axes
fig, axes = plt.subplots(2, 1, figsize=(7, 7), sharex=True)

# Initialize plots
line_demand, = axes[0].plot([], [], marker='o', linestyle='-', label='Demand')
axes[0].set_xlim(0, num_periods)
axes[0].set_ylim(0, max(demand) + 2)
axes[0].set_ylabel('Demand')
axes[0].set_title('Demand Over Time')
axes[0].legend()
axes[0].grid()

line_inventory, = axes[1].step([], [], where='post', linestyle='-', color='g', label='Inventory Level')
axes[1].set_xlim(0, num_periods)
axes[1].set_ylim(-10, max(inventory) + 5)
axes[1].axhline(y=s, color='r', linestyle='--', label='s (Reorder Point)')
axes[1].axhline(y=S, color='b', linestyle='--', label='S (Order-up-to Level)')
axes[1].set_ylabel('Inventory')
axes[1].set_title('Inventory Level Over Time')
axes[1].text(10,20,OrderCount)
axes[1].legend()
axes[1].grid()

plt.xlabel('Time Periods')
plt.tight_layout()

# Animation function
def update(frame):
    line_demand.set_data(range(frame+1), demand[:frame+1])
    line_inventory.set_data(range(frame+1), inventory[:frame+1])
    return line_demand, line_inventory

# Create animation
ani = animation.FuncAnimation(fig, update, frames=num_periods, interval=100, blit=True,repeat=False)
plt.show()
