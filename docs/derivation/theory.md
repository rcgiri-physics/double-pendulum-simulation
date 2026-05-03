# Lagrangian Dynamics of the Double Pendulum

## 1. System Overview

The double pendulum is a classic example of a simple physical system that exhibits complex, chaotic behavior. Unlike the Newtonian approach used in the 3-Body Laboratory, we utilize Lagrangian mechanics to handle the coordinate constraints and coupling between the two masses.

Coordinate System

We define the state of the system using two generalized coordinates:

- $\theta_1$: Angle of the first rod with the vertical.
- $\theta_2$: Angle of the second rod with the vertical.

The Cartesian positions of the masses $m_1$ and $m_2$ with lengths $L_1$ and $L_2$ are:

$$x_1 = L_1 \sin\theta_1$$

$$y_1 = -L_1 \cos\theta_1$$

$$x_2 = L_1 \sin\theta_1 + L_2 \sin\theta_2$$

$$y_2 = -L_1 \cos\theta_1 - L_2 \cos\theta_2$$

## 2. Energy Formulation

To construct the Lagrangian $L = T - V$, we derive the kinetic and potential energies.

Kinetic Energy ($T$)

The velocity components are found by differentiating the Cartesian positions with respect to time:

$$\dot{x}_1 = L_1 \dot{\theta}_1 \cos\theta_1, \quad \dot{y}_1 = L_1 \dot{\theta}_1 \sin\theta_1$$

$$\dot{x}_2 = L_1 \dot{\theta}_1 \cos\theta_1 + L_2 \dot{\theta}_2 \cos\theta_2, \quad \dot{y}_2 = L_1 \dot{\theta}_1 \sin\theta_1 + L_2 \dot{\theta}_2 \sin\theta_2$$

The total kinetic energy $T = \frac{1}{2}m_1 v_1^2 + \frac{1}{2}m_2 v_2^2$ simplifies to:

$$T = \frac{1}{2}(m_1+m_2)L_1^2\dot{\theta}_1^2 + \frac{1}{2}m_2L_2^2\dot{\theta}_2^2 + m_2L_1L_2\dot{\theta}_1\dot{\theta}_2\cos(\theta_1-\theta_2)$$

Potential Energy ($V$)

Taking the pivot as the reference $(y=0)$:$$V = -(m_1+m_2)gL_1\cos\theta_1 - m_2gL_2\cos\theta_2$$

## 3. The Euler-Lagrange Equations

The dynamics are governed by:

$$\frac{d}{dt} \left( \frac{\partial L}{\partial \dot{\theta}_i} \right) - \frac{\partial L}{\partial \theta_i} = 0$$

Expanding this for $\theta_1$ and $\theta_2$ results in two coupled, non-linear second-order ODEs. For numerical implementation, these are recast into the matrix form:

$$\mathbf{M}(\Theta) \ddot{\Theta} = \mathbf{f}(\Theta, \dot{\Theta})$$

Where $\mathbf{M}$ is the Mass Matrix:

$$\mathbf{M} = \begin{bmatrix} (m_1+m_2)L_1 & m_2L_2\cos(\theta_1-\theta_2) \\ L_1\cos(\theta_1-\theta_2) & L_2 \end{bmatrix}$$

And $\mathbf{f}$ is the Force Vector containing gravitational and centrifugal terms.

## 4. Quantifying Chaos

As the system energy increases, the periodic orbits shatter into chaotic flows. This project focuses on two primary metrics for this transition:

- Hamiltonian Conservation: Tracking $\Delta H = |(T+V)_t - (T+V)_0|$ to ensure numerical integrity.
- Bifurcation Analysis: Using Poincaré sections and Maximum Lyapunov Exponents (MLE) to map the sensitivity to initial conditions.

### Integration Strategy
- Small Angle: Validated against linear normal modes.
- Large Angle: Solved via high-order adaptive or symplectic integrators to prevent energy drift.