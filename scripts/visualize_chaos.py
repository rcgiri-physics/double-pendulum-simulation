import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Ensure Python can find your 'src' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.solvers import run_simulation

def get_cartesian(theta1, theta2, L1, L2):
    """Converts angular coordinates to Cartesian (x, y) space."""
    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    
    x2 = x1 + L2 * np.sin(theta2)
    y2 = y1 - L2 * np.cos(theta2)
    
    return x1, y1, x2, y2

def plot_trajectory(sol, params):
    """Generates the Cartesian path and Phase Space plots."""
    t = sol.t
    theta1 = sol.y[0]
    theta2 = sol.y[1]
    omega2 = sol.y[3]

    # Convert angular data to Cartesian coordinates
    x1, y1, x2, y2 = get_cartesian(theta1, theta2, params['L1'], params['L2'])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=100)

    # Plot 1: Cartesian Trajectory (The "Spaghetti" Plot)
    ax1.plot(x2, y2, lw=0.6, color='royalblue', alpha=0.8, label='Mass 2 Path')
    ax1.set_title("Cartesian Trajectory of Mass 2", fontsize=12, fontweight='bold')
    ax1.set_xlabel("x position (m)")
    ax1.set_ylabel("y position (m)")
    ax1.set_aspect('equal')
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Plot 2: Phase Space of Mass 2 (The Strange Attractor)
    ax2.plot(theta2, omega2, lw=0.4, color='crimson', alpha=0.7)
    ax2.set_title("Phase Space: $\\theta_2$ vs $\\omega_2$", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Angle $\\theta_2$ (rad)")
    ax2.set_ylabel("Angular Velocity $\\omega_2$ (rad/s)")
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    
    # Save the output to your data folder
    os.makedirs('data/trajectories', exist_ok=True)
    filepath = 'data/trajectories/chaotic_run_01.png'
    plt.savefig(filepath, dpi=300)
    print(f"Plot successfully saved to {filepath}")
    
    plt.show()

if __name__ == "__main__":
    # Standard benchmark parameters
    params = {'m1': 1.0, 'm2': 1.0, 'L1': 1.0, 'L2': 1.0, 'g': 9.81}
    
    # High-energy chaotic initial state: Both arms horizontal (90 degrees)
    initial_state = [np.pi/2, np.pi/2, 0.0, 0.0] 
    t_span = (0, 30) # 30 seconds of simulated chaos
    
    print(f"Simulating double pendulum for {t_span[1]} seconds...")
    sol = run_simulation(initial_state, t_span, params)
    print("Simulation complete. Generating plots...")
    
    plot_trajectory(sol, params)