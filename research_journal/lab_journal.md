# Research Journal: Double Pendulum Simulation
**Project Phase:** Lagrangian Dynamics & Chaos Quantification
**Date:** May 2026

## Log 01: Transition to Lagrangian Framework
Today marks the shift from the Newtonian vector summation used in the 3-Body Laboratory to the Lagrangian framework ($L = T - V$). The objective is to handle coupled non-linearities without the algebraic mess of explicit scalar expansions.

### 1. Numerical Strategy: The Acceleration Matrix
To maintain high precision, we avoid manual derivation of $\ddot{\theta}_1$ and $\ddot{\theta}_2$. Instead, we implement the system in matrix form:
$$\mathbf{M}(\Theta) \ddot{\Theta} = \mathbf{f}(\Theta, \dot{\Theta})$$

This allows us to utilize `np.linalg.solve` within each integration step, ensuring that the coupling between masses $m_1$ and $m_2$ is handled with double-precision floating-point accuracy.

### 2. Validation Milestones
Using the `DOP853` integrator (8th-order Runge-Kutta), the following benchmarks were established:

| Metric | Target | Result | Status |
| :--- | :--- | :--- | :--- |
| **Static Hamiltonian** | Analytical Match | Matches to $10^{-8}$ | PASS |
| **Energy Drift ($\Delta H$)** | $< 10^{-10}$ | $3.29 \times 10^{-13}$ | PASS |

### 3. Observations
*   **Zero-Energy Trap:** Initial tests at $\theta = \pi/2$ showed "high" relative drift because the starting Hamiltonian was exactly $0.0\text{ J}$. This was corrected by shifting to a $45^\circ$ baseline to provide a non-zero denominator for relative error calculations.
*   **Precision:** The drift of $10^{-13}$ over 5-10 seconds of integration is exceptional, providing a "clean" environment for upcoming bifurcation sweeps.

---

## Log 02: Phase Space Visualization
**Date:** May 2026

With the mathematical baseline secured, the focus shifted to mapping the chaotic regimes of the double pendulum.

### 1. Real-Time Kinematics
Implemented `matplotlib.animation.FuncAnimation` to track the Cartesian trajectory of the lower mass. The core challenge involved optimizing `scipy.integrate.solve_ivp` to output a highly dense, evenly spaced time array (1200 frames over 20 seconds) while passing the parameter dictionary via tuple unpacking. This resulted in a smooth, 60fps validation of the chaotic motion.

### 2. Poincaré Sections
To find the hidden order within the continuous chaos, we utilized SciPy's event tracking. 
*   **Methodology:** The system state was sampled only when the primary arm crossed the vertical axis ($\theta_1 = 0$). 
*   **Observations:** This reduced the complex continuous paths into a discrete phase space scatter plot ($\theta_2$ vs $\omega_2$). The resulting geometry formed a bounded "U-shape". This topology visually confirms our energy conservation firewall: the extreme angular velocities (kinetic energy peaks) only occurred at the exact points where potential energy was minimized, perfectly bounding the chaos within the physical limits of the system.

---

