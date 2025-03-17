import numpy as np
import matplotlib.pyplot as plt

# Simulation Parameters
np.random.seed(42)  # For reproducibility
simulation_days = 100  # Total days to simulate
s = 20  # Reorder point
S = 80  # Order-up-to level
lead_time = 3  # Lead time in days
initial_inventory = 20  # Starting inventory

# Poisson Demand Parameters
lambda_demand = 5  # Average demand per day

# Simulation variables
inventory = initial_inventory
pending_orders = []  # Track outstanding orders (arrival_day, order_qty)
inventory_levels = []  # Track inventory levels
orders_placed = []  # Store days when orders are placed
demand_history = []  # Track daily demand
order_pending = False  # Flag to track if an order has already been placed

# Simulation loop
for day in range(simulation_days):
    # Check if any orders arrive today
    for arrival_day, order_qty in pending_orders[:]:
        if arrival_day == day:
            inventory += order_qty
            pending_orders.remove((arrival_day, order_qty))
            order_pending = False  # Reset flag since order arrived

    # Generate daily demand using Poisson distribution
    demand = np.random.poisson(lambda_demand)
    demand_history.append(demand)

    # Reduce inventory by demand
    inventory -= demand
    if inventory < 0:
        inventory = 0  # No backorders in this case

    # Place an order if inventory reaches or falls below s, but only if no order is pending
    if inventory <= s and not order_pending:
        order_qty = S - inventory  # Order up to S
        orders_placed.append(day)
        pending_orders.append((day + lead_time, order_qty))  # Arrives after lead time
        order_pending = True  # Prevent multiple orders before arrival

    # Track inventory levels
    inventory_levels.append(inventory)

# Plot results with subplots
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(8, 5), sharex=True)

# Demand Plot (Poisson demand)
#axes[0].plot(demand_history, color='blue', marker='o', linestyle='-', label="Daily Demand")
axes[0].bar(range(simulation_days), demand_history, color='lightblue', alpha=0.7, label="Daily Demand")
axes[0].set_ylabel("Demand")
axes[0].set_title("Daily Demand Over Time (Poisson)")
axes[0].legend()
axes[0].grid(True)

# Inventory Level Plot (Stepwise)
axes[1].plot(inventory_levels, label="Inventory Level", marker="", linestyle="-", drawstyle="steps-post")
axes[1].scatter(orders_placed, [s] * len(orders_placed), color='red', label="Order Placed", marker="x")
axes[1].axhline(y=s, color='r', linestyle='--', label="Reorder Point (s)")
axes[1].axhline(y=S, color='g', linestyle='--', label="Max Inventory (S)")
axes[1].set_xlabel("Time Period")
axes[1].set_ylabel("Inventory Level")
axes[1].set_title("Inventory (s,S) Level Over Time, LeadTime=3")
axes[1].legend()
axes[1].set_facecolor('lightgrey')
axes[1].grid(True)

plt.tight_layout()

manager = plt.get_current_fig_manager()
try:
    manager.window.wm_geometry("+100+100")  # For TkAgg backend
except AttributeError:
    manager.window.move(100, 100)  # For Qt5Agg backend
plt.text(88, 115, 'PrasannaMummigatti',style='italic', fontsize=5,color='blue')
plt.text(88, 0, 'PrasannaMummigatti',style='italic', fontsize=5,color='blue')
#plt.show()

plt.show()
