import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
initial_inventory = 10  # Initial inventory level
s = 6  # Reorder point
Q = 80  # Order quantity
num_periods = 100  # Number of time periods

# Generate random demand
np.random.seed(0)  # For reproducibility
demand = np.random.poisson(lam=3, size=num_periods)  # Poisson-distributed demand

# Initialize inventory tracking
inventory = np.zeros(num_periods)
inventory[0] = initial_inventory
orders_placed = np.zeros(num_periods)

# Simulate inventory over time
for t in range(1, num_periods):
    inventory[t] = inventory[t - 1] - demand[t - 1]
    if inventory[t] <= s:
        orders_placed[t] = Q
        inventory[t] += Q

# Setup figure for animation
fig, ax = plt.subplots(2, 1, figsize=(7, 7))

# Demand Plot
ax[0].set_xlim(0, num_periods)
ax[0].set_ylim(0, max(demand) + 2)
ax[0].set_title('Demand over Time')
#ax[0].set_xlabel('Time Period')
ax[0].set_ylabel('Demand')
ax[0].grid(True)
demand_line, = ax[0].plot([], [], 'b-', label="Demand")
ax[0].legend()

# Inventory Plot
ax[1].set_xlim(0, num_periods)
ax[1].set_ylim(0, max(inventory) + 5)
ax[1].set_title('(s, Q) Inventory Policy Simulation')
ax[1].set_xlabel('Time Period')
ax[1].set_ylabel('Inventory Level')
ax[1].axhline(y=s, color='r', linestyle='--', label="Reorder Point (s)")
ax[1].set_facecolor('lightgrey')
ax[1].grid(True)
inventory_line, = ax[1].step([], [], where='post', color='g', label="Inventory Level")
ax[1].legend()

# Animation update function
def update(frame):
    demand_line.set_data(np.arange(frame), demand[:frame])
    
    # Update inventory step plot
    inventory_line.set_data(np.arange(frame), inventory[:frame])
    
    return demand_line, inventory_line

# Create animation
ani = animation.FuncAnimation(fig, update, frames=num_periods, interval=200, blit=True,repeat=False)

plt.show()
