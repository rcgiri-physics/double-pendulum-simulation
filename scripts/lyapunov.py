import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.mechanics import get_derivatives

def calculate_lyapunov(sol1, sol2, t):
    """Calculates phase space divergence and extracts the Lyapunov Exponent."""
    # Calculate the Euclidean distance between the two trajectories in 4D phase space
    divergence = np.linalg.norm(sol1.y - sol2.y, axis=0)
    
    # Avoid log(0) at t=0 by adding a tiny epsilon
    log_divergence = np.log(divergence + 1e-20)
    
    # In chaotic systems, divergence grows exponentially at first, then saturates.
    # We want to find the slope of the linear region BEFORE it saturates.
    # For this high-energy state, exponential growth usually happens between 1 and 8 seconds.
    linear_region_mask = (t > 1) & (t < 8) 
    
    if np.any(linear_region_mask):
        t_fit = t[linear_region_mask]
        log_div_fit = log_divergence[linear_region_mask]
        
        # Fit a line (y = mx + b) where m is the Lyapunov Exponent
        slope, intercept = np.polyfit(t_fit, log_div_fit, 1)
    else:
        slope, intercept = 0, 0
        print("Could not find a valid linear region for fitting.")

    return divergence, log_divergence, slope, intercept

def plot_divergence(t, log_divergence, slope, intercept):
    """Plots the logarithmic divergence to visually confirm exponential growth."""
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    
    # Plot the actual divergence data
    ax.plot(t, log_divergence, lw=1.5, color='royalblue', label='Log Divergence $\\ln(|\\Delta y|)$')
    
    # Plot the trendline
    t_trend = np.linspace(1, 8, 100)
    ax.plot(t_trend, slope * t_trend + intercept, '--', color='crimson', lw=2, 
            label=f'Lyapunov Fit ($\\lambda \\approx {slope:.2f}$)')

    ax.set_title("Sensitive Dependence on Initial Conditions", fontsize=14, fontweight='bold')
    ax.set_xlabel("Time (s)", fontsize=12)
    ax.set_ylabel("Log Divergence $\\ln(|\\Delta y|)$", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='upper left')
    
    os.makedirs('data/analysis', exist_ok=True)
    filepath = 'data/analysis/lyapunov_divergence.png'
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"\nLyapunov plot saved to {filepath}")
    print(f"==================================================")
    print(f"ESTIMATED MAXIMUM LYAPUNOV EXPONENT: {slope:.4f}")
    print(f"==================================================")
    if slope > 0:
        print("A positive value mathematically confirms the system is CHAOTIC.")
    
    plt.show()

if __name__ == "__main__":
    params = {'m1': 1.0, 'm2': 1.0, 'L1': 1.0, 'L2': 1.0, 'g': 9.81}
    
    # State 1: The Baseline
    state_baseline = [np.pi/2, np.pi/2, 0.0, 0.0]
    
    # State 2: The Perturbation (Shift theta1 by a microscopic 10^-10 radians)
    perturbation = 1e-10
    state_perturbed = [np.pi/2 + perturbation, np.pi/2, 0.0, 0.0]
    
    # 20 seconds is plenty of time to see the exponential divergence happen and saturate
    t_span = (0, 20)
    t_eval = np.linspace(t_span[0], t_span[1], 2000) 
    
    print("Running Baseline Simulation...")
    sol1 = solve_ivp(get_derivatives, t_span, state_baseline, args=(params,), 
                     method='DOP853', t_eval=t_eval, rtol=1e-12, atol=1e-14)
                     
    print("Running Perturbed Simulation...")
    sol2 = solve_ivp(get_derivatives, t_span, state_perturbed, args=(params,), 
                     method='DOP853', t_eval=t_eval, rtol=1e-12, atol=1e-14)
    
    print("Computing Lyapunov divergence...")
    div, log_div, lambda_max, intercept = calculate_lyapunov(sol1, sol2, t_eval)
    
    plot_divergence(t_eval, log_div, lambda_max, intercept)