from tkinter import font
from turtle import color
from click import style
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
initial_inventory = 10  # Initial inventory level
s = 6  # Reorder point
Q = 80  # Order quantity
num_periods = 100  # Number of time periods

# Generate random demand
np.random.seed(20)  # For reproducibility
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
fig, ax = plt.subplots(2, 1, figsize=(8, 5), sharex=True)

# Demand Plot (Bar Chart)
ax[0].set_xlim(0, num_periods)
ax[0].set_ylim(0, max(demand) + 2)
ax[0].set_title('Demand over Time')
ax[0].set_ylabel('Demand')
ax[0].grid(True)
bars = ax[0].bar(range(num_periods), np.zeros(num_periods), color='lightblue', alpha=0.7, label="Demand")
ax[0].legend()

# Inventory Plot (Step Chart)
ax[1].set_xlim(0, num_periods)
ax[1].set_ylim(0, max(inventory) + 10)
ax[1].set_title('(s, Q) Inventory Policy Simulation, LeadTime=0')
ax[1].set_xlabel('Time Period')
ax[1].set_ylabel('Inventory Level')
ax[1].axhline(y=s, color='r', linestyle='--', label="Reorder Point (s)")
ax[1].set_facecolor('lightgrey')

ax[1].grid(True)
inventory_line, = ax[1].step([], [], where='post', color='g', label="Inventory Level")
ax[1].legend()

# Animation update function
def update(frame):
    # Update demand bars
    for i in range(frame):
        bars[i].set_height(demand[i])  # Set bar height
    
    # Update inventory step plot
    inventory_line.set_data(np.arange(frame), inventory[:frame])
    
    return bars, inventory_line

# Create animation
ani = animation.FuncAnimation(fig, update, frames=num_periods, interval=10, blit=False, repeat=True)


manager = plt.get_current_fig_manager()
try:
    manager.window.wm_geometry("+100+100")  # For TkAgg backend
except AttributeError:
    manager.window.move(100, 100)  # For Qt5Agg backend
plt.text(88, 115, 'PrasannaMummigatti',style='italic', fontsize=5,color='blue')
plt.text(88, 0, 'PrasannaMummigatti',style='italic', fontsize=5,color='blue')
plt.show()

#plt.show()
