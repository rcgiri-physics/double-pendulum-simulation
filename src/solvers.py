from scipy.integrate import solve_ivp
from .mechanics import get_derivatives

def run_simulation(initial_state, t_span, params, method='DOP853'):
    """High-precision adaptive integration using DOP853."""
    return solve_ivp(
        get_derivatives, 
        t_span, 
        initial_state, 
        method=method, 
        args=(params,),
        rtol=1e-12, 
        atol=1e-14
    )