import numpy as np
import pytest
from src.mechanics import calculate_energy
from src.solvers import run_simulation

def test_initial_hamiltonian():
    """Verify energy calculation against analytical potential energy formula."""
    params = {'m1': 1.0, 'm2': 1.0, 'L1': 1.0, 'L2': 1.0, 'g': 9.81}
    # Stationary state: Kinetic Energy (T) = 0
    state = [np.pi/4, 0, 0, 0] 
    
    # 1. Numerical result from your engine
    energy = calculate_energy(state, **params)
    
    # 2. Analytical result: V = -(m1 + m2)gL1*cos(theta1) - m2gL2*cos(theta2)
    m1, m2, L1, L2, g = params['m1'], params['m2'], params['L1'], params['L2'], params['g']
    t1, t2 = state[0], state[1]
    expected_v = -(m1 + m2) * g * L1 * np.cos(t1) - m2 * g * L2 * np.cos(t2)

    print(f"\nDebug - Engine Energy:     {energy:.15f}")
    print(f"Debug - Analytical Energy: {expected_v:.15f}")
    
    # Check if they match within floating-point precision
    assert np.isclose(energy, expected_v, atol=1e-8), "Physics engine formula error!"

def test_numerical_stability():
    """Verify that the solver maintains energy conservation over time."""
    params = {'m1': 1.0, 'm2': 1.0, 'L1': 1.0, 'L2': 1.0, 'g': 9.81}
    initial_state = [np.pi/4, np.pi/4, 0, 0] 
    t_span = (0, 5)
    
    sol = run_simulation(initial_state, t_span, params)
    
    e0 = calculate_energy(sol.y[:, 0], **params)
    ef = calculate_energy(sol.y[:, -1], **params)
    
    # Relative drift (unitless) is best for high-precision comparisons
    rel_drift = np.abs((ef - e0) / e0)
    
    print(f"Energy Stability Check - Relative Drift: {rel_drift:.2e}")
    assert rel_drift < 1e-10, f"Numerical leakage too high: {rel_drift:.2e}"

if __name__ == "__main__":
    # Allows manual execution: python tests/test_mechanics.py
    print("Running Double Pendulum Physics Validation...")
    test_initial_hamiltonian()
    print("[PASS] Initial Hamiltonian matches theory.")
    
    try:
        test_numerical_stability()
        print("[PASS] Numerical drift is within research tolerance.")
    except AssertionError as e:
        print(f"[FAIL] {e}")