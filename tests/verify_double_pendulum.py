"""physverify spec for the double pendulum in src/.

    physverify run tests/verify_double_pendulum.py

Angles are measured from the downward vertical, state = [theta1, theta2, omega1, omega2].
The reference equations are the closed-form solution of the Euler-Lagrange
equations (as in most textbooks), with D = theta1 - theta2 and
den = 2 m1 + m2 - m2 cos(2 D):

    theta1'' = (-g (2 m1 + m2) sin theta1 - m2 g sin(theta1 - 2 theta2)
                - 2 sin D m2 (omega2^2 L2 + omega1^2 L1 cos D)) / (L1 den)
    theta2'' = 2 sin D (omega1^2 L1 (m1 + m2) + g (m1 + m2) cos theta1
                + omega2^2 L2 m2 cos D) / (L2 den)

The reference energy is built from the Cartesian positions and velocities of
the two bobs, so it does not share the code's formula.

The project has no fixed-step solver of its own (run_simulation calls SciPy's
DOP853), so get_derivatives is stepped with physverify's RK4 and the order
studies expect 4: they check the equations, not SciPy.

What is checked:
- get_derivatives: manufactured solution, reference solution, whole trajectory,
  energy drift, exact patch test (at coarse steps, where round-off stays small).
- calculate_energy agrees with the Cartesian energy.
- run_simulation (DOP853, rtol 1e-12) from the README's benchmark state
  (both arms horizontal) keeps the energy within 1e-10 of its start over 30 s.
  E0 = 0 for that state, so the drift is measured relative to the energy scale
  (m1 + m2) g L1 + m2 g L2, not relative to E0.
"""
# pylint: disable=import-error,wrong-import-position,missing-function-docstring,too-many-locals

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from physverify import Check, ManufacturedODE, Result, ode_checks, patch_study
from physverify.steppers import integrate_fixed, rk4
from src.mechanics import calculate_energy, get_derivatives
from src.solvers import run_simulation

PARAMS = {"m1": 1.0, "m2": 1.5, "L1": 1.0, "L2": 0.7, "g": 9.81}
M1, M2, L1, L2, G = (PARAMS[k] for k in ("m1", "m2", "L1", "L2", "g"))
# Large swings, away from the small-angle regime. (From [1.2, -0.6, 0.5, 1.0] the energy drift
# changes sign between 40 and 80 steps, so its order is only clean from 160 steps on.)
Y0 = np.array([2.0, 1.0, 0.0, 0.0])
T_END = 1.0
NS = (80, 160, 320, 640)


def reference_rhs(_t, y):
    t1, t2, w1, w2 = y
    d = t1 - t2
    den = 2 * M1 + M2 - M2 * np.cos(2 * d)
    a1 = (-G * (2 * M1 + M2) * np.sin(t1) - M2 * G * np.sin(t1 - 2 * t2)
          - 2 * np.sin(d) * M2 * (w2**2 * L2 + w1**2 * L1 * np.cos(d))) / (L1 * den)
    a2 = 2 * np.sin(d) * (w1**2 * L1 * (M1 + M2) + G * (M1 + M2) * np.cos(t1)
                          + w2**2 * L2 * M2 * np.cos(d)) / (L2 * den)
    return np.array([w1, w2, a1, a2])


def energy(y, p=None):
    p = PARAMS if p is None else p
    m1, m2, l1, l2, g = p["m1"], p["m2"], p["L1"], p["L2"], p["g"]
    t1, t2, w1, w2 = y
    z1 = -l1 * np.cos(t1)  # heights of the bobs below the pivot
    z2 = z1 - l2 * np.cos(t2)
    vx1, vz1 = l1 * w1 * np.cos(t1), l1 * w1 * np.sin(t1)
    vx2, vz2 = vx1 + l2 * w2 * np.cos(t2), vz1 + l2 * w2 * np.sin(t2)
    kinetic = 0.5 * m1 * (vx1**2 + vz1**2) + 0.5 * m2 * (vx2**2 + vz2**2)
    return kinetic + m1 * g * z1 + m2 * g * z2


def integrate(source, y0, t_end, n, trajectory=False):
    def rhs(t, y):
        return np.asarray(get_derivatives(t, y, PARAMS), dtype=float) + source(t)

    if not trajectory:
        return integrate_fixed(rhs, y0, 0.0, t_end, n, rk4)
    h = t_end / n
    y = np.array(y0, dtype=float)
    states = [y]
    for i in range(n):
        y = rk4(rhs, i * h, y, h)
        states.append(y)
    return np.array(states)


def manufactured(t):
    return np.array([0.8 * np.sin(1.3 * t) + 0.2, -0.5 * np.cos(0.9 * t), 1.04 * np.cos(1.3 * t), 0.45 * np.sin(0.9 * t)])


def energy_function_agrees():
    rng = np.random.default_rng(4)
    worst = 0.0
    for _ in range(50):
        y = np.concatenate([rng.uniform(-np.pi, np.pi, 2), rng.uniform(-3, 3, 2)])
        worst = max(worst, abs(calculate_energy(y, **PARAMS) - energy(y)))
    if worst <= 1e-12:
        return Result("EXACT", f"agrees at 50 random states (largest difference {worst:.1e} J)")
    return Result("FAIL", f"differs from the Cartesian energy by up to {worst:.3g} J")


def readme_energy_claim():
    params = {"m1": 1.0, "m2": 1.0, "L1": 1.0, "L2": 1.0, "g": 9.81}
    y0 = [np.pi / 2, np.pi / 2, 0.0, 0.0]
    sol = run_simulation(y0, (0.0, 30.0), params)
    e = [energy(sol.y[:, k], params) for k in range(sol.y.shape[1])]
    scale = 2.0 * 9.81 * 1.0 + 1.0 * 9.81 * 1.0
    worst = max(abs(x - e[0]) for x in e) / scale
    if worst < 1e-10:
        return Result("PASS", f"largest |E - E0| / ((m1 + m2) g L1 + m2 g L2) = {worst:.1e} over 30 s")
    return Result("FAIL", f"largest |E - E0| / ((m1 + m2) g L1 + m2 g L2) = {worst:.2g} over 30 s, above 1e-10")


def checks():
    out = ode_checks(
        "get_derivatives + physverify RK4",
        integrate,
        rhs_ref=reference_rhs,
        mms=ManufacturedODE(manufactured, reference_rhs),
        y0_free=Y0,
        t_end=T_END,
        ns=NS,
        order=4.0,
        quantity=energy,
        integrate_trajectory=lambda s, y0, t, n: integrate(s, y0, t, n, trajectory=True),
    )
    patch_args = (integrate, reference_rhs, np.array([0.4, -0.2, 0.3, -0.5]), np.array([0.3, -0.5, 0.2, 0.1]),
                  T_END, (4, 8, 16, 32))
    return out + [
        Check("patch", "get_derivatives + physverify RK4", lambda: patch_study(*patch_args)),
        Check("invariant", "calculate_energy is the Cartesian energy", energy_function_agrees),
        Check("invariant", "run_simulation (DOP853) energy drift, README benchmark", readme_energy_claim),
    ]
