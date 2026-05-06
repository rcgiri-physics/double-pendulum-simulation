import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.mechanics import get_derivatives

def theta1_crossing(t, y, params):
    """
    The Event Tracker.
    This tells SciPy to look for the exact moment the first arm crosses the vertical axis.
    We use sin(theta1) so it catches it every time it does a full rotation too.
    """
    return np.sin(y[0])

# We only want to plot the points when it's swinging in one specific direction 
# (e.g., left to right) to ensure we are capturing the same phase of the system.
theta1_crossing.direction = 1 

def plot_poincare(sol):
    """Plots the discrete Poincaré section."""
    # sol.y_events[0] contains the state of the system ONLY at the crossing moments
    if len(sol.y_events[0]) == 0:
        print("No crossings detected! Try running the simulation longer.")
        return

    crossings = sol.y_events[0]
    
    # Extract theta2 and omega2 at the crossing events
    # We use modulo 2*pi so the angles stay bounded between -pi and pi on the graph
    theta2_vals = (crossings[:, 1] + np.pi) % (2 * np.pi) - np.pi
    omega2_vals = crossings[:, 3]

    fig, ax = plt.subplots(figsize=(8, 8), dpi=150)
    
    # small scatter dots instead of a line
    ax.scatter(theta2_vals, omega2_vals, s=2, color='crimson', alpha=0.7, edgecolors='none')
    
    ax.set_title("Poincaré Section ($\\theta_1 = 0$)", fontsize=14, fontweight='bold')
    ax.set_xlabel("Angle $\\theta_2$ (rad)", fontsize=12)
    ax.set_ylabel("Angular Velocity $\\omega_2$ (rad/s)", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_xlim(-np.pi, np.pi)
    
    os.makedirs('data/trajectories', exist_ok=True)
    filepath = 'data/trajectories/poincare_01.png'
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"Poincaré section saved to {filepath}")
    
    plt.show()

if __name__ == "__main__":
    params = {'m1': 1.0, 'm2': 1.0, 'L1': 1.0, 'L2': 1.0, 'g': 9.81}
    
    # We use a slightly less extreme chaotic state so it actually crosses the origin frequently
    initial_state = [np.pi/2, 0.0, 0.0, 0.0] 
    
    t_span = (0, 500)
    
    print(f"Simulating double pendulum for {t_span[1]} seconds. This may take a moment...")
    
    sol = solve_ivp(
        get_derivatives, t_span, initial_state,
        args=(params,),
        events=theta1_crossing, 
        method='DOP853', rtol=1e-10, atol=1e-12 
    )
    
    print(f"Simulation complete. Detected {len(sol.t_events[0])} crossing events.")
    print("Generating Poincaré scatter plot...")
    
    plot_poincare(sol)