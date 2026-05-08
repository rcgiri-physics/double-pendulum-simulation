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

## Log 03: Chaos Quantification & Lyapunov Exponents
**Date:** May 2026

With the qualitative visualizations complete, the final phase required mathematical proof of the system's "sensitive dependence on initial conditions" (the Butterfly Effect).

### 1. The Perturbation Experiment
To quantify chaos, we measured the divergence of two nearly identical parallel universes in our phase space:
*   **Baseline State:** $\theta_1 = \pi/2, \theta_2 = \pi/2$
*   **Perturbed State:** $\theta_1 = \pi/2 + 10^{-10}$ (A microscopic shift on the order of atomic widths)

Both systems were integrated over 20 seconds using the `DOP853` engine. We then calculated the Euclidean distance between their 4D state vectors ($|\Delta y|$) and plotted the natural logarithm of this divergence ($\ln|\Delta y|$) against time.

### 2. Results & Analysis
*   **Exponential Growth:** The logarithmic plot revealed a clear linear climb starting from the initial $-23$ ($\ln(10^{-10})$) up until the physical limits of the pendulum caused saturation around $t = 15$ seconds.
*   **Maximum Lyapunov Exponent (MLE):** By applying a linear regression to the pre-saturation exponential growth phase ($t=1$ to $t=8$ seconds), we extracted the slope of the divergence.
*   **Calculated MLE ($\lambda$):** $\approx 0.26$

### 3. Conclusion
The strictly positive value of the Maximum Lyapunov Exponent ($\lambda \approx 0.26$) serves as the definitive mathematical proof that the double pendulum is a chaotic system. Because the divergence scales as $e^{\lambda t}$, the initial microscopic uncertainty is magnified by a factor of $e$ approximately every 3.8 seconds. This establishes a hard mathematical limit on the predictive horizon of the system, despite the deterministic nature of the underlying Lagrangian equations.
