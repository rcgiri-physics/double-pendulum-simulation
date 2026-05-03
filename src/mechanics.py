import numpy as np

def get_accelerations(state, m1, m2, L1, L2, g=9.81):
    """Solves M(theta) * alpha = f for the double pendulum."""
    t1, t2, w1, w2 = state
    dt = t1 - t2

    # Mass Matrix M(theta)
    M = np.array([
        [(m1 + m2) * L1, m2 * L2 * np.cos(dt)],
        [L1 * np.cos(dt), L2]
    ])

    # Force Vector f(theta, omega)
    f = np.array([
        -m2 * L2 * (w2**2) * np.sin(dt) - (m1 + m2) * g * np.sin(t1),
        L1 * (w1**2) * np.sin(dt) - g * np.sin(t2)
    ])

    return np.linalg.solve(M, f)

def calculate_energy(state, m1, m2, L1, L2, g=9.81):
    """Calculates the Total Hamiltonian (T + V)."""
    t1, t2, w1, w2 = state
    
    T = 0.5 * (m1 + m2) * (L1 * w1)**2 + \
        0.5 * m2 * (L2 * w2)**2 + \
        m2 * L1 * L2 * w1 * w2 * np.cos(t1 - t2)
    
    V = -(m1 + m2) * g * L1 * np.cos(t1) - m2 * g * L2 * np.cos(t2)
    
    return T + V

def get_derivatives(t, state, params):
    """Standardized wrapper for ODE integrators."""
    t1, t2, w1, w2 = state
    alpha1, alpha2 = get_accelerations(state, **params)
    return [w1, w2, alpha1, alpha2]