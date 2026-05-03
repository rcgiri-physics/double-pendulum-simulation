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