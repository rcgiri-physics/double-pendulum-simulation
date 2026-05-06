import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.solvers import run_simulation

def get_cartesian(theta1, theta2, L1, L2):
    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    x2 = x1 + L2 * np.sin(theta2)
    y2 = y1 - L2 * np.cos(theta2)
    return x1, y1, x2, y2

def animate_trajectory(sol, params):
    """Generates a dynamic animation of the double pendulum."""
    t = sol.t
    theta1, theta2 = sol.y[0], sol.y[1]
    L1, L2 = params['L1'], params['L2']
    
    x1, y1, x2, y2 = get_cartesian(theta1, theta2, L1, L2)

    fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
    ax.set_xlim(-(L1 + L2 + 0.5), (L1 + L2 + 0.5))
    ax.set_ylim(-(L1 + L2 + 0.5), (L1 + L2 + 0.5))
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_title("Double Pendulum Dynamics", fontsize=14, fontweight='bold')

    # Plot elements: The rods, the masses, and the trajectory trail
    line, = ax.plot([], [], 'o-', lw=2, color='black', markersize=8)
    trail, = ax.plot([], [], '-', lw=1, color='royalblue', alpha=0.6)
    
    # Store trail coordinates
    trail_x, trail_y = [], []

    def init():
        line.set_data([], [])
        trail.set_data([], [])
        return line, trail

    def update(frame):
        # Update the rods and masses (Origin -> Mass 1 -> Mass 2)
        thisx = [0, x1[frame], x2[frame]]
        thisy = [0, y1[frame], y2[frame]]
        line.set_data(thisx, thisy)
        
        # Update the trailing path
        trail_x.append(x2[frame])
        trail_y.append(y2[frame])
        
        # Optional: Keep only the last 150 frames of the trail so it doesn't clutter
        if len(trail_x) > 150:
            trail_x.pop(0)
            trail_y.pop(0)
            
        trail.set_data(trail_x, trail_y)
        return line, trail

    # Create the animation object
    dt = t[1] - t[0]
    ani = animation.FuncAnimation(fig, update, frames=len(t),
                                  init_func=init, blit=True, interval=dt*1000)
    
    # Save as GIF (Requires ImageMagick or standard writer depending on OS)
    os.makedirs('data/animations', exist_ok=True)
    ani.save('data/animations/pendulum_chaos.gif', writer='pillow', fps=30)
    
    plt.show()

if __name__ == "__main__":
    params = {'m1': 1.0, 'm2': 1.0, 'L1': 1.0, 'L2': 1.0, 'g': 9.81}
    
    # Using the same high-energy chaotic state
    initial_state = [np.pi/2, np.pi/2, 0.0, 0.0] 
    
    # We need a highly dense, evenly spaced time array for smooth 60fps animation
    t_span = (0, 20)
    t_eval = np.linspace(t_span[0], t_span[1], 1200) # 60 frames per second for 20 seconds
    
    print("Running high-density simulation for animation...")
   
    from scipy.integrate import solve_ivp
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
    from src.mechanics import get_derivatives
    
    sol = solve_ivp(
        get_derivatives, t_span, initial_state,
        args=(params,),
        method='DOP853', t_eval=t_eval, rtol=1e-12, atol=1e-14
    )
    
    print("Simulation complete. Rendering animation...")
    animate_trajectory(sol, params)